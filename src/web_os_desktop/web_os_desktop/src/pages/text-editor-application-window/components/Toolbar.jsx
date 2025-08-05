import React from 'react';
import Button from '../../../components/ui/Button';
import Icon from '../../../components/AppIcon';

const Toolbar = ({ 
  onNewFile, 
  onOpenFile, 
  onSaveFile, 
  onUndo, 
  onRedo, 
  onCut, 
  onCopy, 
  onPaste, 
  onToggleBold, 
  onToggleItalic, 
  onToggleUnderline, 
  onFind, 
  onReplace,
  canUndo, 
  canRedo,
  isBold,
  isItalic,
  isUnderlined
}) => {
  const toolbarGroups = [
    {
      id: 'file',
      items: [
        { id: 'new', icon: 'FileText', tooltip: 'New (Ctrl+N)', action: onNewFile },
        { id: 'open', icon: 'FolderOpen', tooltip: 'Open (Ctrl+O)', action: onOpenFile },
        { id: 'save', icon: 'Save', tooltip: 'Save (Ctrl+S)', action: onSaveFile }
      ]
    },
    {
      id: 'edit',
      items: [
        { id: 'undo', icon: 'Undo', tooltip: 'Undo (Ctrl+Z)', action: onUndo, disabled: !canUndo },
        { id: 'redo', icon: 'Redo', tooltip: 'Redo (Ctrl+Y)', action: onRedo, disabled: !canRedo }
      ]
    },
    {
      id: 'clipboard',
      items: [
        { id: 'cut', icon: 'Scissors', tooltip: 'Cut (Ctrl+X)', action: onCut },
        { id: 'copy', icon: 'Copy', tooltip: 'Copy (Ctrl+C)', action: onCopy },
        { id: 'paste', icon: 'Clipboard', tooltip: 'Paste (Ctrl+V)', action: onPaste }
      ]
    },
    {
      id: 'format',
      items: [
        { id: 'bold', icon: 'Bold', tooltip: 'Bold (Ctrl+B)', action: onToggleBold, active: isBold },
        { id: 'italic', icon: 'Italic', tooltip: 'Italic (Ctrl+I)', action: onToggleItalic, active: isItalic },
        { id: 'underline', icon: 'Underline', tooltip: 'Underline (Ctrl+U)', action: onToggleUnderline, active: isUnderlined }
      ]
    },
    {
      id: 'search',
      items: [
        { id: 'find', icon: 'Search', tooltip: 'Find (Ctrl+F)', action: onFind },
        { id: 'replace', icon: 'Replace', tooltip: 'Replace (Ctrl+H)', action: onReplace }
      ]
    }
  ];

  return (
    <div className="bg-surface border-b border-border h-10 flex items-center px-2 space-x-1">
      {toolbarGroups?.map((group, groupIndex) => (
        <React.Fragment key={group?.id}>
          <div className="flex items-center space-x-1">
            {group?.items?.map((item) => (
              <Button
                key={item?.id}
                variant={item?.active ? "secondary" : "ghost"}
                size="icon"
                onClick={item?.action}
                disabled={item?.disabled}
                className={`w-8 h-8 hover:bg-muted/20 ${item?.active ? 'bg-primary/20 text-primary' : ''}`}
                title={item?.tooltip}
              >
                <Icon name={item?.icon} size={16} />
              </Button>
            ))}
          </div>
          {groupIndex < toolbarGroups?.length - 1 && (
            <div className="w-px h-6 bg-border mx-1" />
          )}
        </React.Fragment>
      ))}
    </div>
  );
};

export default Toolbar;