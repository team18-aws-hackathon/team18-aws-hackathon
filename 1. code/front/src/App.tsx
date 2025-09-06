import { useState } from 'react';
import { ThemeProvider } from '@mui/material/styles';
import {
  WelcomePage,
  DiaryPage,
  LoadingPage,
  QuokkaResponsePage,
} from '@/pages';
import { theme } from '@/theme';

function App() {
  const [currentPage, setCurrentPage] = useState<
    'welcome' | 'diary' | 'loading' | 'response'
  >('welcome');
  const [userName, setUserName] = useState<string>('');

  const handleWelcomeComplete = (name: string) => {
    setUserName(name);
    setCurrentPage('diary');
  };

  const handleBackToWelcome = () => {
    setCurrentPage('welcome');
  };

  const handleSaveEntry = () => {
    setCurrentPage('loading');
  };

  const handleLoadingComplete = () => {
    setCurrentPage('response');
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
        <LoadingPage onComplete={handleLoadingComplete} />
      )}
      {currentPage === 'response' && (
        <QuokkaResponsePage onHome={handleBackToWelcome} userName={userName} />
      )}
    </ThemeProvider>
  );
}

export default App;
