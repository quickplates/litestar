import docusauruseslint from "@docusaurus/eslint-plugin";
import { defineConfig, globalIgnores } from "@eslint/config-helpers";
import jseslint from "@eslint/js";
import perfectionisteslint from "eslint-plugin-perfectionist";
import reacteslint from "eslint-plugin-react";
import reacthookseslint from "eslint-plugin-react-hooks";
import globals from "globals";
import tseslint from "typescript-eslint";

const files = {
  ignored: ["build/", "node_modules/"],
  js: ["**/*.js", "**/*.cjs", "**/*.mjs", "**/*.jsx"],
  ts: ["**/*.ts", "**/*.cts", "**/*.mts", "**/*.tsx"],
};

export default defineConfig(
  // Global ignores
  globalIgnores(files.ignored),

  // JavaScript support
  {
    files: files.js,

    languageOptions: {
      globals: {
        // Support browser globals
        ...globals.browser,
      },

      parserOptions: {
        ecmaFeatures: {
          // Support JSX syntax
          jsx: true,
        },

        // Allow ESM syntax
        sourceType: "module",
      },
    },
  },

  // TypeScript support
  {
    files: files.ts,

    languageOptions: {
      globals: {
        // Support browser globals
        ...globals.browser,
      },

      parser: tseslint.parser,

      parserOptions: {
        ecmaFeatures: {
          // Support JSX syntax
          jsx: true,
        },

        // Allow ESM syntax
        sourceType: "module",
      },
    },
  },

  // JavaScript rules
  {
    extends: [jseslint.configs.recommended],

    files: files.js,

    rules: {
      // Allow empty block statements
      "no-empty": "off",

      // Allow empty destructuring patterns
      "no-empty-pattern": "off",
    },
  },

  // TypeScript rules
  {
    extends: [tseslint.configs.recommended, tseslint.configs.stylistic],

    files: files.ts,

    plugins: {
      "@typescript-eslint": tseslint.plugin,
    },

    rules: {
      // Use objects instead of records for empty types
      "@typescript-eslint/consistent-indexed-object-style": [
        "error",
        "index-signature",
      ],

      // Use types instead of interfaces
      "@typescript-eslint/consistent-type-definitions": ["error", "type"],

      // Use type imports
      "@typescript-eslint/consistent-type-imports": [
        "error",
        {
          disallowTypeAnnotations: false,
        },
      ],

      // Allow namespaces
      "@typescript-eslint/no-namespace": "off",

      // Allow some unused variables
      "@typescript-eslint/no-unused-vars": [
        "error",
        {
          args: "none",
          ignoreRestSiblings: true,
        },
      ],
    },
  },

  // Perfectionist rules
  {
    extends: [
      // This config already enables the plugin
      perfectionisteslint.configs["recommended-natural"],
    ],

    files: [...files.js, ...files.ts],

    rules: {
      // Don't sort module members
      "perfectionist/sort-modules": "off",
    },
  },

  // React rules
  {
    extends: [
      reacteslint.configs.flat.recommended,
      reacteslint.configs.flat["jsx-runtime"],
      reacthookseslint.configs.flat.recommended,
    ],

    files: [...files.js, ...files.ts],

    plugins: {
      react: reacteslint,
      "react-hooks": reacthookseslint,
    },

    rules: {
      // Don't check hook dependencies
      "react-hooks/exhaustive-deps": "off",

      // Allow mutating values returned from hooks
      "react-hooks/immutability": "off",

      // Don't check manual memoization preservation by React Compiler
      "react-hooks/preserve-manual-memoization": "off",
    },

    settings: {
      react: {
        // Automatically detect React version
        version: "detect",
      },
    },
  },

  // Docusaurus rules
  {
    extends: [{ rules: docusauruseslint.configs.recommended.rules }],

    files: [...files.js, ...files.ts],

    plugins: {
      "@docusaurus": docusauruseslint,
    },
  },
);
