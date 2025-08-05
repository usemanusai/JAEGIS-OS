import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import TerminalWindow from './components/TerminalWindow';
import Button from '../../components/ui/Button';
import Icon from '../../components/AppIcon';

const TerminalApplicationWindow = () => {
  const navigate = useNavigate();
  const [isMaximized, setIsMaximized] = useState(false);
  const [windowPosition, setWindowPosition] = useState({ x: 100, y: 100 });
  const [windowSize, setWindowSize] = useState({ width: 800, height: 500 });

  const handleClose = () => {
    navigate('/desktop-environment');
  };

  const handleMinimize = () => {
    // In a real implementation, this would minimize to taskbar
    console.log('Window minimized');
  };

  const handleMaximize = () => {
    setIsMaximized(!isMaximized);
  };

  const handleFocus = () => {
    // Bring window to front
    console.log('Window focused');
  };

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">
      {/* Space background with stars */}
      <div className="absolute inset-0 bg-black">
        <div className="absolute inset-0" style={{
          backgroundImage: `radial-gradient(2px 2px at 20px 30px, #eee, transparent),
                           radial-gradient(2px 2px at 40px 70px, rgba(255,255,255,0.8), transparent),
                           radial-gradient(1px 1px at 90px 40px, #fff, transparent),
                           radial-gradient(1px 1px at 130px 80px, rgba(255,255,255,0.6), transparent),
                           radial-gradient(2px 2px at 160px 30px, #ddd, transparent)`,
          backgroundRepeat: 'repeat',
          backgroundSize: '200px 100px'
        }} />
        
        {/* Galaxy overlay */}
        <div className="absolute inset-0 bg-gradient-to-br from-purple-900/20 via-blue-900/10 to-indigo-900/20" />
      </div>
      {/* Navigation Bar */}
      <div className="relative z-10 bg-slate-800/80 backdrop-blur-sm border-b border-slate-700 p-4">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <Button
              variant="ghost"
              onClick={() => navigate('/desktop-environment')}
              className="text-slate-300 hover:text-white"
            >
              <Icon name="ArrowLeft" size={16} className="mr-2" />
              Back to Desktop
            </Button>
            
            <div className="h-6 w-px bg-slate-600" />
            
            <div className="flex items-center space-x-2">
              <Icon name="Terminal" size={20} className="text-primary" />
              <span className="text-white font-medium">Terminal Application</span>
            </div>
          </div>

          <div className="flex items-center space-x-2">
            <Button
              variant="ghost"
              onClick={() => navigate('/app-launcher-menu')}
              className="text-slate-300 hover:text-white"
            >
              <Icon name="Grid3X3" size={16} className="mr-2" />
              App Launcher
            </Button>
            
            <Button
              variant="ghost"
              onClick={() => navigate('/system-info-application-window')}
              className="text-slate-300 hover:text-white"
            >
              <Icon name="Info" size={16} className="mr-2" />
              System Info
            </Button>
            
            <Button
              variant="ghost"
              onClick={() => navigate('/file-explorer-application-window')}
              className="text-slate-300 hover:text-white"
            >
              <Icon name="Folder" size={16} className="mr-2" />
              File Explorer
            </Button>
            
            <Button
              variant="ghost"
              onClick={() => navigate('/text-editor-application-window')}
              className="text-slate-300 hover:text-white"
            >
              <Icon name="FileText" size={16} className="mr-2" />
              Text Editor
            </Button>
          </div>
        </div>
      </div>
      {/* Terminal Window */}
      <div className="relative z-20 p-8">
        <TerminalWindow
          position={windowPosition}
          size={windowSize}
          isMaximized={isMaximized}
          onClose={handleClose}
          onMinimize={handleMinimize}
          onMaximize={handleMaximize}
          onFocus={handleFocus}
        />
      </div>
      {/* Help Panel */}
      <div className="absolute bottom-4 right-4 z-30">
        <div className="bg-slate-800/90 backdrop-blur-sm rounded-lg p-4 border border-slate-700 max-w-sm">
          <div className="flex items-center space-x-2 mb-3">
            <Icon name="HelpCircle" size={16} className="text-primary" />
            <span className="text-sm font-medium text-white">Terminal Help</span>
          </div>
          
          <div className="text-xs text-slate-300 space-y-1">
            <div>• Type 'help' for available commands</div>
            <div>• Use ↑↓ arrows for command history</div>
            <div>• Press Tab for command completion</div>
            <div>• Drag title bar to move window</div>
            <div>• Use window controls to minimize/maximize</div>
          </div>
        </div>
      </div>
      {/* Status Bar */}
      <div className="absolute bottom-0 left-0 right-0 z-10 bg-slate-800/80 backdrop-blur-sm border-t border-slate-700 px-4 py-2">
        <div className="flex items-center justify-between text-xs text-slate-400">
          <div className="flex items-center space-x-4">
            <span>WebOS Terminal v1.0.0</span>
            <span>•</span>
            <span>Ready</span>
          </div>
          
          <div className="flex items-center space-x-4">
            <span>{new Date()?.toLocaleTimeString()}</span>
            <span>•</span>
            <span>user@webos</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TerminalApplicationWindow;