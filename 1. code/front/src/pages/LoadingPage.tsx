import { useEffect } from 'react';
import { MobileContainer } from '@/components';
import diaryImage from '@/assets/diary-20240901-004.png';

interface LoadingPageProps {
  onComplete: () => void;
}

export const LoadingPage = ({ onComplete }: LoadingPageProps) => {
  useEffect(() => {
    const timer = setTimeout(() => {
      onComplete();
    }, 3000);

    return () => clearTimeout(timer);
  }, [onComplete]);
  return (
    <MobileContainer>
      <div className="flex-1 flex flex-col items-center justify-center bg-gradient-to-r from-rose-300 to-rose-500 px-6">
        {/* Centered Quokka Face in White Circle */}
        <div className="mb-auto mt-auto flex flex-col items-center">
          <div className="w-40 h-40 bg-white rounded-full flex items-center justify-center mb-6">
            <img
              src={diaryImage}
              alt="Quokka"
              className="w-32 h-32 object-contain"
            />
          </div>

          {/* Loading Dots */}
          <div className="flex gap-2">
            <div className="w-3 h-3 bg-white rounded-full animate-bounce"></div>
            <div
              className="w-3 h-3 bg-white rounded-full animate-bounce"
              style={{ animationDelay: '0.1s' }}
            ></div>
            <div
              className="w-3 h-3 bg-white rounded-full animate-bounce"
              style={{ animationDelay: '0.2s' }}
            ></div>
          </div>
        </div>

        {/* Bottom Message */}
        <div className="mb-8">
          <p className="text-white text-xl text-center font-medium">
            So that happened…
          </p>
        </div>
      </div>
    </MobileContainer>
  );
};
