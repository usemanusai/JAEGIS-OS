import React, { useState, useRef, useEffect } from 'react';
import { useWindowManager } from '../../../components/ui/WindowManager';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import TerminalApplication from './applications/TerminalApplication';
import SystemInfoApplication from './applications/SystemInfoApplication';
import FileExplorerApplication from './applications/FileExplorerApplication';
import TextEditorApplication from './applications/TextEditorApplication';

const WindowRenderer = () => {
  const { windows, activeWindowId, focusWindow, closeWindow, minimizeWindow, maximizeWindow, updateWindowPosition, updateWindowSize } = useWindowManager();
  const [dragState, setDragState] = useState({});
  const [resizeState, setResizeState] = useState({});
  const dragRef = useRef({});
  const resizeRef = useRef({});

  const getApplicationComponent = (componentName) => {
    const components = {
      'TerminalWindow': TerminalApplication,
      'SystemInfoWindow': SystemInfoApplication,
      'FileExplorerWindow': FileExplorerApplication,
      'TextEditorWindow': TextEditorApplication
    };
    return components?.[componentName] || (() => <div className="p-4 text-muted-foreground">Application not found</div>);
  };

  const handleMouseDown = (e, windowId, action) => {
    e?.preventDefault();
    focusWindow(windowId);

    if (action === 'drag') {
      const window = windows?.find(w => w?.id === windowId);
      const rect = e?.currentTarget?.closest('.app-window')?.getBoundingClientRect();
      
      dragRef.current[windowId] = {
        startX: e?.clientX - window.position?.x,
        startY: e?.clientY - window.position?.y
      };

      setDragState(prev => ({ ...prev, [windowId]: true }));
    } else if (action === 'resize') {
      const window = windows?.find(w => w?.id === windowId);
      
      resizeRef.current[windowId] = {
        startX: e?.clientX,
        startY: e?.clientY,
        startWidth: window.size?.width,
        startHeight: window.size?.height
      };

      setResizeState(prev => ({ ...prev, [windowId]: true }));
    }
  };

  useEffect(() => {
    const handleMouseMove = (e) => {
      Object.keys(dragState)?.forEach(windowId => {
        if (dragState?.[windowId] && dragRef?.current?.[windowId]) {
          const newX = e?.clientX - dragRef?.current?.[windowId]?.startX;
          const newY = e?.clientY - dragRef?.current?.[windowId]?.startY;
          
          // Constrain to viewport
          const constrainedX = Math.max(0, Math.min(newX, window.innerWidth - 320));
          const constrainedY = Math.max(0, Math.min(newY, window.innerHeight - 240));
          
          updateWindowPosition(windowId, { x: constrainedX, y: constrainedY });
        }
      });

      Object.keys(resizeState)?.forEach(windowId => {
        if (resizeState?.[windowId] && resizeRef?.current?.[windowId]) {
          const deltaX = e?.clientX - resizeRef?.current?.[windowId]?.startX;
          const deltaY = e?.clientY - resizeRef?.current?.[windowId]?.startY;
          
          const newWidth = Math.max(320, resizeRef?.current?.[windowId]?.startWidth + deltaX);
          const newHeight = Math.max(240, resizeRef?.current?.[windowId]?.startHeight + deltaY);
          
          updateWindowSize(windowId, { width: newWidth, height: newHeight });
        }
      });
    };

    const handleMouseUp = () => {
      setDragState({});
      setResizeState({});
      dragRef.current = {};
      resizeRef.current = {};
    };

    if (Object.keys(dragState)?.length > 0 || Object.keys(resizeState)?.length > 0) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
    }

    return () => {
      document.removeEventListener('mousemove', handleMouseMove);
      document.removeEventListener('mouseup', handleMouseUp);
    };
  }, [dragState, resizeState, updateWindowPosition, updateWindowSize]);

  return (
    <>
      {windows?.filter(window => !window.isMinimized)?.map((window) => {
        const ApplicationComponent = getApplicationComponent(window.component);
        const isActive = activeWindowId === window.id;
        const isMaximized = window.isMaximized;

        const windowStyle = isMaximized
          ? {
              position: 'fixed',
              top: 0,
              left: 0,
              right: 0,
              bottom: '64px', // Account for taskbar
              width: 'auto',
              height: 'auto',
              zIndex: window.zIndex
            }
          : {
              position: 'absolute',
              left: window.position?.x,
              top: window.position?.y,
              width: window.size?.width,
              height: window.size?.height,
              zIndex: window.zIndex
            };

        return (
          <div
            key={window.id}
            className={`app-window ${isActive ? 'focused' : ''}`}
            style={windowStyle}
            onClick={() => focusWindow(window.id)}
          >
            {/* Window Header */}
            <div
              className="app-window-header cursor-move select-none"
              onMouseDown={(e) => !isMaximized && handleMouseDown(e, window.id, 'drag')}
            >
              <div className="flex items-center space-x-2">
                <Icon name={window.icon || "Square"} size={16} className="text-primary" />
                <span className="text-sm font-medium text-foreground truncate">
                  {window.title}
                </span>
              </div>
              
              <div className="flex items-center space-x-1">
                <Button
                  variant="ghost"
                  size="icon"
                  className="w-6 h-6 hover:bg-muted/20"
                  onClick={(e) => {
                    e?.stopPropagation();
                    minimizeWindow(window.id);
                  }}
                >
                  <Icon name="Minus" size={12} />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  className="w-6 h-6 hover:bg-muted/20"
                  onClick={(e) => {
                    e?.stopPropagation();
                    maximizeWindow(window.id);
                  }}
                >
                  <Icon name={isMaximized ? "Minimize2" : "Maximize2"} size={12} />
                </Button>
                <Button
                  variant="ghost"
                  size="icon"
                  className="w-6 h-6 hover:bg-destructive/20 hover:text-destructive"
                  onClick={(e) => {
                    e?.stopPropagation();
                    closeWindow(window.id);
                  }}
                >
                  <Icon name="X" size={12} />
                </Button>
              </div>
            </div>
            {/* Window Content */}
            <div className="flex-1 overflow-hidden bg-background">
              <ApplicationComponent windowId={window.id} />
            </div>
            {/* Resize Handle */}
            {!isMaximized && (
              <div
                className="absolute bottom-0 right-0 w-4 h-4 cursor-se-resize opacity-0 hover:opacity-100 transition-opacity"
                onMouseDown={(e) => handleMouseDown(e, window.id, 'resize')}
              >
                <div className="absolute bottom-1 right-1 w-2 h-2 border-r-2 border-b-2 border-muted-foreground/50" />
              </div>
            )}
          </div>
        );
      })}
    </>
  );
};

export default WindowRenderer;