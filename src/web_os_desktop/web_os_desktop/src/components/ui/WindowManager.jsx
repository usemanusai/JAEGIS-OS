import React, { createContext, useContext, useState, useCallback, useRef } from 'react';

const WindowManagerContext = createContext();

export const useWindowManager = () => {
  const context = useContext(WindowManagerContext);
  if (!context) {
    throw new Error('useWindowManager must be used within a WindowManagerProvider');
  }
  return context;
};

export const WindowManagerProvider = ({ children }) => {
  const [windows, setWindows] = useState([]);
  const [activeWindowId, setActiveWindowId] = useState(null);
  const nextZIndex = useRef(1000);

  const createWindow = useCallback((windowConfig) => {
    const windowId = `window-${Date.now()}-${Math.random()?.toString(36)?.substr(2, 9)}`;
    const newWindow = {
      id: windowId,
      title: windowConfig?.title,
      component: windowConfig?.component,
      position: windowConfig?.position || { x: 100, y: 100 },
      size: windowConfig?.size || { width: 800, height: 600 },
      zIndex: nextZIndex.current++,
      isMinimized: false,
      isMaximized: false,
      isDragging: false,
      isResizing: false,
      ...windowConfig
    };

    setWindows(prev => [...prev, newWindow]);
    setActiveWindowId(windowId);
    return windowId;
  }, []);

  const closeWindow = useCallback((windowId) => {
    setWindows(prev => prev?.filter(window => window.id !== windowId));
    setActiveWindowId(prev => prev === windowId ? null : prev);
  }, []);

  const focusWindow = useCallback((windowId) => {
    setWindows(prev => prev?.map(window => 
      window.id === windowId 
        ? { ...window, zIndex: nextZIndex.current++ }
        : window
    ));
    setActiveWindowId(windowId);
  }, []);

  const minimizeWindow = useCallback((windowId) => {
    setWindows(prev => prev?.map(window => 
      window.id === windowId 
        ? { ...window, isMinimized: !window.isMinimized }
        : window
    ));
  }, []);

  const maximizeWindow = useCallback((windowId) => {
    setWindows(prev => prev?.map(window => 
      window.id === windowId 
        ? { ...window, isMaximized: !window.isMaximized }
        : window
    ));
  }, []);

  const updateWindowPosition = useCallback((windowId, position) => {
    setWindows(prev => prev?.map(window => 
      window.id === windowId 
        ? { ...window, position }
        : window
    ));
  }, []);

  const updateWindowSize = useCallback((windowId, size) => {
    setWindows(prev => prev?.map(window => 
      window.id === windowId 
        ? { ...window, size }
        : window
    ));
  }, []);

  const getActiveWindows = useCallback(() => {
    return windows?.filter(window => !window.isMinimized);
  }, [windows]);

  const value = {
    windows,
    activeWindowId,
    createWindow,
    closeWindow,
    focusWindow,
    minimizeWindow,
    maximizeWindow,
    updateWindowPosition,
    updateWindowSize,
    getActiveWindows
  };

  return (
    <WindowManagerContext.Provider value={value}>
      {children}
    </WindowManagerContext.Provider>
  );
};

export default WindowManagerProvider;