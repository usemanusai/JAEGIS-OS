import React from 'react';
import { useWindowManager } from './WindowManager';
import Icon from '../AppIcon';
import Button from './Button';

const DesktopIconGrid = () => {
  const { createWindow } = useWindowManager();

  const desktopApps = [
    {
      id: 'terminal',
      name: 'Terminal',
      icon: 'Terminal',
      component: 'TerminalWindow',
      size: { width: 800, height: 500 }
    },
    {
      id: 'file-explorer',
      name: 'File Explorer',
      icon: 'Folder',
      component: 'FileExplorerWindow',
      size: { width: 900, height: 600 }
    },
    {
      id: 'text-editor',
      name: 'Text Editor',
      icon: 'FileText',
      component: 'TextEditorWindow',
      size: { width: 800, height: 600 }
    },
    {
      id: 'system-info',
      name: 'System Info',
      icon: 'Info',
      component: 'SystemInfoWindow',
      size: { width: 700, height: 500 }
    }
  ];

  const handleAppLaunch = (app) => {
    const randomOffset = Math.random() * 50;
    createWindow({
      title: app?.name,
      component: app?.component,
      icon: app?.icon,
      position: { 
        x: 100 + randomOffset, 
        y: 100 + randomOffset 
      },
      size: app?.size
    });
  };

  const handleDoubleClick = (app) => {
    handleAppLaunch(app);
  };

  return (
    <div className="fixed top-4 right-4 z-10 w-32">
      <div className="space-y-4">
        {desktopApps?.map((app) => (
          <div
            key={app?.id}
            className="flex flex-col items-center space-y-2 group cursor-pointer"
            onDoubleClick={() => handleDoubleClick(app)}
          >
            <Button
              variant="ghost"
              size="icon"
              className="w-16 h-16 hover-scale click-scale bg-surface/50 hover:bg-surface/80 border border-border/50 group-hover:border-primary/30 transition-all duration-150"
              onClick={() => handleAppLaunch(app)}
            >
              <Icon 
                name={app?.icon} 
                size={28} 
                className="text-primary group-hover:text-primary/80" 
              />
            </Button>
            <span className="text-xs text-center text-foreground/90 group-hover:text-foreground max-w-full truncate px-1">
              {app?.name}
            </span>
          </div>
        ))}

        {/* Recycle Bin */}
        <div className="flex flex-col items-center space-y-2 group cursor-pointer mt-8">
          <Button
            variant="ghost"
            size="icon"
            className="w-16 h-16 hover-scale click-scale bg-surface/50 hover:bg-surface/80 border border-border/50 group-hover:border-muted/30 transition-all duration-150"
          >
            <Icon 
              name="Trash2" 
              size={28} 
              className="text-muted-foreground group-hover:text-muted" 
            />
          </Button>
          <span className="text-xs text-center text-muted-foreground group-hover:text-muted max-w-full truncate px-1">
            Recycle Bin
          </span>
        </div>
      </div>
    </div>
  );
};

export default DesktopIconGrid;