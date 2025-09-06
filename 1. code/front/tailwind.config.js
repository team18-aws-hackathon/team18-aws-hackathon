/** @type {import('tailwindcss').Config} */
export default {
  content: ['./index.html', './src/**/*.{js,ts,jsx,tsx}'],
  theme: {
    extend: {
      colors: {
        beige: {
          100: '#f5f5dc',
          200: '#f0e68c',
          300: '#ddbea9',
          400: '#d2b48c',
          500: '#D9965B',
        },
        lime: {
          300: '#bef264',
          400: '#a3e635',
          500: '#9ABF49',
        },
        rose: {
          100: '#F5E5E5',
          200: '#EDCACA',
          300: '#E5AFAF',
          400: '#E19F9F', //main
          500: '#D88A8A',
          600: '#CF7575',
          700: '#C66060',
        },
        accent: {
          100: '#E8D1D2',
          200: '#D1A3A5',
          300: '#C87B7D',
          400: '#B85D5E', //main
          500: '#A54F50',
          600: '#924142',
          700: '#7F3334',
        },
      },
    },
  },
  plugins: [],
};
