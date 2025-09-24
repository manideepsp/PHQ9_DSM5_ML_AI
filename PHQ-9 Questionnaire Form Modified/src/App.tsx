import React, { useState } from 'react';
import { PHQ9Form } from './components/PHQ9Form';
import { Navbar } from './components/Navbar';
import { LoginForm } from './components/LoginForm';
import { RegistrationForm } from './components/RegistrationForm';
import { AuthProvider, useAuth } from './contexts/AuthContext';

type ViewType = 'home' | 'login' | 'register';

function AppContent() {
  const [currentView, setCurrentView] = useState<ViewType>('home');
  const { isAuthenticated } = useAuth();

  // Reset to home view when user logs in
  React.useEffect(() => {
    if (isAuthenticated && (currentView === 'login' || currentView === 'register')) {
      setCurrentView('home');
    }
  }, [isAuthenticated, currentView]);

  const renderCurrentView = () => {
    if (!isAuthenticated) {
      switch (currentView) {
        case 'login':
          return <LoginForm onSwitchToRegister={() => setCurrentView('register')} />;
        case 'register':
          return <RegistrationForm onSwitchToLogin={() => setCurrentView('login')} />;
        default:
          return (
            <div className="min-h-screen bg-blue-50">
              <Navbar 
                onShowLogin={() => setCurrentView('login')}
                onShowRegister={() => setCurrentView('register')}
              />
              <main className="py-8">
                <div className="max-w-4xl mx-auto p-6 text-center">
                  <div className="bg-white rounded-lg shadow-2xl p-12">
                    <h1 className="text-3xl text-gray-800 mb-6">Welcome to MindCare</h1>
                    <p className="text-lg text-gray-600 mb-8">
                      Access mental health assessments and tools to support your wellbeing.
                    </p>
                    <p className="text-gray-500">
                      Please log in or register to access the PHQ-9 Depression Screening Questionnaire and other features.
                    </p>
                  </div>
                </div>
              </main>
              
              {/* Decorative background elements */}
              <div className="fixed inset-0 pointer-events-none overflow-hidden -z-10">
                <div className="absolute top-10 left-10 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse"></div>
                <div className="absolute top-40 right-10 w-72 h-72 bg-blue-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-2000"></div>
                <div className="absolute bottom-10 left-20 w-72 h-72 bg-blue-100 rounded-full mix-blend-multiply filter blur-xl opacity-25 animate-pulse animation-delay-4000"></div>
                <div className="absolute bottom-40 right-20 w-72 h-72 bg-blue-400 rounded-full mix-blend-multiply filter blur-xl opacity-15 animate-pulse animation-delay-6000"></div>
              </div>
            </div>
          );
      }
    }

    // Authenticated user views
    return (
      <div className="min-h-screen bg-blue-50">
        <Navbar />
        <main className="py-8">
          <PHQ9Form />
        </main>
        
        {/* Decorative background elements */}
        <div className="fixed inset-0 pointer-events-none overflow-hidden -z-10">
          <div className="absolute top-10 left-10 w-72 h-72 bg-blue-200 rounded-full mix-blend-multiply filter blur-xl opacity-30 animate-pulse"></div>
          <div className="absolute top-40 right-10 w-72 h-72 bg-blue-300 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse animation-delay-2000"></div>
          <div className="absolute bottom-10 left-20 w-72 h-72 bg-blue-100 rounded-full mix-blend-multiply filter blur-xl opacity-25 animate-pulse animation-delay-4000"></div>
          <div className="absolute bottom-40 right-20 w-72 h-72 bg-blue-400 rounded-full mix-blend-multiply filter blur-xl opacity-15 animate-pulse animation-delay-6000"></div>
        </div>
      </div>
    );
  };

  return renderCurrentView();
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}