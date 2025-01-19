/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/*.html'
  ],
  theme: {
    extend: {
      fontFamily: {
        sfpro: ["sfpro","sans-serif"],
        sfprobold: ["sfpro-bold","sans-serif"],
        sfprolight: ["sfpro-light","sans-serif"],
      }
    },
  },
  plugins: [],
}

