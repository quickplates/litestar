import docusauruseslint from "@docusaurus/eslint-plugin";
import eslint from "@eslint/js";
import perfectionisteslint from "eslint-plugin-perfectionist";
import globals from "globals";
import tseslint from "typescript-eslint";

export default tseslint.config(
  // Use recommended eslint rules
  eslint.configs.recommended,

  // Use strict type-checked typescript-eslint rules
  tseslint.configs.strictTypeChecked,

  // Use stylistic type-checked typescript-eslint rules
  tseslint.configs.stylisticTypeChecked,

  // Use recommended perfectionist rules
  perfectionisteslint.configs["recommended-alphabetical"],

  // Custom configuration
  {
    languageOptions: {
      globals: {
        // Support browser globals
        ...globals.browser,

        // Support node globals
        ...globals.node,
      },

      parserOptions: {
        // Use project service to build type information
        // Needed for type-aware linting
        projectService: true,

        // Set the root directory of the project
        // Needed for type-aware linting
        tsconfigRootDir: import.meta.dirname,
      },
    },

    plugins: {
      // Enable docusaurus plugin
      "@docusaurus": docusauruseslint,
    },

    rules: {
      // Use recommended docusaurus rules
      ...docusauruseslint.configs.recommended.rules,
    },
  },
);
