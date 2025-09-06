import { useState } from 'react';
import { MobileContainer, Header, Button, TextArea } from '@/components';
import diaryImage from '@/assets/diary-20240901-004.png';

interface DiaryPageProps {
  onBack: () => void;
  onSaveEntry: () => void;
}

export const DiaryPage = ({ onBack, onSaveEntry }: DiaryPageProps) => {
  const [diaryText, setDiaryText] = useState('');

  return (
    <MobileContainer>
      <Header title="Diary" showBack onBack={onBack} />

      <div className="flex-1 p-6 flex flex-col bg-white">
        {/* Quokka Ask Section */}
        <div className="mb-6 flex items-start gap-3">
          {/* Quokka Avatar */}
          <div className="w-12 h-12 rounded-full bg-white border border-rose-400 flex items-center justify-center relative flex-shrink-0">
            <img
              src={diaryImage}
              alt="Quokka"
              className="w-10 h-10 object-contain"
            />
          </div>
          {/* Speech Bubble */}
          <div
            className="bg-white rounded-2xl p-4 relative flex-1"
            style={{ filter: 'drop-shadow(0 4px 6px rgba(0, 0, 0, 0.1))' }}
          >
            {/* Arrow pointing to quokka */}
            <div className="absolute left-0 top-[0.9rem] w-0 h-0 border-t-[12px] border-b-[12px] border-r-[12px] border-t-transparent border-b-transparent border-r-white -translate-x-3"></div>
            <span className="text-base text-gray-800">How are you today?</span>
          </div>
        </div>

        {/* Diary Text Area */}
        <div className="flex-1 mb-4">
          <TextArea
            placeholder="Tell me your stories..."
            value={diaryText}
            onChange={setDiaryText}
          />
        </div>

        {/* Save Button */}
        <Button 
          fullWidth 
          variant="rose" 
          onClick={() => diaryText.trim() && onSaveEntry()}
          className={!diaryText.trim() ? 'bg-white border-2 border-accent-400 text-accent-400 cursor-not-allowed' : ''}
        >
          Save Entry
        </Button>
      </div>
    </MobileContainer>
  );
};
