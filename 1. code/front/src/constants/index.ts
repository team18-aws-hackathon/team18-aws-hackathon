export const API_BASE_URL = 'https://your-api-gateway-url.com'; // 실제 URL로 변경

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
