import { useState } from 'react';
import { apiService } from '../services';
import type { ApiResponse } from '../types';

export const useApi = () => {
  const [loading, setLoading] = useState(false);

  const callApi = async <T>(apiCall: () => Promise<ApiResponse<T>>) => {
    setLoading(true);
    try {
      const result = await apiCall();
      return result;
    } finally {
      setLoading(false);
    }
  };

  return { loading, callApi };
};

// 개별 API 훅들
export const useTextApi = () => {
  const { loading, callApi } = useApi();
  
  const processText = (text: string) => 
    callApi(() => apiService.processText({ text }));

  return { processText, loading };
};

export const useImageApi = () => {
  const { loading, callApi } = useApi();
  
  const processImage = (image: string) => 
    callApi(() => apiService.processImage({ image }));

  return { processImage, loading };
};

export const useVoiceApi = () => {
  const { loading, callApi } = useApi();
  
  const processVoice = (audio: string) => 
    callApi(() => apiService.processVoice({ audio }));

  return { processVoice, loading };
};
