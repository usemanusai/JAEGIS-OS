import React from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const WindowControls = ({ 
  onMinimize, 
  onMaximize, 
  onClose, 
  isMaximized,
  title = "File Explorer"
}) => {
  return (
    <div className="bg-muted/20 border-b border-border h-10 flex items-center justify-between px-4 select-none">
      {/* Window Title */}
      <div className="flex items-center space-x-2">
        <Icon name="Folder" size={16} className="text-primary" />
        <span className="text-sm font-medium text-foreground">{title}</span>
      </div>

      {/* Window Control Buttons */}
      <div className="flex items-center space-x-1">
        <Button
          variant="ghost"
          size="icon"
          onClick={onMinimize}
          className="w-8 h-8 hover:bg-muted/40"
          title="Minimize"
        >
          <Icon name="Minus" size={14} />
        </Button>
        
        <Button
          variant="ghost"
          size="icon"
          onClick={onMaximize}
          className="w-8 h-8 hover:bg-muted/40"
          title={isMaximized ? "Restore" : "Maximize"}
        >
          <Icon name={isMaximized ? "Square" : "Maximize2"} size={14} />
        </Button>
        
        <Button
          variant="ghost"
          size="icon"
          onClick={onClose}
          className="w-8 h-8 hover:bg-destructive/20 hover:text-destructive"
          title="Close"
        >
          <Icon name="X" size={14} />
        </Button>
      </div>
    </div>
  );
};

export default WindowControls;