import { MobileContainer, Header } from '@/components';

interface LoadingPageProps {
  onBack: () => void;
}

export const LoadingPage = ({ onBack }: LoadingPageProps) => {
  return (
    <MobileContainer>
      {/* 임시 헤더, 삭제 예정 */}
      <Header title="Loading" showBack onBack={onBack} />
      <div className="flex-1 flex flex-col items-center justify-center bg-gradient-to-r from-beige-300 to-beige-400 px-6">
        {/* Centered Quokka Face in White Circle */}
        <div className="mb-auto mt-auto flex flex-col items-center">
          <div className="w-32 h-32 bg-white rounded-full flex items-center justify-center mb-6">
            <div className="text-6xl">🐨</div>
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
