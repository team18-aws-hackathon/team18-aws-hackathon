import { MobileContainer, Header, Button } from '@/components';
import { PlayArrow, Download } from '@mui/icons-material';
import { useState, useEffect } from 'react';
import diaryImage004 from '@/assets/diary-20240901-004.png';
import diaryImage005 from '@/assets/diary-20240901-005.png';
import diaryImage006 from '@/assets/diary-20240901-003.png';

interface QuokkaResponsePageProps {
  onBack: () => void;
}

export const QuokkaResponsePage = ({ onBack }: QuokkaResponsePageProps) => {
  const [currentImage, setCurrentImage] = useState('');

  const images = [diaryImage004, diaryImage005, diaryImage006];

  useEffect(() => {
    const randomIndex = Math.floor(Math.random() * images.length);
    setCurrentImage(images[randomIndex]);
  }, []);

  const handleDownload = () => {
    // Download functionality will be implemented later
    console.log('Download image');
  };

  return (
    <MobileContainer>
      <Header title="Quokka Response" showBack onBack={onBack} />

      <div className="flex-1 p-6 flex flex-col bg-white">
        {/* Speech Bubble */}
        <div className="mb-8">
          <div className="bg-rose-400 rounded-2xl p-4 relative shadow-lg">
            {/* Audio Player */}
            <div className="flex items-center gap-3 mb-4">
              {/* Play Button Circle */}
              <div className="w-10 h-10 bg-white rounded-full flex items-center justify-center cursor-pointer">
                <PlayArrow className="text-black" sx={{ fontSize: 20 }} />
              </div>

              {/* Progress Bar */}
              <div className="flex-1 flex items-center gap-2">
                <span className="text-xs text-white">0:15</span>
                <div className="flex-1 h-1 bg-white bg-opacity-30 rounded-full">
                  <div className="w-1/3 h-full bg-black rounded-full"></div>
                </div>
                <span className="text-xs text-white">0:45</span>
              </div>
            </div>

            <p className="text-white text-base">
              Thank you for sharing your thoughts with me today! I can see that
              you're going through a lot right now. Remember that it's
              completely normal to feel this way, and you're doing great by
              taking the time to reflect on your emotions. Keep being kind to
              yourself! 🌟
            </p>
          </div>
        </div>

        {/* Quokka Character */}
        <div className="flex-1 flex items-center justify-center mb-8 px-4">
          <div className="w-full max-w-sm aspect-square bg-white rounded-full flex items-center justify-center">
            <img
              src={currentImage}
              alt="Quokka"
              className="w-48 h-48 object-contain"
            />
          </div>
        </div>

        {/* Download Button */}
        <Button
          fullWidth
          onClick={handleDownload}
          className="bg-accent-300 hover:bg-accent-500"
        >
          <Download sx={{ fontSize: 20 }} />
          Download Image
        </Button>
      </div>
    </MobileContainer>
  );
};
