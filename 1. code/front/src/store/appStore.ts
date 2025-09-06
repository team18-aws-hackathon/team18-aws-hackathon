import { create } from 'zustand';
import { SaveDiaryResult } from '@/types';

interface AppState {
  selectedQuokka: 'F' | 'T';
  diaryText: string;
  apiResults: SaveDiaryResult | null;
  setSelectedQuokka: (type: 'F' | 'T') => void;
  setDiaryText: (text: string) => void;
  setApiResults: (results: SaveDiaryResult) => void;
}

export const useAppStore = create<AppState>((set) => ({
  selectedQuokka: 'F',
  diaryText: '',
  apiResults: null,
  setSelectedQuokka: (type) => set({ selectedQuokka: type }),
  setDiaryText: (text) => set({ diaryText: text }),
  setApiResults: (results) => set({ apiResults: results }),
}));
