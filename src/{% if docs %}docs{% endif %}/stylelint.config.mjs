/** @type {import("stylelint").Config} */
export default {
  extends: [
    // Standard rules
    "stylelint-config-standard",

    // CSS Modules rules
    "stylelint-config-css-modules",

    // Alphabetical ordering rules
    "stylelint-config-alphabetical-order",
  ],

  rules: {
    // Disable custom property naming pattern enforcement
    "custom-property-pattern": null,
  },
};
