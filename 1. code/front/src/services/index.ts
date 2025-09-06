// src/services/apiService.ts
import { SaveDiaryResult } from '@/types';

const API_BASE_URL =
  'https://7jkqyuppw2.execute-api.us-east-1.amazonaws.com/dev';

export const callAllApis = async (
  content: string,
  type: 'F' | 'T'
): Promise<SaveDiaryResult> => {
  try {
    // 1. 먼저 text API 호출
    const textResponse = await fetch(`${API_BASE_URL}/generate/text`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content, type }),
    });
    const textResult = await textResponse.json();

    // 2. diary_id가 있으면 image, voice API 호출
    const diaryId = textResult?.diary_id;
    const compliment = textResult?.compliment;

    if (!diaryId) {
      return {
        textResult,
        errors: ['diary_id not found in text response'],
      };
    }

    // 3. image와 voice API 동시 호출
    const [imageResult, voiceResult] = await Promise.allSettled([
      fetch(`${API_BASE_URL}/generate/image`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ diary_id: diaryId, compliment }),
      }).then((res) => res.json()),

      fetch(`${API_BASE_URL}/generate/voice`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ diary_id: diaryId, compliment }),
      }).then((res) => res.json()),
    ]);

    return {
      textResult,
      imageResult:
        imageResult.status === 'fulfilled' ? imageResult.value : undefined,
      voiceResult:
        voiceResult.status === 'fulfilled' ? voiceResult.value : undefined,
      errors: [
        ...(imageResult.status === 'rejected' ? [`Image API failed`] : []),
        ...(voiceResult.status === 'rejected' ? [`Voice API failed`] : []),
      ],
    };
  } catch (error) {
    return {
      errors: [`API call failed: ${error}`],
    };
  }
};
