import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const NavigationSidebar = ({ currentPath, onNavigate, isCollapsed, onToggleCollapse }) => {
  const [expandedFolders, setExpandedFolders] = useState(new Set(['home', 'documents']));

  const quickAccessItems = [
    { id: 'desktop', name: 'Desktop', icon: 'Monitor', path: '/home/user/Desktop' },
    { id: 'documents', name: 'Documents', icon: 'FileText', path: '/home/user/Documents' },
    { id: 'downloads', name: 'Downloads', icon: 'Download', path: '/home/user/Downloads' },
    { id: 'pictures', name: 'Pictures', icon: 'Image', path: '/home/user/Pictures' },
    { id: 'music', name: 'Music', icon: 'Music', path: '/home/user/Music' },
    { id: 'videos', name: 'Videos', icon: 'Video', path: '/home/user/Videos' }
  ];

  const folderTree = [
    {
      id: 'home',
      name: 'Home',
      icon: 'Home',
      path: '/home/user',
      children: [
        { id: 'desktop', name: 'Desktop', icon: 'Monitor', path: '/home/user/Desktop' },
        { 
          id: 'documents', 
          name: 'Documents', 
          icon: 'FileText', 
          path: '/home/user/Documents',
          children: [
            { id: 'projects', name: 'Projects', icon: 'Folder', path: '/home/user/Documents/Projects' },
            { id: 'reports', name: 'Reports', icon: 'Folder', path: '/home/user/Documents/Reports' }
          ]
        },
        { id: 'downloads', name: 'Downloads', icon: 'Download', path: '/home/user/Downloads' },
        { id: 'pictures', name: 'Pictures', icon: 'Image', path: '/home/user/Pictures' }
      ]
    },
    {
      id: 'system',
      name: 'System',
      icon: 'HardDrive',
      path: '/system',
      children: [
        { id: 'bin', name: 'bin', icon: 'Folder', path: '/system/bin' },
        { id: 'etc', name: 'etc', icon: 'Folder', path: '/system/etc' },
        { id: 'var', name: 'var', icon: 'Folder', path: '/system/var' }
      ]
    }
  ];

  const toggleFolder = (folderId) => {
    const newExpanded = new Set(expandedFolders);
    if (newExpanded?.has(folderId)) {
      newExpanded?.delete(folderId);
    } else {
      newExpanded?.add(folderId);
    }
    setExpandedFolders(newExpanded);
  };

  const renderTreeItem = (item, level = 0) => {
    const isExpanded = expandedFolders?.has(item?.id);
    const hasChildren = item?.children && item?.children?.length > 0;
    const isActive = currentPath === item?.path;

    return (
      <div key={item?.id}>
        <Button
          variant="ghost"
          onClick={() => {
            if (hasChildren) {
              toggleFolder(item?.id);
            }
            onNavigate(item?.path);
          }}
          className={`
            w-full justify-start px-2 py-1 h-8 text-sm
            ${isActive ? 'bg-primary/20 text-primary' : 'hover:bg-muted/20'}
          `}
          style={{ paddingLeft: `${8 + level * 16}px` }}
        >
          {hasChildren && (
            <Icon 
              name={isExpanded ? "ChevronDown" : "ChevronRight"} 
              size={14} 
              className="mr-1 flex-shrink-0" 
            />
          )}
          <Icon name={item?.icon} size={16} className="mr-2 flex-shrink-0" />
          <span className="truncate">{item?.name}</span>
        </Button>
        {hasChildren && isExpanded && (
          <div>
            {item?.children?.map(child => renderTreeItem(child, level + 1))}
          </div>
        )}
      </div>
    );
  };

  if (isCollapsed) {
    return (
      <div className="w-12 bg-surface border-r border-border flex flex-col items-center py-2 space-y-2">
        <Button
          variant="ghost"
          size="icon"
          onClick={onToggleCollapse}
          className="w-8 h-8"
        >
          <Icon name="ChevronRight" size={16} />
        </Button>
        {quickAccessItems?.slice(0, 4)?.map(item => (
          <Button
            key={item?.id}
            variant="ghost"
            size="icon"
            onClick={() => onNavigate(item?.path)}
            className={`w-8 h-8 ${currentPath === item?.path ? 'bg-primary/20 text-primary' : ''}`}
            title={item?.name}
          >
            <Icon name={item?.icon} size={16} />
          </Button>
        ))}
      </div>
    );
  }

  return (
    <div className="w-64 bg-surface border-r border-border flex flex-col">
      {/* Header */}
      <div className="p-3 border-b border-border flex items-center justify-between">
        <h3 className="text-sm font-medium text-foreground">Explorer</h3>
        <Button
          variant="ghost"
          size="icon"
          onClick={onToggleCollapse}
          className="w-6 h-6"
        >
          <Icon name="ChevronLeft" size={14} />
        </Button>
      </div>
      <div className="flex-1 overflow-y-auto">
        {/* Quick Access */}
        <div className="p-2">
          <div className="text-xs font-medium text-muted-foreground mb-2 px-2">Quick Access</div>
          <div className="space-y-1">
            {quickAccessItems?.map(item => (
              <Button
                key={item?.id}
                variant="ghost"
                onClick={() => onNavigate(item?.path)}
                className={`
                  w-full justify-start px-2 py-1 h-8 text-sm
                  ${currentPath === item?.path ? 'bg-primary/20 text-primary' : 'hover:bg-muted/20'}
                `}
              >
                <Icon name={item?.icon} size={16} className="mr-2 flex-shrink-0" />
                <span className="truncate">{item?.name}</span>
              </Button>
            ))}
          </div>
        </div>

        {/* Folder Tree */}
        <div className="p-2 border-t border-border">
          <div className="text-xs font-medium text-muted-foreground mb-2 px-2">This PC</div>
          <div className="space-y-1">
            {folderTree?.map(item => renderTreeItem(item))}
          </div>
        </div>
      </div>
    </div>
  );
};

export default NavigationSidebar;