import { createTheme } from '@mui/material/styles';

// TypeScript 타입 확장
declare module '@mui/material/styles' {
  interface Palette {
    beige: {
      100: string;
      200: string;
      300: string;
      400: string;
      500: string;
    };
    lime: {
      100: string;
      200: string;
      300: string;
      400: string;
      500: string;
    };
  }

  interface PaletteOptions {
    beige?: {
      100?: string;
      200?: string;
      300?: string;
      400?: string;
      500?: string;
    };
    lime?: {
      100?: string;
      200?: string;
      300?: string;
      400?: string;
      500?: string;
    };
  }
}

export const theme = createTheme({
  palette: {
    beige: {
      100: '#f5f5dc',
      200: '#f0e68c',
      300: '#ddbea9',
      400: '#d2b48c',
      500: '#D9965B',
    },
    lime: {
      100: '#ecfccb',
      200: '#d9f99d',
      300: '#bef264',
      400: '#a3e635',
      500: '#9ABF49',
    },
    grey: {
      300: '#d1d5db',
    },
  },
});
