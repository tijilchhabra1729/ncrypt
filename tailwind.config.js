module.exports = {
  future: {
    // removeDeprecatedGapUtilities: true,
    // purgeLayersByDefault: true,
  },
  purge: [],
  theme: {
    extend: {
      colors: {

        background: {
          // 'primary': '#edf2f7',
          // 'secondary': '#CBD5E0',
          // 'ternary': '#A0AEC0',
          'primary': '#EDF2F7',
          'secondary': '#3c3d40',
          'ternary': '#2d2e30',
          'textprime': '#718096',
          'textsecon': '#c9c9c9',
        },
        sidebar: {
          'primary': '#F7FAFC',
          'secondary': '#F7FAFC',
          'ternary': '#E6FFFA',
          'text': '#38B2AC',
        },
      },
    },
  },
  variants: {
    transitionProperty: ['responsive', 'hover', 'focus'],
  },
  plugins: [],
}
