import { FlatCompat } from "@eslint/eslintrc";
import eslint from "@eslint/js";
import perfectionisteslint from "eslint-plugin-perfectionist";
import globals from "globals";
import tseslint from "typescript-eslint";

const compat = new FlatCompat({
  baseDirectory: import.meta.dirname,
});

export default tseslint.config(
  // Use recommended eslint rules
  eslint.configs.recommended,

  // Use recommended type-checked typescript-eslint rules
  tseslint.configs.recommendedTypeChecked,

  // Use stylistic type-checked typescript-eslint rules
  tseslint.configs.stylisticTypeChecked,

  // Use recommended Docusaurus rules
  ...compat.extends("plugin:@docusaurus/recommended"),

  // Use recommended perfectionist rules
  perfectionisteslint.configs["recommended-alphabetical"],

  // Custom configuration
  {
    languageOptions: {
      globals: {
        // Support browser globals
        ...globals.browser,

        // Support ES2023 globals
        ...globals.es2023,

        // Support node globals
        ...globals.node,
      },

      parserOptions: {
        // Use project service to build type information
        // Needed for type-aware linting
        projectService: true,

        // Allow ES2022 syntax
        sourceType: "module",

        // Set the root directory of the project
        // Needed for type-aware linting
        tsconfigRootDir: import.meta.dirname,
      },
    },

    rules: {
      // Use objects instead of records for empty types
      "@typescript-eslint/consistent-indexed-object-style": [
        "error",
        "index-signature",
      ],

      // Use types instead of interfaces
      "@typescript-eslint/consistent-type-definitions": ["error", "type"],

      // Allow promises in callbacks
      "@typescript-eslint/no-misused-promises": [
        "error",
        {
          checksVoidReturn: false,
        },
      ],

      // Allow nullish coalescing operator for primitive types
      "@typescript-eslint/prefer-nullish-coalescing": [
        "error",
        {
          ignorePrimitives: true,
        },
      ],

      // Allow async functions without await
      "@typescript-eslint/require-await": "off",

      // Skip checking whether static methods are bound
      "@typescript-eslint/unbound-method": [
        "error",
        {
          ignoreStatic: true,
        },
      ],

      // Allow anonymous default exports
      "import/no-anonymous-default-export": "off",

      // Allow empty block statements
      "no-empty": "off",

      // Allow empty destructuring patterns
      "no-empty-pattern": "off",

      // Don't sort module members
      "perfectionist/sort-modules": "off",
    },
  },
);
