import React, { useState, useRef, useEffect } from 'react';
import Icon from '../../../../components/AppIcon';
import Button from '../../../../components/ui/Button';
import Input from '../../../../components/ui/Input';

const TextEditorApplication = ({ windowId }) => {
  const [content, setContent] = useState(`Welcome to Web OS Text Editor

This is a simple text editor application running in your browser-based desktop environment.

Features:
• Basic text editing capabilities
• File operations (New, Open, Save)
• Find and replace functionality
• Word count and statistics
• Multiple document support

You can start typing to edit this document or create a new one using the File menu.

---

Sample content for demonstration:
Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.

Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.`);
  
  const [fileName, setFileName] = useState('Untitled.txt');
  const [isModified, setIsModified] = useState(false);
  const [findText, setFindText] = useState('');
  const [replaceText, setReplaceText] = useState('');
  const [showFindReplace, setShowFindReplace] = useState(false);
  const [wordCount, setWordCount] = useState(0);
  const [charCount, setCharCount] = useState(0);
  const [lineCount, setLineCount] = useState(0);
  const textareaRef = useRef(null);

  useEffect(() => {
    // Update statistics
    const words = content?.trim() ? content?.trim()?.split(/\s+/)?.length : 0;
    const chars = content?.length;
    const lines = content?.split('\n')?.length;
    
    setWordCount(words);
    setCharCount(chars);
    setLineCount(lines);
  }, [content]);

  const handleContentChange = (e) => {
    setContent(e?.target?.value);
    setIsModified(true);
  };

  const handleNewFile = () => {
    if (isModified) {
      const shouldContinue = window.confirm('You have unsaved changes. Continue without saving?');
      if (!shouldContinue) return;
    }
    
    setContent('');
    setFileName('Untitled.txt');
    setIsModified(false);
  };

  const handleSaveFile = () => {
    // Simulate saving file
    const blob = new Blob([content], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = fileName;
    document.body?.appendChild(a);
    a?.click();
    document.body?.removeChild(a);
    URL.revokeObjectURL(url);
    
    setIsModified(false);
  };

  const handleOpenFile = () => {
    const input = document.createElement('input');
    input.type = 'file';
    input.accept = '.txt,.md,.js,.jsx,.html,.css,.json';
    input.onchange = (e) => {
      const file = e?.target?.files?.[0];
      if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
          setContent(e?.target?.result);
          setFileName(file?.name);
          setIsModified(false);
        };
        reader?.readAsText(file);
      }
    };
    input?.click();
  };

  const handleFind = () => {
    if (!findText) return;
    
    const textarea = textareaRef?.current;
    const text = textarea?.value;
    const index = text?.toLowerCase()?.indexOf(findText?.toLowerCase());
    
    if (index !== -1) {
      textarea?.focus();
      textarea?.setSelectionRange(index, index + findText?.length);
    } else {
      alert('Text not found');
    }
  };

  const handleReplace = () => {
    if (!findText) return;
    
    const newContent = content?.replace(new RegExp(findText, 'gi'), replaceText);
    setContent(newContent);
    setIsModified(true);
  };

  const handleReplaceAll = () => {
    if (!findText) return;
    
    const newContent = content?.replace(new RegExp(findText, 'gi'), replaceText);
    setContent(newContent);
    setIsModified(true);
  };

  const insertText = (text) => {
    const textarea = textareaRef?.current;
    const start = textarea?.selectionStart;
    const end = textarea?.selectionEnd;
    const newContent = content?.substring(0, start) + text + content?.substring(end);
    setContent(newContent);
    setIsModified(true);
    
    // Set cursor position after inserted text
    setTimeout(() => {
      textarea?.focus();
      textarea?.setSelectionRange(start + text?.length, start + text?.length);
    }, 0);
  };

  return (
    <div className="h-full flex flex-col bg-background">
      {/* Menu Bar */}
      <div className="border-b border-border p-2 bg-surface/50">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-1">
            <Button variant="ghost" size="sm" onClick={handleNewFile}>
              <Icon name="FileText" size={16} className="mr-1" />
              New
            </Button>
            <Button variant="ghost" size="sm" onClick={handleOpenFile}>
              <Icon name="FolderOpen" size={16} className="mr-1" />
              Open
            </Button>
            <Button variant="ghost" size="sm" onClick={handleSaveFile}>
              <Icon name="Save" size={16} className="mr-1" />
              Save
            </Button>
            <div className="w-px h-6 bg-border mx-2" />
            <Button 
              variant="ghost" 
              size="sm" 
              onClick={() => setShowFindReplace(!showFindReplace)}
            >
              <Icon name="Search" size={16} className="mr-1" />
              Find
            </Button>
          </div>
          
          <div className="flex items-center space-x-4 text-sm text-muted-foreground">
            <span>{fileName}{isModified ? ' *' : ''}</span>
          </div>
        </div>
      </div>
      {/* Find & Replace Panel */}
      {showFindReplace && (
        <div className="border-b border-border p-3 bg-surface/30">
          <div className="flex items-center space-x-2 mb-2">
            <Input
              type="text"
              placeholder="Find..."
              value={findText}
              onChange={(e) => setFindText(e?.target?.value)}
              className="w-48"
            />
            <Button variant="outline" size="sm" onClick={handleFind}>
              Find
            </Button>
            <Button 
              variant="ghost" 
              size="icon" 
              onClick={() => setShowFindReplace(false)}
            >
              <Icon name="X" size={16} />
            </Button>
          </div>
          <div className="flex items-center space-x-2">
            <Input
              type="text"
              placeholder="Replace with..."
              value={replaceText}
              onChange={(e) => setReplaceText(e?.target?.value)}
              className="w-48"
            />
            <Button variant="outline" size="sm" onClick={handleReplace}>
              Replace
            </Button>
            <Button variant="outline" size="sm" onClick={handleReplaceAll}>
              Replace All
            </Button>
          </div>
        </div>
      )}
      {/* Editor Area */}
      <div className="flex-1 flex">
        <div className="flex-1 p-4">
          <textarea
            ref={textareaRef}
            value={content}
            onChange={handleContentChange}
            className="w-full h-full resize-none bg-transparent border-none outline-none text-foreground font-mono text-sm leading-relaxed"
            placeholder="Start typing..."
            spellCheck="false"
          />
        </div>
      </div>
      {/* Status Bar */}
      <div className="border-t border-border p-2 bg-surface/50">
        <div className="flex items-center justify-between text-xs text-muted-foreground">
          <div className="flex items-center space-x-4">
            <span>Lines: {lineCount}</span>
            <span>Words: {wordCount}</span>
            <span>Characters: {charCount}</span>
          </div>
          <div className="flex items-center space-x-4">
            <span>UTF-8</span>
            <span>Plain Text</span>
          </div>
        </div>
      </div>
      {/* Quick Insert Toolbar */}
      <div className="border-t border-border p-2 bg-surface/30">
        <div className="flex items-center space-x-2">
          <span className="text-xs text-muted-foreground mr-2">Quick Insert:</span>
          <Button 
            variant="ghost" 
            size="xs" 
            onClick={() => insertText(new Date()?.toLocaleDateString())}
          >
            Date
          </Button>
          <Button 
            variant="ghost" 
            size="xs" 
            onClick={() => insertText(new Date()?.toLocaleTimeString())}
          >
            Time
          </Button>
          <Button 
            variant="ghost" 
            size="xs" 
            onClick={() => insertText('---\n')}
          >
            Separator
          </Button>
          <Button 
            variant="ghost" 
            size="xs" 
            onClick={() => insertText('TODO: ')}
          >
            TODO
          </Button>
        </div>
      </div>
    </div>
  );
};

export default TextEditorApplication;