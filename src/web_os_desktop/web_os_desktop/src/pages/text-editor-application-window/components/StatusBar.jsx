import React from 'react';
import Icon from '../../../components/AppIcon';

const StatusBar = ({ 
  wordCount, 
  characterCount, 
  lineCount, 
  currentLine, 
  currentColumn, 
  isModified, 
  fileName, 
  encoding, 
  lineEnding,
  fontSize,
  zoomLevel
}) => {
  const getDocumentStatus = () => {
    if (isModified) {
      return { icon: 'Circle', text: 'Modified', color: 'text-warning' };
    }
    return { icon: 'CheckCircle', text: 'Saved', color: 'text-success' };
  };

  const status = getDocumentStatus();

  return (
    <div className="bg-surface border-t border-border h-6 flex items-center justify-between px-3 text-xs text-muted-foreground">
      {/* Left side - Document status and info */}
      <div className="flex items-center space-x-4">
        <div className={`flex items-center space-x-1 ${status.color}`}>
          <Icon name={status.icon} size={12} />
          <span>{status.text}</span>
        </div>
        
        <div className="flex items-center space-x-1">
          <Icon name="FileText" size={12} />
          <span>{fileName || 'Untitled'}</span>
        </div>

        <div className="flex items-center space-x-4">
          <span>Lines: {lineCount}</span>
          <span>Words: {wordCount}</span>
          <span>Characters: {characterCount}</span>
        </div>
      </div>
      {/* Right side - Position and settings */}
      <div className="flex items-center space-x-4">
        <span>Ln {currentLine}, Col {currentColumn}</span>
        
        <div className="flex items-center space-x-1">
          <Icon name="Type" size={12} />
          <span>{fontSize}px</span>
        </div>

        <div className="flex items-center space-x-1">
          <Icon name="ZoomIn" size={12} />
          <span>{zoomLevel}%</span>
        </div>

        <span>{encoding || 'UTF-8'}</span>
        <span>{lineEnding || 'LF'}</span>

        <div className="flex items-center space-x-1">
          <Icon name="Clock" size={12} />
          <span>{new Date()?.toLocaleTimeString('en-US', { 
            hour: '2-digit', 
            minute: '2-digit',
            hour12: true 
          })}</span>
        </div>
      </div>
    </div>
  );
};

export default StatusBar;