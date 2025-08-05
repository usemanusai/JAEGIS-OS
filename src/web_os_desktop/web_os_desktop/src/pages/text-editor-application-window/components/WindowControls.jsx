import React from 'react';
import Button from '../../../components/ui/Button';
import Icon from '../../../components/AppIcon';

const WindowControls = ({ 
  title, 
  onMinimize, 
  onMaximize, 
  onClose, 
  isMaximized, 
  isModified 
}) => {
  return (
    <div className="bg-surface border-b border-border h-8 flex items-center justify-between px-3 select-none">
      {/* Window Title */}
      <div className="flex items-center space-x-2 flex-1">
        <Icon name="FileText" size={16} className="text-primary" />
        <span className="text-sm font-medium text-foreground truncate">
          {title}{isModified ? ' •' : ''}
        </span>
      </div>

      {/* Window Controls */}
      <div className="flex items-center space-x-1">
        <Button
          variant="ghost"
          size="icon"
          onClick={onMinimize}
          className="w-6 h-6 hover:bg-muted/20"
          title="Minimize"
        >
          <Icon name="Minus" size={12} />
        </Button>
        
        <Button
          variant="ghost"
          size="icon"
          onClick={onMaximize}
          className="w-6 h-6 hover:bg-muted/20"
          title={isMaximized ? "Restore" : "Maximize"}
        >
          <Icon name={isMaximized ? "Minimize2" : "Maximize2"} size={12} />
        </Button>
        
        <Button
          variant="ghost"
          size="icon"
          onClick={onClose}
          className="w-6 h-6 hover:bg-destructive/20 hover:text-destructive"
          title="Close"
        >
          <Icon name="X" size={12} />
        </Button>
      </div>
    </div>
  );
};

export default WindowControls;