import React, { useState } from 'react';
import Button from '../../../components/ui/Button';
import Icon from '../../../components/AppIcon';

const MenuBar = ({ onNewFile, onOpenFile, onSaveFile, onSaveAsFile, onUndo, onRedo, onCut, onCopy, onPaste, onFind, onReplace, onToggleWordWrap, onToggleLineNumbers, onZoomIn, onZoomOut, onZoomReset, onToggleBold, onToggleItalic, onToggleUnderline, onFontSize, onFontFamily, canUndo, canRedo, wordWrap, lineNumbers, fontSize, fontFamily }) => {
  const [activeMenu, setActiveMenu] = useState(null);

  const menuItems = [
    {
      id: 'file',
      label: 'File',
      items: [
        { id: 'new', label: 'New', shortcut: 'Ctrl+N', action: onNewFile, icon: 'FileText' },
        { id: 'open', label: 'Open', shortcut: 'Ctrl+O', action: onOpenFile, icon: 'FolderOpen' },
        { id: 'save', label: 'Save', shortcut: 'Ctrl+S', action: onSaveFile, icon: 'Save' },
        { id: 'saveAs', label: 'Save As', shortcut: 'Ctrl+Shift+S', action: onSaveAsFile, icon: 'Save' }
      ]
    },
    {
      id: 'edit',
      label: 'Edit',
      items: [
        { id: 'undo', label: 'Undo', shortcut: 'Ctrl+Z', action: onUndo, icon: 'Undo', disabled: !canUndo },
        { id: 'redo', label: 'Redo', shortcut: 'Ctrl+Y', action: onRedo, icon: 'Redo', disabled: !canRedo },
        { id: 'separator1', type: 'separator' },
        { id: 'cut', label: 'Cut', shortcut: 'Ctrl+X', action: onCut, icon: 'Scissors' },
        { id: 'copy', label: 'Copy', shortcut: 'Ctrl+C', action: onCopy, icon: 'Copy' },
        { id: 'paste', label: 'Paste', shortcut: 'Ctrl+V', action: onPaste, icon: 'Clipboard' },
        { id: 'separator2', type: 'separator' },
        { id: 'find', label: 'Find', shortcut: 'Ctrl+F', action: onFind, icon: 'Search' },
        { id: 'replace', label: 'Replace', shortcut: 'Ctrl+H', action: onReplace, icon: 'Replace' }
      ]
    },
    {
      id: 'view',
      label: 'View',
      items: [
        { id: 'wordWrap', label: 'Word Wrap', action: onToggleWordWrap, icon: wordWrap ? 'Check' : 'Square', checked: wordWrap },
        { id: 'lineNumbers', label: 'Line Numbers', action: onToggleLineNumbers, icon: lineNumbers ? 'Check' : 'Square', checked: lineNumbers },
        { id: 'separator3', type: 'separator' },
        { id: 'zoomIn', label: 'Zoom In', shortcut: 'Ctrl++', action: onZoomIn, icon: 'ZoomIn' },
        { id: 'zoomOut', label: 'Zoom Out', shortcut: 'Ctrl+-', action: onZoomOut, icon: 'ZoomOut' },
        { id: 'zoomReset', label: 'Reset Zoom', shortcut: 'Ctrl+0', action: onZoomReset, icon: 'RotateCcw' }
      ]
    },
    {
      id: 'format',
      label: 'Format',
      items: [
        { id: 'bold', label: 'Bold', shortcut: 'Ctrl+B', action: onToggleBold, icon: 'Bold' },
        { id: 'italic', label: 'Italic', shortcut: 'Ctrl+I', action: onToggleItalic, icon: 'Italic' },
        { id: 'underline', label: 'Underline', shortcut: 'Ctrl+U', action: onToggleUnderline, icon: 'Underline' },
        { id: 'separator4', type: 'separator' },
        { id: 'fontSize', label: `Font Size (${fontSize}px)`, type: 'submenu', icon: 'Type' },
        { id: 'fontFamily', label: `Font Family (${fontFamily})`, type: 'submenu', icon: 'AlignLeft' }
      ]
    }
  ];

  const fontSizes = [10, 12, 14, 16, 18, 20, 24, 28, 32, 36];
  const fontFamilies = ['Arial', 'Helvetica', 'Times New Roman', 'Courier New', 'Georgia', 'Verdana', 'Trebuchet MS', 'Comic Sans MS'];

  const handleMenuClick = (menuId) => {
    setActiveMenu(activeMenu === menuId ? null : menuId);
  };

  const handleItemClick = (item) => {
    if (item?.action) {
      item?.action();
    }
    setActiveMenu(null);
  };

  const handleFontSizeChange = (size) => {
    onFontSize(size);
    setActiveMenu(null);
  };

  const handleFontFamilyChange = (family) => {
    onFontFamily(family);
    setActiveMenu(null);
  };

  return (
    <div className="bg-surface border-b border-border h-8 flex items-center px-2 relative z-50">
      {menuItems?.map((menu) => (
        <div key={menu?.id} className="relative">
          <Button
            variant="ghost"
            size="sm"
            onClick={() => handleMenuClick(menu?.id)}
            className={`h-6 px-3 text-xs hover:bg-muted/20 ${activeMenu === menu?.id ? 'bg-muted/20' : ''}`}
          >
            {menu?.label}
          </Button>

          {activeMenu === menu?.id && (
            <>
              <div 
                className="fixed inset-0 z-40" 
                onClick={() => setActiveMenu(null)}
              />
              <div className="absolute top-full left-0 bg-surface border border-border rounded-md shadow-lg py-1 min-w-48 z-50">
                {menu?.items?.map((item) => {
                  if (item?.type === 'separator') {
                    return <div key={item?.id} className="h-px bg-border my-1" />;
                  }

                  if (item?.id === 'fontSize') {
                    return (
                      <div key={item?.id} className="relative group">
                        <div className="flex items-center justify-between px-3 py-1.5 text-sm hover:bg-muted/20 cursor-pointer">
                          <div className="flex items-center space-x-2">
                            <Icon name={item?.icon} size={14} />
                            <span>{item?.label}</span>
                          </div>
                          <Icon name="ChevronRight" size={14} />
                        </div>
                        <div className="absolute left-full top-0 bg-surface border border-border rounded-md shadow-lg py-1 min-w-32 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-150">
                          {fontSizes?.map((size) => (
                            <button
                              key={size}
                              onClick={() => handleFontSizeChange(size)}
                              className={`w-full text-left px-3 py-1.5 text-sm hover:bg-muted/20 ${fontSize === size ? 'bg-primary/20 text-primary' : ''}`}
                            >
                              {size}px
                            </button>
                          ))}
                        </div>
                      </div>
                    );
                  }

                  if (item?.id === 'fontFamily') {
                    return (
                      <div key={item?.id} className="relative group">
                        <div className="flex items-center justify-between px-3 py-1.5 text-sm hover:bg-muted/20 cursor-pointer">
                          <div className="flex items-center space-x-2">
                            <Icon name={item?.icon} size={14} />
                            <span>{item?.label}</span>
                          </div>
                          <Icon name="ChevronRight" size={14} />
                        </div>
                        <div className="absolute left-full top-0 bg-surface border border-border rounded-md shadow-lg py-1 min-w-40 opacity-0 invisible group-hover:opacity-100 group-hover:visible transition-all duration-150">
                          {fontFamilies?.map((family) => (
                            <button
                              key={family}
                              onClick={() => handleFontFamilyChange(family)}
                              className={`w-full text-left px-3 py-1.5 text-sm hover:bg-muted/20 ${fontFamily === family ? 'bg-primary/20 text-primary' : ''}`}
                              style={{ fontFamily: family }}
                            >
                              {family}
                            </button>
                          ))}
                        </div>
                      </div>
                    );
                  }

                  return (
                    <button
                      key={item?.id}
                      onClick={() => handleItemClick(item)}
                      disabled={item?.disabled}
                      className={`w-full flex items-center justify-between px-3 py-1.5 text-sm hover:bg-muted/20 disabled:opacity-50 disabled:cursor-not-allowed ${item?.checked ? 'bg-primary/20 text-primary' : ''}`}
                    >
                      <div className="flex items-center space-x-2">
                        <Icon name={item?.icon} size={14} />
                        <span>{item?.label}</span>
                      </div>
                      {item?.shortcut && (
                        <span className="text-xs text-muted-foreground">{item?.shortcut}</span>
                      )}
                    </button>
                  );
                })}
              </div>
            </>
          )}
        </div>
      ))}
    </div>
  );
};

export default MenuBar;