export interface ApiResponse<T> {
  success: boolean;
  data?: T;
  message?: string;
  error?: string;
}

// 3개 API 모두 같은 텍스트를 받음
export interface TextRequest {
  text: string;
}

export interface ImageRequest {
  text: string; // 텍스트를 이미지로 처리
}

export interface VoiceRequest {
  text: string; // 텍스트를 음성으로 처리
}

// 각 API 응답 타입
export interface ProcessedResult {
  diary_id?: string;
  compliment?: string;
  quality_analysis?: {
    level?: string;
    message?: string;
  };
  error?: string;
  image_url?: string; // image API 응답에 포함
  audio_url?: string; // voice API 응답에 포함
}

// 전체 저장 결과
export interface SaveDiaryResult {
  textResult?: ProcessedResult;
  imageResult?: ProcessedResult;
  voiceResult?: ProcessedResult;
  errors?: string[];
}
