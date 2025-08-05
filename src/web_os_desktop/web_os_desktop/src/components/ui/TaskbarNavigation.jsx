import React, { useState, useEffect } from 'react';
import { useWindowManager } from './WindowManager';
import Icon from '../AppIcon';
import Button from './Button';
import SystemTray from './SystemTray';
import { appRegistry } from '../../services/AppRegistry';

const TaskbarNavigation = () => {
  const { windows, activeWindowId, focusWindow, minimizeWindow, createWindow } = useWindowManager();
  const [currentTime, setCurrentTime] = useState(new Date());
  const [showAppLauncher, setShowAppLauncher] = useState(false);

  useEffect(() => {
    const timer = setInterval(() => {
      setCurrentTime(new Date());
    }, 1000);

    return () => clearInterval(timer);
  }, []);

  const handleStartButtonClick = () => {
    setShowAppLauncher(!showAppLauncher);
  };

  const handleWindowClick = (windowId) => {
    const window = windows?.find(w => w?.id === windowId);
    if (window.isMinimized) {
      minimizeWindow(windowId);
    }
    focusWindow(windowId);
  };

  const formatTime = (date) => {
    return date?.toLocaleTimeString('en-US', {
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    });
  };

  const formatDate = (date) => {
    return date?.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric'
    });
  };

  return (
    <>
      <div className="taskbar">
        {/* Start Button */}
        <Button
          variant="ghost"
          size="sm"
          onClick={handleStartButtonClick}
          className="mr-4 hover:bg-muted/20 text-foreground"
        >
          <Icon name="Grid3X3" size={20} className="mr-2" />
          <span className="hidden sm:inline">Start</span>
        </Button>

        {/* Active Windows */}
        <div className="flex-1 flex items-center space-x-2 overflow-x-auto">
          {windows?.map((window) => (
            <Button
              key={window.id}
              variant={activeWindowId === window.id ? "secondary" : "ghost"}
              size="sm"
              onClick={() => handleWindowClick(window.id)}
              className={`
                min-w-0 max-w-48 flex items-center space-x-2 px-3 py-2
                ${window.isMinimized ? 'opacity-60' : ''}
                ${activeWindowId === window.id ? 'bg-primary/20 border-primary/30' : 'hover:bg-muted/20'}
              `}
            >
              <Icon name={window.icon || "Square"} size={16} />
              <span className="truncate text-sm">{window.title}</span>
            </Button>
          ))}
        </div>

        {/* System Tray */}
        <div className="flex items-center space-x-4 ml-4">
          {/* Core Services Status */}
          <SystemTray />

          {/* System Status Icons */}
          <div className="hidden md:flex items-center space-x-2">
            <Button variant="ghost" size="icon" className="w-8 h-8">
              <Icon name="Wifi" size={16} />
            </Button>
            <Button variant="ghost" size="icon" className="w-8 h-8">
              <Icon name="Volume2" size={16} />
            </Button>
            <Button variant="ghost" size="icon" className="w-8 h-8">
              <Icon name="Battery" size={16} />
            </Button>
          </div>

          {/* Clock */}
          <div className="text-right text-sm text-foreground">
            <div className="font-medium">{formatTime(currentTime)}</div>
            <div className="text-xs text-muted-foreground hidden sm:block">
              {formatDate(currentTime)}
            </div>
          </div>

          {/* Notification Area */}
          <Button variant="ghost" size="icon" className="w-8 h-8">
            <Icon name="Bell" size={16} />
          </Button>
        </div>
      </div>
      {/* App Launcher Menu Overlay */}
      {showAppLauncher && (
        <>
          <div 
            className="fixed inset-0 z-[1999]" 
            onClick={() => setShowAppLauncher(false)}
          />
          <div className="fixed bottom-16 left-4 z-[2000]">
            <AppLauncherMenu onClose={() => setShowAppLauncher(false)} />
          </div>
        </>
      )}
    </>
  );
};

const AppLauncherMenu = ({ onClose }) => {
  const { createWindow } = useWindowManager();
  const [applications, setApplications] = useState([]);
  const [categories, setCategories] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('All');

  useEffect(() => {
    // Get applications from registry
    const registeredApps = appRegistry.getRegisteredApps();
    setApplications(registeredApps);

    // Get categories
    const appCategories = ['All', ...appRegistry.getCategories()];
    setCategories(appCategories);
  }, []);

  const filteredApplications = selectedCategory === 'All'
    ? applications
    : applications.filter(app => app.category === selectedCategory);

  const handleAppLaunch = async (app) => {
    try {
      await appRegistry.launchApp(app.id);
      onClose();
    } catch (error) {
      console.error('Failed to launch app:', error);
      // Fallback to basic window creation
      createWindow({
        title: app?.name,
        component: () => <div>Failed to load {app.name}</div>,
        icon: app?.icon,
        position: { x: 150 + Math.random() * 100, y: 150 + Math.random() * 100 },
        size: { width: 800, height: 600 }
      });
      onClose();
    }
  };

  return (
    <div className="glass-strong rounded-lg p-6 w-96 animate-slide-up">
      <div className="mb-4">
        <h2 className="text-lg font-semibold text-foreground mb-1">Applications</h2>
        <p className="text-sm text-muted-foreground">Launch your favorite apps</p>
      </div>

      {/* Category Filter */}
      <div className="mb-4">
        <div className="flex flex-wrap gap-2">
          {categories.map((category) => (
            <button
              key={category}
              onClick={() => setSelectedCategory(category)}
              className={`px-3 py-1 text-xs rounded-full transition-colors ${
                selectedCategory === category
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-700 text-gray-300 hover:bg-gray-600'
              }`}
            >
              {category}
            </button>
          ))}
        </div>
      </div>

      <div className="grid grid-cols-2 gap-3 max-h-80 overflow-y-auto">
        {filteredApplications?.map((app) => (
          <Button
            key={app?.id}
            variant="ghost"
            onClick={() => handleAppLaunch(app)}
            className="h-auto p-4 flex flex-col items-center space-y-2 hover:bg-muted/20 focus-ring"
          >
            <Icon name={app?.icon || "Square"} size={32} className="text-primary" />
            <div className="text-center">
              <div className="text-sm font-medium text-foreground">{app?.name}</div>
              <div className="text-xs text-muted-foreground">{app?.description}</div>
            </div>
          </Button>
        ))}
      </div>
      <div className="mt-4 pt-4 border-t border-border">
        <div className="flex justify-between">
          <Button variant="ghost" size="sm" className="text-muted-foreground">
            <Icon name="User" size={16} className="mr-2" />
            Profile
          </Button>
          <Button variant="ghost" size="sm" className="text-muted-foreground">
            <Icon name="Power" size={16} className="mr-2" />
            Power
          </Button>
        </div>
      </div>
    </div>
  );
};

export default TaskbarNavigation;