import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';


const FileGrid = ({ files, viewMode, onFileSelect, onFileOpen, selectedFiles, onContextMenu }) => {
  const [draggedItem, setDraggedItem] = useState(null);

  const getFileIcon = (file) => {
    if (file?.type === 'folder') return 'Folder';
    
    const extension = file?.name?.split('.')?.pop()?.toLowerCase();
    switch (extension) {
      case 'txt': case'md':
        return 'FileText';
      case 'jpg': case'jpeg': case'png': case'gif':
        return 'Image';
      case 'mp3': case'wav': case'flac':
        return 'Music';
      case 'mp4': case'avi': case'mkv':
        return 'Video';
      case 'pdf':
        return 'FileText';
      case 'zip': case'rar': case'7z':
        return 'Archive';
      case 'js': case'jsx': case'ts': case'tsx':
        return 'Code';
      case 'html': case'css':
        return 'Code2';
      default:
        return 'File';
    }
  };

  const formatFileSize = (bytes) => {
    if (bytes === 0) return '0 B';
    const k = 1024;
    const sizes = ['B', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i))?.toFixed(1)) + ' ' + sizes?.[i];
  };

  const formatDate = (dateString) => {
    const date = new Date(dateString);
    return date?.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleFileClick = (file, event) => {
    if (event.ctrlKey || event.metaKey) {
      // Multi-select
      onFileSelect(file, true);
    } else {
      // Single select
      onFileSelect(file, false);
    }
  };

  const handleFileDoubleClick = (file) => {
    onFileOpen(file);
  };

  const handleDragStart = (e, file) => {
    setDraggedItem(file);
    e.dataTransfer.effectAllowed = 'move';
  };

  const handleDragOver = (e) => {
    e?.preventDefault();
    e.dataTransfer.dropEffect = 'move';
  };

  const handleDrop = (e, targetFile) => {
    e?.preventDefault();
    if (draggedItem && targetFile && targetFile?.type === 'folder' && draggedItem?.id !== targetFile?.id) {
      // Handle file move operation
      console.log(`Moving ${draggedItem?.name} to ${targetFile?.name}`);
    }
    setDraggedItem(null);
  };

  const handleContextMenu = (e, file) => {
    e?.preventDefault();
    onContextMenu(e, file);
  };

  if (viewMode === 'grid') {
    return (
      <div className="p-4 grid grid-cols-2 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-6 xl:grid-cols-8 gap-4">
        {files?.map((file) => (
          <div
            key={file?.id}
            className={`
              flex flex-col items-center p-3 rounded-lg cursor-pointer transition-colors
              ${selectedFiles?.includes(file?.id) 
                ? 'bg-primary/20 border border-primary/30' :'hover:bg-muted/20 border border-transparent'
              }
            `}
            draggable
            onDragStart={(e) => handleDragStart(e, file)}
            onDragOver={handleDragOver}
            onDrop={(e) => handleDrop(e, file)}
            onClick={(e) => handleFileClick(file, e)}
            onDoubleClick={() => handleFileDoubleClick(file)}
            onContextMenu={(e) => handleContextMenu(e, file)}
          >
            <Icon 
              name={getFileIcon(file)} 
              size={48} 
              className={`mb-2 ${file?.type === 'folder' ? 'text-accent' : 'text-muted-foreground'}`} 
            />
            <span className="text-sm text-center text-foreground truncate w-full" title={file?.name}>
              {file?.name}
            </span>
            {file?.type !== 'folder' && (
              <span className="text-xs text-muted-foreground mt-1">
                {formatFileSize(file?.size)}
              </span>
            )}
          </div>
        ))}
      </div>
    );
  }

  if (viewMode === 'list') {
    return (
      <div className="p-4 space-y-1">
        {files?.map((file) => (
          <div
            key={file?.id}
            className={`
              flex items-center p-2 rounded-md cursor-pointer transition-colors
              ${selectedFiles?.includes(file?.id) 
                ? 'bg-primary/20 border border-primary/30' :'hover:bg-muted/20'
              }
            `}
            draggable
            onDragStart={(e) => handleDragStart(e, file)}
            onDragOver={handleDragOver}
            onDrop={(e) => handleDrop(e, file)}
            onClick={(e) => handleFileClick(file, e)}
            onDoubleClick={() => handleFileDoubleClick(file)}
            onContextMenu={(e) => handleContextMenu(e, file)}
          >
            <Icon 
              name={getFileIcon(file)} 
              size={20} 
              className={`mr-3 flex-shrink-0 ${file?.type === 'folder' ? 'text-accent' : 'text-muted-foreground'}`} 
            />
            <span className="text-sm text-foreground flex-1 truncate">{file?.name}</span>
            {file?.type !== 'folder' && (
              <span className="text-xs text-muted-foreground ml-4">
                {formatFileSize(file?.size)}
              </span>
            )}
          </div>
        ))}
      </div>
    );
  }

  // Details view
  return (
    <div className="flex flex-col">
      {/* Header */}
      <div className="flex items-center p-2 bg-muted/10 border-b border-border text-xs font-medium text-muted-foreground">
        <div className="flex-1 px-2">Name</div>
        <div className="w-24 px-2">Size</div>
        <div className="w-32 px-2">Type</div>
        <div className="w-40 px-2">Modified</div>
      </div>
      {/* File List */}
      <div className="flex-1 overflow-y-auto">
        {files?.map((file) => (
          <div
            key={file?.id}
            className={`
              flex items-center p-2 border-b border-border/50 cursor-pointer transition-colors
              ${selectedFiles?.includes(file?.id) 
                ? 'bg-primary/20' :'hover:bg-muted/20'
              }
            `}
            draggable
            onDragStart={(e) => handleDragStart(e, file)}
            onDragOver={handleDragOver}
            onDrop={(e) => handleDrop(e, file)}
            onClick={(e) => handleFileClick(file, e)}
            onDoubleClick={() => handleFileDoubleClick(file)}
            onContextMenu={(e) => handleContextMenu(e, file)}
          >
            <div className="flex-1 flex items-center px-2">
              <Icon 
                name={getFileIcon(file)} 
                size={16} 
                className={`mr-2 flex-shrink-0 ${file?.type === 'folder' ? 'text-accent' : 'text-muted-foreground'}`} 
              />
              <span className="text-sm text-foreground truncate">{file?.name}</span>
            </div>
            <div className="w-24 px-2 text-sm text-muted-foreground">
              {file?.type === 'folder' ? '-' : formatFileSize(file?.size)}
            </div>
            <div className="w-32 px-2 text-sm text-muted-foreground capitalize">
              {file?.type === 'folder' ? 'Folder' : file?.name?.split('.')?.pop() || 'File'}
            </div>
            <div className="w-40 px-2 text-sm text-muted-foreground">
              {formatDate(file?.modified)}
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

export default FileGrid;