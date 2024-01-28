export default {
  js2svg: {
    // Don't minify
    pretty: true,
  },
  plugins: [
    {
      name: "preset-default",
      params: {
        overrides: {
          // See: https://github.com/svg/svgo/issues/1128
          removeViewBox: false,
          // Sort attributes for consistency
          sortAttrs: true,
          // Remove off-canvas elements to reduce file size
          removeOffCanvasPaths: true,
          // Add a newline at the end of the file for consistency
          finalNewline: true,
        },
      },
    },
  ],
};
