import React from 'react';
import { useWindowManager } from './WindowManager';
import Icon from '../AppIcon';
import Button from './Button';

const AppLauncherMenu = ({ onClose }) => {
  const { createWindow } = useWindowManager();

  const applications = [
    {
      id: 'terminal',
      name: 'Terminal',
      icon: 'Terminal',
      description: 'Command line interface',
      component: 'TerminalWindow',
      category: 'System'
    },
    {
      id: 'file-explorer',
      name: 'File Explorer',
      icon: 'Folder',
      description: 'Browse files and folders',
      component: 'FileExplorerWindow',
      category: 'System'
    },
    {
      id: 'text-editor',
      name: 'Text Editor',
      icon: 'FileText',
      description: 'Edit text files',
      component: 'TextEditorWindow',
      category: 'Productivity'
    },
    {
      id: 'system-info',
      name: 'System Info',
      icon: 'Info',
      description: 'View system information',
      component: 'SystemInfoWindow',
      category: 'System'
    },
    {
      id: 'settings',
      name: 'Settings',
      icon: 'Settings',
      description: 'System preferences',
      component: 'SettingsWindow',
      category: 'System'
    },
    {
      id: 'calculator',
      name: 'Calculator',
      icon: 'Calculator',
      description: 'Basic calculator',
      component: 'CalculatorWindow',
      category: 'Utilities'
    },
    {
      id: 'image-viewer',
      name: 'Image Viewer',
      icon: 'Image',
      description: 'View images',
      component: 'ImageViewerWindow',
      category: 'Media'
    },
    {
      id: 'music-player',
      name: 'Music Player',
      icon: 'Music',
      description: 'Play audio files',
      component: 'MusicPlayerWindow',
      category: 'Media'
    }
  ];

  const categories = [...new Set(applications.map(app => app.category))];

  const handleAppLaunch = (app) => {
    const randomOffset = Math.random() * 50;
    createWindow({
      title: app?.name,
      component: app?.component,
      icon: app?.icon,
      position: { 
        x: 150 + randomOffset, 
        y: 150 + randomOffset 
      },
      size: { width: 800, height: 600 }
    });
    onClose();
  };

  const handleKeyDown = (event, app) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      handleAppLaunch(app);
    }
  };

  return (
    <div className="glass-strong rounded-lg p-6 w-[480px] max-h-[600px] animate-slide-up shadow-2xl">
      {/* Header */}
      <div className="mb-6">
        <div className="flex items-center justify-between mb-2">
          <h2 className="text-xl font-semibold text-foreground">Applications</h2>
          <Button
            variant="ghost"
            size="icon"
            onClick={onClose}
            className="w-8 h-8 hover:bg-muted/20"
          >
            <Icon name="X" size={16} />
          </Button>
        </div>
        <p className="text-sm text-muted-foreground">Launch your favorite applications</p>
      </div>
      {/* Search Bar */}
      <div className="mb-6">
        <div className="relative">
          <Icon 
            name="Search" 
            size={16} 
            className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground" 
          />
          <input
            type="text"
            placeholder="Search applications..."
            className="w-full pl-10 pr-4 py-2 bg-input border border-border rounded-md text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent"
          />
        </div>
      </div>
      {/* Applications Grid */}
      <div className="overflow-y-auto max-h-80">
        {categories?.map((category) => (
          <div key={category} className="mb-6">
            <h3 className="text-sm font-medium text-muted-foreground mb-3 uppercase tracking-wide">
              {category}
            </h3>
            <div className="grid grid-cols-2 gap-2">
              {applications?.filter(app => app?.category === category)?.map((app) => (
                  <Button
                    key={app?.id}
                    variant="ghost"
                    onClick={() => handleAppLaunch(app)}
                    onKeyDown={(e) => handleKeyDown(e, app)}
                    className="h-auto p-3 flex items-center space-x-3 hover:bg-muted/20 focus-ring text-left justify-start"
                  >
                    <div className="flex-shrink-0">
                      <Icon name={app?.icon} size={24} className="text-primary" />
                    </div>
                    <div className="flex-1 min-w-0">
                      <div className="text-sm font-medium text-foreground truncate">
                        {app?.name}
                      </div>
                      <div className="text-xs text-muted-foreground truncate">
                        {app?.description}
                      </div>
                    </div>
                  </Button>
                ))}
            </div>
          </div>
        ))}
      </div>
      {/* Footer */}
      <div className="mt-6 pt-4 border-t border-border">
        <div className="flex justify-between items-center">
          <div className="flex space-x-2">
            <Button 
              variant="ghost" 
              size="sm" 
              className="text-muted-foreground hover:text-foreground"
            >
              <Icon name="User" size={16} className="mr-2" />
              Profile
            </Button>
            <Button 
              variant="ghost" 
              size="sm" 
              className="text-muted-foreground hover:text-foreground"
            >
              <Icon name="Settings" size={16} className="mr-2" />
              Settings
            </Button>
          </div>
          <Button 
            variant="ghost" 
            size="sm" 
            className="text-muted-foreground hover:text-error"
          >
            <Icon name="Power" size={16} className="mr-2" />
            Power
          </Button>
        </div>
      </div>
    </div>
  );
};

export default AppLauncherMenu;