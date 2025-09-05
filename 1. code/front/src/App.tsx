import { useState } from 'react'
import { ThemeProvider } from '@mui/material/styles'
import { WelcomePage, DiaryPage } from '@/pages'
import { theme } from '@/theme'

function App() {
  const [currentPage, setCurrentPage] = useState<'welcome' | 'diary'>('welcome')

  const handleWelcomeComplete = () => {
    setCurrentPage('diary')
  }

  const handleBackToWelcome = () => {
    setCurrentPage('welcome')
  }

  return (
    <ThemeProvider theme={theme}>
      {currentPage === 'welcome' && (
        <WelcomePage onComplete={handleWelcomeComplete} />
      )}
      {currentPage === 'diary' && (
        <DiaryPage onBack={handleBackToWelcome} />
      )}
    </ThemeProvider>
  )
}

export default App