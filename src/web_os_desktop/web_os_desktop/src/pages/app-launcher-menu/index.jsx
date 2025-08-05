import React, { useState, useEffect, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import MenuHeader from './components/MenuHeader';
import SearchBar from './components/SearchBar';
import RecentApplications from './components/RecentApplications';
import ApplicationGrid from './components/ApplicationGrid';
import MenuFooter from './components/MenuFooter';

const AppLauncherMenu = () => {
  const navigate = useNavigate();
  const [searchTerm, setSearchTerm] = useState('');
  const [isVisible, setIsVisible] = useState(true);
  const menuRef = useRef(null);

  const applications = [
    {
      id: 'terminal',
      name: 'Terminal',
      icon: 'Terminal',
      description: 'Command line interface',
      category: 'System',
      route: '/terminal-application-window'
    },
    {
      id: 'file-explorer',
      name: 'File Explorer',
      icon: 'Folder',
      description: 'Browse files and folders',
      category: 'System',
      route: '/file-explorer-application-window'
    },
    {
      id: 'text-editor',
      name: 'Text Editor',
      icon: 'FileText',
      description: 'Edit text files',
      category: 'Productivity',
      route: '/text-editor-application-window'
    },
    {
      id: 'system-info',
      name: 'System Info',
      icon: 'Info',
      description: 'View system information',
      category: 'System',
      route: '/system-info-application-window'
    },
    {
      id: 'settings',
      name: 'Settings',
      icon: 'Settings',
      description: 'System preferences',
      category: 'System',
      route: '/desktop-environment'
    },
    {
      id: 'calculator',
      name: 'Calculator',
      icon: 'Calculator',
      description: 'Basic calculator',
      category: 'Utilities',
      route: '/desktop-environment'
    },
    {
      id: 'image-viewer',
      name: 'Image Viewer',
      icon: 'Image',
      description: 'View images',
      category: 'Media',
      route: '/desktop-environment'
    },
    {
      id: 'music-player',
      name: 'Music Player',
      icon: 'Music',
      description: 'Play audio files',
      category: 'Media',
      route: '/desktop-environment'
    }
  ];

  const recentApplications = [
    applications?.find(app => app?.id === 'terminal'),
    applications?.find(app => app?.id === 'file-explorer'),
    applications?.find(app => app?.id === 'text-editor')
  ]?.filter(Boolean);

  const handleAppLaunch = (app) => {
    console.log(`Launching application: ${app?.name}`);
    
    // Simulate window creation with random positioning
    const randomOffset = Math.random() * 50;
    const windowConfig = {
      id: `${app?.id}-${Date.now()}`,
      title: app?.name,
      component: app?.id,
      position: { 
        x: 150 + randomOffset, 
        y: 150 + randomOffset 
      },
      size: { width: 800, height: 600 },
      icon: app?.icon
    };

    // Store window config in localStorage for desktop environment
    const existingWindows = JSON.parse(localStorage.getItem('openWindows') || '[]');
    existingWindows?.push(windowConfig);
    localStorage.setItem('openWindows', JSON.stringify(existingWindows));

    // Navigate to the application route or back to desktop
    if (app?.route && app?.route !== '/desktop-environment') {
      navigate(app?.route);
    } else {
      navigate('/desktop-environment');
    }
    
    handleClose();
  };

  const handleClose = () => {
    setIsVisible(false);
    setTimeout(() => {
      navigate('/desktop-environment');
    }, 150);
  };

  const handleSearchChange = (value) => {
    setSearchTerm(value);
  };

  // Handle click outside to close menu
  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef?.current && !menuRef?.current?.contains(event.target)) {
        handleClose();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
    };
  }, []);

  // Handle keyboard navigation
  useEffect(() => {
    const handleKeyDown = (event) => {
      if (event.key === 'Escape') {
        handleClose();
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, []);

  return (
    <div className="fixed inset-0 bg-slate-900 z-50">
      {/* Background overlay */}
      <div 
        className="absolute inset-0 bg-black/50 backdrop-blur-sm"
        onClick={handleClose}
      />
      
      {/* Menu positioned in bottom-left corner */}
      <div className="absolute bottom-20 left-4 z-10">
        <div 
          ref={menuRef}
          className={`
            bg-slate-800/95 backdrop-blur-lg border border-slate-600/50 rounded-lg p-6 w-[480px] max-h-[600px] shadow-2xl
            ${isVisible ? 'animate-slide-up opacity-100' : 'opacity-0 translate-y-4'}
            transition-all duration-150 ease-out
          `}
        >
          <MenuHeader onClose={handleClose} />
          
          <SearchBar 
            searchTerm={searchTerm} 
            onSearchChange={handleSearchChange} 
          />
          
          {!searchTerm && (
            <RecentApplications 
              recentApps={recentApplications} 
              onAppLaunch={handleAppLaunch} 
            />
          )}
          
          <ApplicationGrid 
            applications={applications}
            onAppLaunch={handleAppLaunch}
            searchTerm={searchTerm}
          />
          
          <MenuFooter />
        </div>
      </div>

      {/* Mobile responsive adjustments */}
      <style jsx>{`
        @media (max-width: 640px) {
          .absolute.bottom-20.left-4 {
            position: fixed;
            bottom: 0;
            left: 0;
            right: 0;
            top: 0;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 1rem;
          }
          
          .w-\\[480px\\] {
            width: 100%;
            max-width: 400px;
          }
        }
      `}</style>
    </div>
  );
};

export default AppLauncherMenu;