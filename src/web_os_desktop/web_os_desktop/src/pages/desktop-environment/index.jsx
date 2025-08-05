import React, { useEffect, useState } from 'react';
import { WindowManagerProvider, useWindowManager } from '../../components/ui/WindowManager';
import TaskbarNavigation from '../../components/ui/TaskbarNavigation';
import DesktopBackground from './components/DesktopBackground';
import DesktopIcons from './components/DesktopIcons';
import WindowRenderer from './components/WindowRenderer';
import GlobalCommandPalette from '../../components/ui/GlobalCommandPalette';
import { appRegistry } from '../../services/AppRegistry';

// Component to initialize app registry with window manager
const AppRegistryInitializer = () => {
  const windowManager = useWindowManager();

  useEffect(() => {
    // Initialize app registry with window manager if not already done
    if (windowManager && !appRegistry.windowManager) {
      appRegistry.windowManager = windowManager;
      console.log('✅ App Registry connected to Window Manager');
    }
  }, [windowManager]);

  return null;
};

const DesktopEnvironment = () => {
  const [commandPaletteOpen, setCommandPaletteOpen] = useState(false);

  // Global keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      // Ctrl+Space or Cmd+Space to open command palette
      if ((e.ctrlKey || e.metaKey) && e.code === 'Space') {
        e.preventDefault();
        setCommandPaletteOpen(true);
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, []);

  return (
    <WindowManagerProvider>
      <AppRegistryInitializer />
      <div className="fixed inset-0 overflow-hidden bg-background">
        {/* Desktop Background */}
        <DesktopBackground />

        {/* Desktop Icons */}
        <DesktopIcons />

        {/* Window Renderer */}
        <WindowRenderer />

        {/* Taskbar */}
        <TaskbarNavigation />

        {/* Global Command Palette */}
        <GlobalCommandPalette
          isOpen={commandPaletteOpen}
          onClose={() => setCommandPaletteOpen(false)}
        />
      </div>
    </WindowManagerProvider>
  );
};

export default DesktopEnvironment;