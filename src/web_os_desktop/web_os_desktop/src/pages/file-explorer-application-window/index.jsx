import React, { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import NavigationSidebar from './components/NavigationSidebar';
import FileToolbar from './components/FileToolbar';
import FileGrid from './components/FileGrid';
import ContextMenu from './components/ContextMenu';
import StatusBar from './components/StatusBar';
import WindowControls from './components/WindowControls';

const FileExplorerApplicationWindow = () => {
  const navigate = useNavigate();
  
  // Window state
  const [isMaximized, setIsMaximized] = useState(false);
  const [sidebarCollapsed, setSidebarCollapsed] = useState(false);
  
  // Navigation state
  const [currentPath, setCurrentPath] = useState('/home/user');
  const [navigationHistory, setNavigationHistory] = useState(['/home/user']);
  const [historyIndex, setHistoryIndex] = useState(0);
  
  // File system state
  const [files, setFiles] = useState([]);
  const [selectedFiles, setSelectedFiles] = useState([]);
  const [viewMode, setViewMode] = useState('grid');
  const [isLoading, setIsLoading] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');
  
  // Context menu state
  const [contextMenu, setContextMenu] = useState(null);

  // Mock file system data
  const mockFileSystem = {
    '/home/user': [
      { id: 1, name: 'Desktop', type: 'folder', size: 0, modified: '2025-01-30T10:30:00Z' },
      { id: 2, name: 'Documents', type: 'folder', size: 0, modified: '2025-01-29T15:45:00Z' },
      { id: 3, name: 'Downloads', type: 'folder', size: 0, modified: '2025-01-31T09:15:00Z' },
      { id: 4, name: 'Pictures', type: 'folder', size: 0, modified: '2025-01-28T14:20:00Z' },
      { id: 5, name: 'Music', type: 'folder', size: 0, modified: '2025-01-27T11:30:00Z' },
      { id: 6, name: 'Videos', type: 'folder', size: 0, modified: '2025-01-26T16:45:00Z' },
      { id: 7, name: 'readme.txt', type: 'file', size: 1024, modified: '2025-01-31T08:00:00Z' }
    ],
    '/home/user/Documents': [
      { id: 8, name: 'Projects', type: 'folder', size: 0, modified: '2025-01-30T12:00:00Z' },
      { id: 9, name: 'Reports', type: 'folder', size: 0, modified: '2025-01-29T10:30:00Z' },
      { id: 10, name: 'presentation.pdf', type: 'file', size: 2048576, modified: '2025-01-31T14:15:00Z' },
      { id: 11, name: 'notes.txt', type: 'file', size: 512, modified: '2025-01-30T16:20:00Z' },
      { id: 12, name: 'budget.xlsx', type: 'file', size: 1048576, modified: '2025-01-29T09:45:00Z' }
    ],
    '/home/user/Downloads': [
      { id: 13, name: 'installer.exe', type: 'file', size: 52428800, modified: '2025-01-31T11:30:00Z' },
      { id: 14, name: 'image.jpg', type: 'file', size: 3145728, modified: '2025-01-30T13:45:00Z' },
      { id: 15, name: 'archive.zip', type: 'file', size: 10485760, modified: '2025-01-29T17:20:00Z' }
    ],
    '/home/user/Pictures': [
      { id: 16, name: 'vacation.jpg', type: 'file', size: 4194304, modified: '2025-01-28T12:00:00Z' },
      { id: 17, name: 'family.png', type: 'file', size: 2097152, modified: '2025-01-27T15:30:00Z' },
      { id: 18, name: 'screenshot.png', type: 'file', size: 1048576, modified: '2025-01-31T10:15:00Z' }
    ],
    '/home/user/Desktop': [
      { id: 19, name: 'shortcut.lnk', type: 'file', size: 256, modified: '2025-01-31T08:30:00Z' },
      { id: 20, name: 'temp', type: 'folder', size: 0, modified: '2025-01-30T14:45:00Z' }
    ]
  };

  // Load files for current path
  const loadFiles = useCallback(async (path) => {
    setIsLoading(true);
    
    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 300));
    
    const pathFiles = mockFileSystem?.[path] || [];
    const filteredFiles = searchQuery 
      ? pathFiles?.filter(file => 
          file?.name?.toLowerCase()?.includes(searchQuery?.toLowerCase())
        )
      : pathFiles;
    
    setFiles(filteredFiles);
    setSelectedFiles([]);
    setIsLoading(false);
  }, [searchQuery]);

  // Navigation functions
  const navigateToPath = useCallback((newPath) => {
    if (newPath !== currentPath) {
      const newHistory = navigationHistory?.slice(0, historyIndex + 1);
      newHistory?.push(newPath);
      setNavigationHistory(newHistory);
      setHistoryIndex(newHistory?.length - 1);
      setCurrentPath(newPath);
    }
  }, [currentPath, navigationHistory, historyIndex]);

  const goBack = useCallback(() => {
    if (historyIndex > 0) {
      const newIndex = historyIndex - 1;
      setHistoryIndex(newIndex);
      setCurrentPath(navigationHistory?.[newIndex]);
    }
  }, [historyIndex, navigationHistory]);

  const goForward = useCallback(() => {
    if (historyIndex < navigationHistory?.length - 1) {
      const newIndex = historyIndex + 1;
      setHistoryIndex(newIndex);
      setCurrentPath(navigationHistory?.[newIndex]);
    }
  }, [historyIndex, navigationHistory]);

  const goUp = useCallback(() => {
    const pathParts = currentPath?.split('/')?.filter(part => part);
    if (pathParts?.length > 0) {
      pathParts?.pop();
      const parentPath = '/' + pathParts?.join('/');
      navigateToPath(parentPath || '/');
    }
  }, [currentPath, navigateToPath]);

  // File operations
  const handleFileSelect = useCallback((file, multiSelect) => {
    if (multiSelect) {
      setSelectedFiles(prev => 
        prev?.includes(file?.id) 
          ? prev?.filter(id => id !== file?.id)
          : [...prev, file?.id]
      );
    } else {
      setSelectedFiles([file?.id]);
    }
  }, []);

  const handleFileOpen = useCallback((file) => {
    if (file?.type === 'folder') {
      const newPath = currentPath === '/' ? `/${file?.name}` : `${currentPath}/${file?.name}`;
      navigateToPath(newPath);
    } else {
      console.log(`Opening file: ${file?.name}`);
      // Handle file opening based on type
    }
  }, [currentPath, navigateToPath]);

  const handleContextMenu = useCallback((event, file) => {
    event.preventDefault();
    setContextMenu({
      position: { x: event.clientX, y: event.clientY },
      file
    });
  }, []);

  const handleContextAction = useCallback((actionId, file) => {
    console.log(`Context action: ${actionId}`, file);
    
    switch (actionId) {
      case 'open':
        if (file) handleFileOpen(file);
        break;
      case 'refresh':
        loadFiles(currentPath);
        break;
      case 'new-folder': console.log('Creating new folder');
        break;
      case 'delete':
        if (file) {
          console.log(`Deleting: ${file?.name}`);
        }
        break;
      case 'rename':
        if (file) {
          console.log(`Renaming: ${file?.name}`);
        }
        break;
      case 'properties': console.log('Showing properties', file);
        break;
      default:
        console.log(`Unhandled action: ${actionId}`);
    }
  }, [currentPath, handleFileOpen, loadFiles]);

  const handleSearch = useCallback((query) => {
    setSearchQuery(query);
  }, []);

  const handleRefresh = useCallback(() => {
    loadFiles(currentPath);
  }, [currentPath, loadFiles]);

  // Window controls
  const handleMinimize = () => {
    console.log('Minimizing window');
  };

  const handleMaximize = () => {
    setIsMaximized(!isMaximized);
  };

  const handleClose = () => {
    navigate('/desktop-environment');
  };

  // Calculate totals for status bar
  const totalSize = files?.reduce((sum, file) => sum + (file?.size || 0), 0);
  const lastModified = files?.length > 0 
    ? Math.max(...files?.map(f => new Date(f.modified)?.getTime()))
    : null;

  // Load files when path changes
  useEffect(() => {
    loadFiles(currentPath);
  }, [currentPath, loadFiles]);

  // Close context menu on click outside
  useEffect(() => {
    const handleClickOutside = () => {
      if (contextMenu) {
        setContextMenu(null);
      }
    };

    document.addEventListener('click', handleClickOutside);
    return () => document.removeEventListener('click', handleClickOutside);
  }, [contextMenu]);

  return (
    <div className={`
      fixed bg-background border border-border rounded-lg overflow-hidden shadow-2xl
      ${isMaximized 
        ? 'inset-0 rounded-none' :'top-20 left-20 w-[1200px] h-[800px]'
      }
    `}>
      {/* Window Controls */}
      <WindowControls
        onMinimize={handleMinimize}
        onMaximize={handleMaximize}
        onClose={handleClose}
        isMaximized={isMaximized}
        title="File Explorer"
      />
      {/* Main Content */}
      <div className="flex h-full">
        {/* Navigation Sidebar */}
        <NavigationSidebar
          currentPath={currentPath}
          onNavigate={navigateToPath}
          isCollapsed={sidebarCollapsed}
          onToggleCollapse={() => setSidebarCollapsed(!sidebarCollapsed)}
        />

        {/* Main Panel */}
        <div className="flex-1 flex flex-col">
          {/* Toolbar */}
          <FileToolbar
            currentPath={currentPath}
            onNavigate={navigateToPath}
            onBack={goBack}
            onForward={goForward}
            onUp={goUp}
            canGoBack={historyIndex > 0}
            canGoForward={historyIndex < navigationHistory?.length - 1}
            viewMode={viewMode}
            onViewModeChange={setViewMode}
            onSearch={handleSearch}
            onRefresh={handleRefresh}
          />

          {/* File Grid */}
          <div 
            className="flex-1 overflow-auto bg-background"
            onContextMenu={(e) => handleContextMenu(e, null)}
          >
            <FileGrid
              files={files}
              viewMode={viewMode}
              onFileSelect={handleFileSelect}
              onFileOpen={handleFileOpen}
              selectedFiles={selectedFiles}
              onContextMenu={handleContextMenu}
            />
          </div>

          {/* Status Bar */}
          <StatusBar
            totalItems={files?.length}
            selectedItems={selectedFiles?.length}
            totalSize={totalSize}
            currentPath={currentPath}
            isLoading={isLoading}
            lastModified={lastModified}
          />
        </div>
      </div>
      {/* Context Menu */}
      {contextMenu && (
        <ContextMenu
          position={contextMenu?.position}
          file={contextMenu?.file}
          onClose={() => setContextMenu(null)}
          onAction={handleContextAction}
        />
      )}
    </div>
  );
};

export default FileExplorerApplicationWindow;