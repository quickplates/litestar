module.exports = {
  env: {
    // Support browser globals
    browser: true,

    // Support node globals
    node: true,
  },

  extends: [
    // Use recommended eslint rules
    "eslint:recommended",

    // Use recommended typescript-eslint rules
    "plugin:@typescript-eslint/recommended",

    // Use recommended docusaurus rules
    "plugin:@docusaurus/recommended",

    // Turn off rules that might conflict with Prettier
    "prettier",
  ],

  // Use typescript-eslint parser
  parser: "@typescript-eslint/parser",

  plugins: [
    // Support typescript-eslint
    "@typescript-eslint",
  ],

  // Ignore configuration files in directories above this one
  root: true,
};
