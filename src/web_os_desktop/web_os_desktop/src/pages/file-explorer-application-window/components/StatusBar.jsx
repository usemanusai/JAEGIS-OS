import React from 'react';
import Icon from '../../../components/AppIcon';

const StatusBar = ({ 
  totalItems, 
  selectedItems, 
  totalSize, 
  currentPath, 
  isLoading,
  lastModified 
}) => {
  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB', 'TB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i))?.toFixed(1)) + ' ' + sizes?.[i];
  };

  const getStatusText = () => {
    if (isLoading) {
      return 'Loading...';
    }

    if (selectedItems > 0) {
      return `${selectedItems} of ${totalItems} items selected`;
    }

    return `${totalItems} items`;
  };

  const getSizeText = () => {
    if (totalSize > 0) {
      return formatFileSize(totalSize);
    }
    return '';
  };

  return (
    <div className="bg-surface border-t border-border px-4 py-2 flex items-center justify-between text-xs text-muted-foreground">
      {/* Left side - Item count and selection */}
      <div className="flex items-center space-x-4">
        <div className="flex items-center space-x-2">
          {isLoading && (
            <Icon name="Loader2" size={12} className="animate-spin" />
          )}
          <span>{getStatusText()}</span>
        </div>
        
        {totalSize > 0 && (
          <>
            <div className="w-px h-4 bg-border" />
            <span>{getSizeText()}</span>
          </>
        )}
      </div>
      {/* Right side - Path and last modified */}
      <div className="flex items-center space-x-4">
        {lastModified && (
          <>
            <span>Modified: {new Date(lastModified)?.toLocaleString()}</span>
            <div className="w-px h-4 bg-border" />
          </>
        )}
        
        <div className="flex items-center space-x-1">
          <Icon name="MapPin" size={12} />
          <span className="max-w-64 truncate" title={currentPath}>
            {currentPath}
          </span>
        </div>
      </div>
    </div>
  );
};

export default StatusBar;