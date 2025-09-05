/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'beige': {
          100: '#f5f5dc',
          200: '#f0e68c', 
          300: '#ddbea9',
          400: '#d2b48c',
          500: '#D9965B',
        },
        'lime': {
          300: '#bef264',
          400: '#a3e635',
          500: '#9ABF49',
        }
      }
    },
  },
  plugins: [],
}