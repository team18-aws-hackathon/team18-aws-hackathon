import { API_BASE_URL, API_ENDPOINTS, API_CONFIG } from '../constants';
import type {
  ApiResponse,
  TextRequest,
  ImageRequest,
  VoiceRequest,
  ProcessedResult,
} from '../types';

class ApiService {
  private async request<T>(endpoint: string, data: T): Promise<ApiResponse<T>> {
    try {
      const response = await fetch(`${API_BASE_URL}${endpoint}`, {
        method: 'POST',
        headers: API_CONFIG.headers,
        body: JSON.stringify(data),
      });

      const result = await response.json();
      return result;
    } catch (error) {
      return {
        success: false,
        error: error instanceof Error ? error.message : 'Unknown error',
      };
    }
  }

  async processText(data: TextRequest): Promise<ApiResponse<ProcessedResult>> {
    return this.request<ProcessedResult>(API_ENDPOINTS.TEXT, data);
  }

  async processImage(
    data: ImageRequest
  ): Promise<ApiResponse<ProcessedResult>> {
    return this.request<ProcessedResult>(API_ENDPOINTS.IMAGE, data);
  }

  async processVoice(
    data: VoiceRequest
  ): Promise<ApiResponse<ProcessedResult>> {
    return this.request<ProcessedResult>(API_ENDPOINTS.VOICE, data);
  }
}

export const apiService = new ApiService();
