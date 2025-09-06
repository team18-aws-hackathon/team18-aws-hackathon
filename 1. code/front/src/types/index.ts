// API 요청/응답 타입 정의
export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

// 3개 API 요청 타입
export interface TextRequest {
  text: string;
}

export interface ImageRequest {
  image: string; // base64 또는 URL
}

export interface VoiceRequest {
  audio: string; // base64 또는 URL
}

// 응답 데이터 타입 (필요에 따라 수정)
export interface ProcessedResult {
  result: string;
  timestamp: string;
}
