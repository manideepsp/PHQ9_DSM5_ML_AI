import React from 'react';
import { Button } from './ui/button';
import { Heart, Menu, User, Home, FileText, Settings, LogIn, LogOut } from 'lucide-react';
import { useAuth } from '../contexts/AuthContext';

interface NavbarProps {
  onShowLogin?: () => void;
  onShowRegister?: () => void;
}

export function Navbar({ onShowLogin, onShowRegister }: NavbarProps) {
  const { user, isAuthenticated, logout } = useAuth();

  const handleLogout = () => {
    logout();
  };

  return (
    <nav className="bg-blue-600 shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between items-center h-16">
          {/* Logo and Brand */}
          <div className="flex items-center space-x-3">
            <div className="bg-blue-500 p-2 rounded-full">
              <Heart className="h-6 w-6 text-white" />
            </div>
            <div>
              <h1 className="text-white text-xl font-semibold">MindCare</h1>
              <p className="text-white/80 text-sm">Mental Health Assessment</p>
            </div>
          </div>

          {/* Desktop Navigation */}
          <div className="hidden md:flex items-center space-x-6">
            {isAuthenticated ? (
              <>
                <Button variant="ghost" className="text-white hover:bg-blue-500 hover:text-white">
                  <Home className="h-4 w-4 mr-2" />
                  Home
                </Button>
                <Button variant="ghost" className="text-white hover:bg-blue-500 hover:text-white">
                  <FileText className="h-4 w-4 mr-2" />
                  Assessments
                </Button>
                <Button variant="ghost" className="text-white hover:bg-blue-500 hover:text-white">
                  <Settings className="h-4 w-4 mr-2" />
                  Settings
                </Button>
                <div className="flex items-center space-x-3">
                  <span className="text-white/90 text-sm">
                    Welcome, {user?.name || user?.username}
                  </span>
                  <Button 
                    variant="ghost" 
                    onClick={handleLogout}
                    className="text-white hover:bg-blue-500 hover:text-white"
                  >
                    <LogOut className="h-4 w-4 mr-2" />
                    Logout
                  </Button>
                </div>
              </>
            ) : (
              <div className="flex items-center space-x-3">
                <Button 
                  variant="ghost" 
                  onClick={onShowLogin}
                  className="text-white hover:bg-blue-500 hover:text-white"
                >
                  <LogIn className="h-4 w-4 mr-2" />
                  Login
                </Button>
                <Button 
                  onClick={onShowRegister}
                  className="bg-blue-500 hover:bg-blue-400 text-white border-0 shadow-lg transform transition-all duration-200 hover:scale-105"
                >
                  <User className="h-4 w-4 mr-2" />
                  Register
                </Button>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden">
            <Button variant="ghost" size="sm" className="text-white hover:bg-blue-500">
              <Menu className="h-6 w-6" />
            </Button>
          </div>
        </div>
      </div>
    </nav>
  );
}