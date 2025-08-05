import React, { useState, useEffect } from 'react';
import Icon from '../../../../components/AppIcon';
import Button from '../../../../components/ui/Button';


const FileExplorerApplication = ({ windowId }) => {
  const [currentPath, setCurrentPath] = useState('/home/user');
  const [selectedItems, setSelectedItems] = useState([]);
  const [viewMode, setViewMode] = useState('list'); // 'list' or 'grid'
  const [sortBy, setSortBy] = useState('name');
  const [sortOrder, setSortOrder] = useState('asc');

  const mockFileSystem = {
    '/': {
      type: 'folder',
      name: 'Root',
      children: ['home', 'usr', 'var', 'etc']
    },
    '/home': {
      type: 'folder',
      name: 'home',
      children: ['user']
    },
    '/home/user': {
      type: 'folder',
      name: 'user',
      children: ['Documents', 'Downloads', 'Pictures', 'Videos', 'Desktop', 'Music']
    },
    '/home/user/Documents': {
      type: 'folder',
      name: 'Documents',
      children: ['report.pdf', 'notes.txt', 'presentation.pptx', 'Projects']
    },
    '/home/user/Downloads': {
      type: 'folder',
      name: 'Downloads',
      children: ['installer.exe', 'image.jpg', 'archive.zip']
    },
    '/home/user/Pictures': {
      type: 'folder',
      name: 'Pictures',
      children: ['vacation.jpg', 'family.png', 'screenshot.png']
    },
    '/home/user/Videos': {
      type: 'folder',
      name: 'Videos',
      children: ['movie.mp4', 'tutorial.avi']
    },
    '/home/user/Desktop': {
      type: 'folder',
      name: 'Desktop',
      children: ['shortcut.lnk', 'readme.txt']
    },
    '/home/user/Music': {
      type: 'folder',
      name: 'Music',
      children: ['song1.mp3', 'song2.wav', 'playlist.m3u']
    }
  };

  const mockFiles = {
    'report.pdf': { type: 'file', size: '2.4 MB', modified: '2024-07-30', icon: 'FileText' },
    'notes.txt': { type: 'file', size: '1.2 KB', modified: '2024-07-31', icon: 'FileText' },
    'presentation.pptx': { type: 'file', size: '5.8 MB', modified: '2024-07-29', icon: 'Presentation' },
    'installer.exe': { type: 'file', size: '45.2 MB', modified: '2024-07-28', icon: 'Download' },
    'image.jpg': { type: 'file', size: '3.1 MB', modified: '2024-07-31', icon: 'Image' },
    'archive.zip': { type: 'file', size: '12.5 MB', modified: '2024-07-30', icon: 'Archive' },
    'vacation.jpg': { type: 'file', size: '4.2 MB', modified: '2024-07-25', icon: 'Image' },
    'family.png': { type: 'file', size: '2.8 MB', modified: '2024-07-26', icon: 'Image' },
    'screenshot.png': { type: 'file', size: '1.5 MB', modified: '2024-07-31', icon: 'Image' },
    'movie.mp4': { type: 'file', size: '1.2 GB', modified: '2024-07-20', icon: 'Video' },
    'tutorial.avi': { type: 'file', size: '856 MB', modified: '2024-07-22', icon: 'Video' },
    'shortcut.lnk': { type: 'file', size: '2 KB', modified: '2024-07-31', icon: 'Link' },
    'readme.txt': { type: 'file', size: '856 B', modified: '2024-07-31', icon: 'FileText' },
    'song1.mp3': { type: 'file', size: '4.2 MB', modified: '2024-07-15', icon: 'Music' },
    'song2.wav': { type: 'file', size: '42.1 MB', modified: '2024-07-16', icon: 'Music' },
    'playlist.m3u': { type: 'file', size: '1.2 KB', modified: '2024-07-17', icon: 'Music' }
  };

  const getCurrentItems = () => {
    const currentFolder = mockFileSystem?.[currentPath];
    if (!currentFolder || !currentFolder?.children) return [];

    return currentFolder?.children?.map(itemName => {
      const itemPath = `${currentPath}/${itemName}`;
      const isFolder = mockFileSystem?.[itemPath];
      
      if (isFolder) {
        return {
          name: itemName,
          type: 'folder',
          size: `${isFolder?.children?.length || 0} items`,
          modified: '2024-07-31',
          icon: 'Folder',
          path: itemPath
        };
      } else {
        return {
          name: itemName,
          ...mockFiles?.[itemName],
          path: itemPath
        };
      }
    });
  };

  const handleItemClick = (item) => {
    if (item?.type === 'folder') {
      setCurrentPath(item?.path);
      setSelectedItems([]);
    } else {
      setSelectedItems([item?.name]);
    }
  };

  const handleItemDoubleClick = (item) => {
    if (item?.type === 'folder') {
      setCurrentPath(item?.path);
      setSelectedItems([]);
    }
  };

  const navigateUp = () => {
    const pathParts = currentPath?.split('/')?.filter(Boolean);
    if (pathParts?.length > 0) {
      pathParts?.pop();
      const newPath = '/' + pathParts?.join('/');
      setCurrentPath(newPath === '/' ? '/' : newPath);
      setSelectedItems([]);
    }
  };

  const navigateToPath = (path) => {
    setCurrentPath(path);
    setSelectedItems([]);
  };

  const getPathBreadcrumbs = () => {
    const parts = currentPath?.split('/')?.filter(Boolean);
    const breadcrumbs = [{ name: 'Root', path: '/' }];
    
    let currentBreadcrumbPath = '';
    parts?.forEach(part => {
      currentBreadcrumbPath += '/' + part;
      breadcrumbs?.push({
        name: part,
        path: currentBreadcrumbPath
      });
    });
    
    return breadcrumbs;
  };

  const getFileIcon = (item) => {
    if (item?.type === 'folder') return 'Folder';
    return item?.icon || 'File';
  };

  const items = getCurrentItems();
  const breadcrumbs = getPathBreadcrumbs();

  return (
    <div className="h-full flex flex-col bg-background">
      {/* Toolbar */}
      <div className="border-b border-border p-3 bg-surface/50">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center space-x-2">
            <Button
              variant="ghost"
              size="sm"
              onClick={navigateUp}
              disabled={currentPath === '/'}
            >
              <Icon name="ArrowLeft" size={16} />
            </Button>
            <Button variant="ghost" size="sm">
              <Icon name="ArrowRight" size={16} />
            </Button>
            <Button variant="ghost" size="sm">
              <Icon name="RotateCcw" size={16} />
            </Button>
          </div>
          
          <div className="flex items-center space-x-2">
            <Button
              variant={viewMode === 'list' ? 'secondary' : 'ghost'}
              size="sm"
              onClick={() => setViewMode('list')}
            >
              <Icon name="List" size={16} />
            </Button>
            <Button
              variant={viewMode === 'grid' ? 'secondary' : 'ghost'}
              size="sm"
              onClick={() => setViewMode('grid')}
            >
              <Icon name="Grid3X3" size={16} />
            </Button>
          </div>
        </div>

        {/* Address Bar */}
        <div className="flex items-center space-x-2">
          <div className="flex items-center space-x-1 flex-1 bg-input rounded-md px-3 py-2 border border-border">
            {breadcrumbs?.map((crumb, index) => (
              <React.Fragment key={crumb?.path}>
                <Button
                  variant="ghost"
                  size="xs"
                  onClick={() => navigateToPath(crumb?.path)}
                  className="text-foreground hover:text-primary"
                >
                  {crumb?.name}
                </Button>
                {index < breadcrumbs?.length - 1 && (
                  <Icon name="ChevronRight" size={12} className="text-muted-foreground" />
                )}
              </React.Fragment>
            ))}
          </div>
          <Button variant="ghost" size="sm">
            <Icon name="Search" size={16} />
          </Button>
        </div>
      </div>
      {/* File List */}
      <div className="flex-1 overflow-y-auto p-4">
        {items?.length === 0 ? (
          <div className="text-center py-12">
            <Icon name="FolderOpen" size={48} className="text-muted-foreground mx-auto mb-4" />
            <p className="text-muted-foreground">This folder is empty</p>
          </div>
        ) : (
          <div className={viewMode === 'grid' ? 'grid grid-cols-4 gap-4' : 'space-y-1'}>
            {items?.map((item) => (
              <div
                key={item?.name}
                className={`
                  flex items-center p-2 rounded-md cursor-pointer transition-colors
                  ${selectedItems?.includes(item?.name) ? 'bg-primary/20 border border-primary/30' : 'hover:bg-muted/20'}
                  ${viewMode === 'grid' ? 'flex-col text-center space-y-2' : 'space-x-3'}
                `}
                onClick={() => handleItemClick(item)}
                onDoubleClick={() => handleItemDoubleClick(item)}
              >
                <Icon 
                  name={getFileIcon(item)} 
                  size={viewMode === 'grid' ? 32 : 20} 
                  className={item?.type === 'folder' ? 'text-primary' : 'text-muted-foreground'} 
                />
                <div className={`flex-1 min-w-0 ${viewMode === 'grid' ? 'text-center' : ''}`}>
                  <div className="text-sm font-medium text-foreground truncate">
                    {item?.name}
                  </div>
                  {viewMode === 'list' && (
                    <div className="flex items-center space-x-4 text-xs text-muted-foreground">
                      <span>{item?.size}</span>
                      <span>{item?.modified}</span>
                    </div>
                  )}
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
      {/* Status Bar */}
      <div className="border-t border-border p-2 bg-surface/50">
        <div className="flex items-center justify-between text-xs text-muted-foreground">
          <span>{items?.length} items</span>
          <span>{selectedItems?.length} selected</span>
        </div>
      </div>
    </div>
  );
};

export default FileExplorerApplication;