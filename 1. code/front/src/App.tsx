import { useState } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import { WelcomePage, DiaryPage, LoadingPage, QuokkaResponsePage } from '@/pages';
import { theme } from '@/theme';

function App() {
  const [currentPage, setCurrentPage] = useState<
    'welcome' | 'diary' | 'loading' | 'response'
  >('welcome');

  const handleWelcomeComplete = () => {
    setCurrentPage('diary');
  };

  const handleBackToWelcome = () => {
    setCurrentPage('welcome');
  };

  const handleSaveEntry = () => {
    setCurrentPage('loading');
  };

  const handleBackToDiary = () => {
    setCurrentPage('diary');
  };

  const handleLoadingComplete = () => {
    setCurrentPage('response');
  };

  const handleBackToLoading = () => {
    setCurrentPage('loading');
  };

  return (
    <ThemeProvider theme={theme}>
      {currentPage === 'welcome' && (
        <WelcomePage onComplete={handleWelcomeComplete} />
      )}
      {currentPage === 'diary' && (
        <DiaryPage onBack={handleBackToWelcome} onSaveEntry={handleSaveEntry} />
      )}
      {currentPage === 'loading' && (
        <LoadingPage onBack={handleBackToDiary} onComplete={handleLoadingComplete} />
      )}
      {currentPage === 'response' && (
        <QuokkaResponsePage onBack={handleBackToLoading} />
      )}
    </ThemeProvider>
  );
}

export default App;
