module.exports = {
  purge: ['./src/**/*.{js,jsx,ts,tsx}', './public/index.html'],
  darkMode: false, // or 'media' or 'class'
  theme: {
    extend: {
      fontFamily: {
        'Raleway': ['Raleway Heavy']
      },
      colors : {
        'F6F3EF': '#F6F3EF',
        'bt-reg':'#FFDE59'
        
      },
      textColor: {
        '845A29':'#845A29'
      },
      width: {
        '3/7': '45%'
      }
    },

  },
  variants: {
    extend: {
      backgroundColor: ['focus','hover', 'active'],
      borderColor:['focus'],
      listStyleType: ['hover', 'focus'],
      outline:['focus', 'active'],
      animation: ['motion-safe'],
      scale: ['hover'],
      transform: ['hover'],
    },
  },
  plugins: ["macros"],
}
