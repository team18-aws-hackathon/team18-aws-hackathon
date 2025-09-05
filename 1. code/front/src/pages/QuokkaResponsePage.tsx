import { MobileContainer, Header, Button } from '@/components'
import { PlayArrow, Download } from '@mui/icons-material'

interface QuokkaResponsePageProps {
  onBack: () => void
}

export const QuokkaResponsePage = ({ onBack }: QuokkaResponsePageProps) => {
  const handleDownload = () => {
    // Download functionality will be implemented later
    console.log('Download image')
  }

  return (
    <MobileContainer>
      <Header title="Quokka Response" showBack onBack={onBack} />
      
      <div className="flex-1 p-6 flex flex-col bg-white">
        {/* Speech Bubble */}
        <div className="mb-8">
          <div className="bg-beige-500 rounded-2xl p-4 relative shadow-lg">
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
              Thank you for sharing your thoughts with me today! I can see that you're going through a lot right now. 
              Remember that it's completely normal to feel this way, and you're doing great by taking the time to reflect on your emotions. 
              Keep being kind to yourself! 🌟
            </p>
          </div>
        </div>

        {/* Quokka Character */}
        <div className="flex-1 flex items-center justify-center mb-8 px-4">
          <div className="w-full max-w-sm aspect-square bg-lime-100 rounded-full flex items-center justify-center">
            <div className="text-9xl">🐨</div>
          </div>
        </div>

        {/* Download Button */}
        <Button fullWidth onClick={handleDownload} className="bg-lime-500 hover:bg-lime-600">
          <Download sx={{ fontSize: 20 }} />
          Download Image
        </Button>
      </div>
    </MobileContainer>
  )
}