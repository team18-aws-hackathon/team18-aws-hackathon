export const API_BASE_URL =
  'https://7jkqyuppw2.execute-api.us-east-1.amazonaws.com/dev'; // 실제 URL로 변경

export const API_ENDPOINTS = {
  TEXT: '/generate/text',
  IMAGE: '/generate/image',
  VOICE: '/generate/voice',
} as const;

export const API_CONFIG = {
  timeout: 30000,
  headers: {
    'Content-Type': 'application/json',
  },
} as const;
