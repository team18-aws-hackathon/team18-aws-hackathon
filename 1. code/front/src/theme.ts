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
      300: string;
      400: string;
      500: string;
    };
    rose: {
      100: string;
      200: string;
      300: string;
      400: string;
      500: string;
      600: string;
      700: string;
    };
    accent: {
      100: string;
      200: string;
      300: string;
      400: string;
      500: string;
      600: string;
      700: string;
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
      300?: string;
      400?: string;
      500?: string;
    };
    rose?: {
      100?: string;
      200?: string;
      300?: string;
      400?: string;
      500?: string;
      600?: string;
      700?: string;
    };
    accent?: {
      100?: string;
      200?: string;
      300?: string;
      400?: string;
      500?: string;
      600?: string;
      700?: string;
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
});
