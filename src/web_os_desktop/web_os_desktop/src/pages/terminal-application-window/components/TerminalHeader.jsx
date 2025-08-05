import React from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const TerminalHeader = ({ onMinimize, onMaximize, onClose, isMaximized }) => {
  return (
    <div className="app-window-header bg-slate-800 border-b border-slate-700 h-10 flex items-center justify-between px-4">
      <div className="flex items-center space-x-2">
        <Icon name="Terminal" size={16} className="text-primary" />
        <span className="text-sm font-medium text-foreground">Terminal</span>
      </div>
      
      <div className="flex items-center space-x-1">
        <Button
          variant="ghost"
          size="icon"
          onClick={onMinimize}
          className="w-6 h-6 hover:bg-slate-700 text-muted-foreground hover:text-foreground"
        >
          <Icon name="Minus" size={12} />
        </Button>
        
        <Button
          variant="ghost"
          size="icon"
          onClick={onMaximize}
          className="w-6 h-6 hover:bg-slate-700 text-muted-foreground hover:text-foreground"
        >
          <Icon name={isMaximized ? "Minimize2" : "Maximize2"} size={12} />
        </Button>
        
        <Button
          variant="ghost"
          size="icon"
          onClick={onClose}
          className="w-6 h-6 hover:bg-red-600 text-muted-foreground hover:text-white"
        >
          <Icon name="X" size={12} />
        </Button>
      </div>
    </div>
  );
};

export default TerminalHeader;