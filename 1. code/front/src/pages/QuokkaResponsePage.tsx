import { MobileContainer, Header, Button } from '@/components';
import { PlayArrow, Pause, Download } from '@mui/icons-material';
import { useState, useEffect, useRef } from 'react';
import { useAppStore } from '@/store/appStore';

interface QuokkaResponsePageProps {
  onBack: () => void;
}

export const QuokkaResponsePage = ({ onBack }: QuokkaResponsePageProps) => {
  const { apiResults } = useAppStore();
  const currentImage = apiResults?.imageResult?.image_url || '';
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const [duration, setDuration] = useState(45);
  const audioRef = useRef<HTMLAudioElement>(null);

  console.log('API Results:', apiResults);

  // const images = [diaryImage004, diaryImage005, diaryImage006];

  // Use apiResults.textResult, apiResults.imageResult, apiResults.voiceResult
  // to display the API responses

  // useEffect(() => {
  //   const randomIndex = Math.floor(Math.random() * images.length);
  //   setCurrentImage(images[randomIndex]);
  // }, []);

  useEffect(() => {
    const audio = audioRef.current;
    if (!audio) return;

    const updateTime = () => setCurrentTime(audio.currentTime);
    const updateDuration = () => setDuration(audio.duration);
    const handleEnded = () => setIsPlaying(false);

    audio.addEventListener('timeupdate', updateTime);
    audio.addEventListener('loadedmetadata', updateDuration);
    audio.addEventListener('ended', handleEnded);

    return () => {
      audio.removeEventListener('timeupdate', updateTime);
      audio.removeEventListener('loadedmetadata', updateDuration);
      audio.removeEventListener('ended', handleEnded);
    };
  }, []);

  const togglePlay = () => {
    const audio = audioRef.current;
    if (!audio) return;

    if (isPlaying) {
      audio.pause();
    } else {
      audio.play();
    }
    setIsPlaying(!isPlaying);
  };

  const formatTime = (time: number) => {
    const minutes = Math.floor(time / 60);
    const seconds = Math.floor(time % 60);
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const handleDownload = () => {
    const link = document.createElement('a');
    link.href = currentImage;
    link.download = 'quokka-image.png';
    document.body.appendChild(link);
    link.click();
    document.body.removeChild(link);
  };

  return (
    <MobileContainer>
      <Header title="Quokka Response" showBack onBack={onBack} />

      <div className="flex-1 p-6 flex flex-col bg-white">
        {/* Speech Bubble */}
        <div className="mb-8">
          <div className="bg-rose-400 rounded-2xl p-4 relative shadow-lg">
            {/* Audio Player */}
            <audio ref={audioRef} preload="metadata">
              <source src="/path/to/audio.mp3" type="audio/mpeg" />
            </audio>
            <div className="flex items-center gap-3 mb-4">
              {/* Play Button Circle */}
              <div
                className="w-10 h-10 bg-white rounded-full flex items-center justify-center cursor-pointer"
                onClick={togglePlay}
              >
                {isPlaying ? (
                  <Pause className="text-black" sx={{ fontSize: 20 }} />
                ) : (
                  <PlayArrow className="text-black" sx={{ fontSize: 20 }} />
                )}
              </div>

              {/* Progress Bar */}
              <div className="flex-1 flex items-center gap-2">
                <span className="text-xs text-white">
                  {formatTime(currentTime)}
                </span>
                <div className="flex-1 h-1 bg-white bg-opacity-30 rounded-full">
                  <div
                    className="h-full bg-white rounded-full transition-all duration-100"
                    style={{
                      width: `${duration > 0 ? (currentTime / duration) * 100 : 0}%`,
                    }}
                  ></div>
                </div>
                <span className="text-xs text-white">
                  {formatTime(duration)}
                </span>
              </div>
            </div>

            <p className="text-white text-base">
              {apiResults?.textResult?.compliment}
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
        <Button fullWidth onClick={handleDownload} variant="rose">
          <Download sx={{ fontSize: 20 }} />
          Download Image
        </Button>
      </div>
    </MobileContainer>
  );
};
