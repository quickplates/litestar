from collections.abc import Callable, Iterator, Mapping
from dataclasses import dataclass, fields
from typing import Any, cast, override

from litestar._openapi.datastructures import RegisteredSchema, SchemaRegistry
from litestar._openapi.schema_generation import SchemaCreator
from litestar.config.app import AppConfig
from litestar.openapi.spec import (
    XML,
    Discriminator,
    ExternalDocumentation,
    OpenAPIFormat,
    OpenAPIType,
    Reference,
    Schema,
)
from litestar.plugins import InitPlugin
from litestar.plugins.pydantic import (
    PydanticDIPlugin,
    PydanticInitPlugin,
    PydanticSchemaPlugin,
)
from litestar.typing import FieldDefinition
from pydantic import TypeAdapter

type Transform[I, O] = Callable[[I], O]


@dataclass
class CustomSchema(Schema):
    """Custom schema that fixes some issues."""

    default: Any = ...

    @override
    def to_schema(self) -> dict[str, Any]:
        schema = super().to_schema()

        if self.default is ...:
            schema.pop("default", None)
        else:
            schema["default"] = self.default

        return schema


class SchemaGenerator:
    """Generator of JSON schemas for annotations."""

    def __init__(self, namespace: tuple[str, ...], *, by_alias: bool = True) -> None:
        self.namespace = namespace
        self.by_alias = by_alias

    @property
    def _ref_template(self) -> str:
        prefix = "_".join((*self.namespace, ""))
        return f"#/components/schemas/{prefix}" + "{model}"

    def generate(self, annotation: Any) -> dict[str, Any]:
        """Generate JSON schema for the given annotation."""
        return TypeAdapter(annotation).json_schema(
            by_alias=self.by_alias, ref_template=self._ref_template
        )


class SchemaConverter:
    """Standard converter for raw schemas to schema models."""

    def __init__(self, references: dict[str, Reference] | None = None) -> None:
        self.references = references or {}

    @property
    def _fields(self) -> list[tuple[str, str]]:
        return [
            (field.name, field.metadata.get("alias", field.name))
            for field in fields(Schema)
        ]

    @property
    def _transforms(self) -> dict[str, Transform]:
        return {
            "allOf": lambda value: [self.convert(schema) for schema in value],
            "anyOf": lambda value: [self.convert(schema) for schema in value],
            "oneOf": lambda value: [self.convert(schema) for schema in value],
            "not": self.convert,
            "if": self.convert,
            "then": self.convert,
            "else": self.convert,
            "dependentSchemas": lambda value: {
                key: self.convert(schema) for key, schema in value.items()
            },
            "prefixItems": lambda value: [self.convert(schema) for schema in value],
            "items": self.convert,
            "contains": self.convert,
            "properties": lambda value: {
                key: self.convert(schema) for key, schema in value.items()
            },
            "patternProperties": lambda value: {
                key: self.convert(schema) for key, schema in value.items()
            },
            "additionalProperties": lambda value: value
            if isinstance(value, bool)
            else self.convert(value),
            "propertyNames": self.convert,
            "unevaluatedItems": self.convert,
            "unevaluatedProperties": self.convert,
            "type": lambda value: [OpenAPIType(t) for t in value]
            if isinstance(value, list)
            else OpenAPIType(value),
            "format": lambda value: OpenAPIFormat(value),
            "contentSchema": self.convert,
            "discriminator": lambda value: Discriminator(
                property_name=value["propertyName"],
                mapping=value.get("mapping"),
            ),
            "xml": lambda value: XML(
                name=value.get("name"),
                namespace=value.get("namespace"),
                prefix=value.get("prefix"),
                attribute=value.get("attribute", False),
                wrapped=value.get("wrapped", False),
            ),
            "externalDocs": lambda value: ExternalDocumentation(
                url=value["url"],
                description=value.get("description"),
            ),
        }

    def _handle_reference(self, schema: dict[str, Any]) -> Reference:
        ref = schema["$ref"]
        name = ref.split("/")[-1]
        return self.references.get(name, Reference(ref=ref))

    def _build_schema(self, schema: dict[str, Any]) -> Schema:
        args = {
            field: self._transforms.get(alias, lambda x: x)(schema[alias])
            for field, alias in self._fields
            if alias in schema
        }
        return CustomSchema(**args)

    def convert(self, schema: dict[str, Any]) -> Schema | Reference:
        """Convert raw schema to schema model."""
        if "$ref" in schema:
            return self._handle_reference(schema)

        return self._build_schema(schema)


class DefinitionRegistry(Mapping[tuple[str, ...], RegisteredSchema]):
    """Registry for schema definitions."""

    def __init__(self, registry: SchemaRegistry) -> None:
        self.registry = registry

    def register(self, key: tuple[str, ...]) -> RegisteredSchema:
        """Register new definition."""
        field = FieldDefinition.from_annotation(
            type(key[-1], (), {"__module__": ".".join(key[:-1])})
        )

        self.registry.get_schema_for_field_definition(field)
        reference = self.registry.get_reference_for_field_definition(field)

        if reference is None:
            raise LookupError

        return self.registry.from_reference(reference)

    @override
    def __iter__(self) -> Iterator[tuple[str, ...]]:
        for registration in self.registry:
            yield registration.key

    @override
    def __len__(self) -> int:
        return len(list(self.__iter__()))

    @override
    def __getitem__(self, key: tuple[str, ...]) -> RegisteredSchema:
        for registration in self.registry:
            if registration.key == key:
                return registration

        raise KeyError(key)


class DefinitionsRegistrator:
    """Registrator for schema definitions."""

    def __init__(self, registry: SchemaRegistry, namespace: tuple[str, ...]) -> None:
        self.namespace = namespace
        self.registry = DefinitionRegistry(registry)

    def _resolve_registrations(
        self, definitions: dict[str, dict[str, Any]]
    ) -> tuple[dict[str, RegisteredSchema], dict[str, RegisteredSchema]]:
        existing: dict[str, RegisteredSchema] = {}
        new: dict[str, RegisteredSchema] = {}

        for name in definitions:
            key = (*self.namespace, name)

            if registration := self.registry.get(key):
                existing[name] = registration
            else:
                new[name] = self.registry.register(key)

        return existing, new

    def _get_references(
        self, registrations: dict[str, RegisteredSchema]
    ) -> dict[str, Reference]:
        return {
            "_".join(registration.key): registration.references[0]
            for registration in registrations.values()
        }

    def register(self, definitions: dict[str, dict[str, Any]]) -> dict[str, Reference]:
        """Register definitions."""
        existing, new = self._resolve_registrations(definitions)

        references = self._get_references(existing | new)
        converter = SchemaConverter(references)

        for name, registration in new.items():
            registration.schema = cast("Schema", converter.convert(definitions[name]))

        return references


class CustomPydanticSchemaPlugin(PydanticSchemaPlugin):
    """Custom plugin that creates schemas from the ones generated by Pydantic."""

    def _get_namespace(self, annotation: Any) -> tuple[str, ...]:
        if hasattr(annotation, "__annotation__"):
            return self._get_namespace(annotation.__annotation__)

        return tuple(annotation.__module__.split("."))

    def _generate_schema(
        self, annotation: Any, namespace: tuple[str, ...]
    ) -> dict[str, Any]:
        generator = SchemaGenerator(namespace, by_alias=self.prefer_alias)
        return generator.generate(annotation)

    def _register_definitions(
        self,
        definitions: dict[str, dict[str, Any]],
        schema_creator: SchemaCreator,
        namespace: tuple[str, ...],
    ) -> dict[str, Reference]:
        registrator = DefinitionsRegistrator(schema_creator.schema_registry, namespace)
        return registrator.register(definitions)

    def _convert(
        self, schema: dict[str, Any], references: dict[str, Reference]
    ) -> Schema:
        converter = SchemaConverter(references)
        return cast("Schema", converter.convert(schema))

    @override
    def to_openapi_schema(
        self, field_definition: FieldDefinition, schema_creator: SchemaCreator
    ) -> Schema:
        namespace = self._get_namespace(field_definition.annotation)
        schema = self._generate_schema(field_definition.annotation, namespace)

        definitions = schema.pop("$defs", {})
        references = self._register_definitions(definitions, schema_creator, namespace)

        return self._convert(schema, references)


class PydanticPlugin(InitPlugin):
    """Plugin for Pydantic integration."""

    @override
    def on_app_init(self, app_config: AppConfig) -> AppConfig:
        app_config.plugins.extend(
            [
                PydanticInitPlugin(prefer_alias=True, round_trip=True),
                CustomPydanticSchemaPlugin(prefer_alias=True),
                PydanticDIPlugin(),
            ]
        )
        return app_config
