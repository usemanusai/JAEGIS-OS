import React, { useEffect, useRef } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const ContextMenu = ({ position, file, onClose, onAction }) => {
  const menuRef = useRef(null);

  useEffect(() => {
    const handleClickOutside = (event) => {
      if (menuRef?.current && !menuRef?.current?.contains(event.target)) {
        onClose();
      }
    };

    const handleEscape = (event) => {
      if (event.key === 'Escape') {
        onClose();
      }
    };

    document.addEventListener('mousedown', handleClickOutside);
    document.addEventListener('keydown', handleEscape);

    return () => {
      document.removeEventListener('mousedown', handleClickOutside);
      document.removeEventListener('keydown', handleEscape);
    };
  }, [onClose]);

  const menuItems = file ? [
    { id: 'open', label: 'Open', icon: 'FolderOpen', shortcut: 'Enter' },
    { id: 'separator1', type: 'separator' },
    { id: 'cut', label: 'Cut', icon: 'Scissors', shortcut: 'Ctrl+X' },
    { id: 'copy', label: 'Copy', icon: 'Copy', shortcut: 'Ctrl+C' },
    { id: 'paste', label: 'Paste', icon: 'Clipboard', shortcut: 'Ctrl+V', disabled: true },
    { id: 'separator2', type: 'separator' },
    { id: 'rename', label: 'Rename', icon: 'Edit', shortcut: 'F2' },
    { id: 'delete', label: 'Delete', icon: 'Trash2', shortcut: 'Del', danger: true },
    { id: 'separator3', type: 'separator' },
    { id: 'properties', label: 'Properties', icon: 'Info', shortcut: 'Alt+Enter' }
  ] : [
    { id: 'refresh', label: 'Refresh', icon: 'RefreshCw', shortcut: 'F5' },
    { id: 'separator1', type: 'separator' },
    { id: 'paste', label: 'Paste', icon: 'Clipboard', shortcut: 'Ctrl+V', disabled: true },
    { id: 'separator2', type: 'separator' },
    { id: 'new-folder', label: 'New Folder', icon: 'FolderPlus', shortcut: 'Ctrl+Shift+N' },
    { id: 'new-file', label: 'New File', icon: 'FilePlus' },
    { id: 'separator3', type: 'separator' },
    { id: 'select-all', label: 'Select All', icon: 'CheckSquare', shortcut: 'Ctrl+A' },
    { id: 'separator4', type: 'separator' },
    { id: 'properties', label: 'Properties', icon: 'Settings' }
  ];

  const handleAction = (actionId) => {
    onAction(actionId, file);
    onClose();
  };

  return (
    <div
      ref={menuRef}
      className="fixed z-[1000] bg-surface border border-border rounded-md shadow-lg py-1 min-w-48 animate-fade-in"
      style={{
        left: position?.x,
        top: position?.y,
        transform: 'translate(0, 0)'
      }}
    >
      {menuItems?.map((item) => {
        if (item?.type === 'separator') {
          return (<div key={item?.id} className="h-px bg-border my-1" />);
        }

        return (
          <Button
            key={item?.id}
            variant="ghost"
            onClick={() => handleAction(item?.id)}
            disabled={item?.disabled}
            className={`
              w-full justify-start px-3 py-2 h-8 text-sm rounded-none
              ${item?.danger ? 'hover:bg-destructive/20 hover:text-destructive' : 'hover:bg-muted/20'}
              ${item?.disabled ? 'opacity-50 cursor-not-allowed' : ''}
            `}
          >
            <Icon name={item?.icon} size={16} className="mr-3 flex-shrink-0" />
            <span className="flex-1 text-left">{item?.label}</span>
            {item?.shortcut && (
              <span className="text-xs text-muted-foreground ml-4">
                {item?.shortcut}
              </span>
            )}
          </Button>
        );
      })}
    </div>
  );
};

export default ContextMenu;