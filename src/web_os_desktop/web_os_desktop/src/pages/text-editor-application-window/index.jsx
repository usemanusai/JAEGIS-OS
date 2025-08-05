import React, { useState, useEffect, useCallback, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import MenuBar from './components/MenuBar';
import Toolbar from './components/Toolbar';
import EditorArea from './components/EditorArea';
import StatusBar from './components/StatusBar';
import WindowControls from './components/WindowControls';

const TextEditorApplicationWindow = () => {
  const navigate = useNavigate();
  
  // Document state
  const [content, setContent] = useState("");
  const [fileName, setFileName] = useState("Untitled");
  const [isModified, setIsModified] = useState(false);
  const [originalContent, setOriginalContent] = useState("");
  
  // Editor settings
  const [fontSize, setFontSize] = useState(14);
  const [fontFamily, setFontFamily] = useState("Courier New");
  const [wordWrap, setWordWrap] = useState(true);
  const [lineNumbers, setLineNumbers] = useState(true);
  const [zoomLevel, setZoomLevel] = useState(100);
  
  // Editor state
  const [undoStack, setUndoStack] = useState([]);
  const [redoStack, setRedoStack] = useState([]);
  const [selectionStart, setSelectionStart] = useState(0);
  const [selectionEnd, setSelectionEnd] = useState(0);
  const [currentLine, setCurrentLine] = useState(1);
  const [currentColumn, setCurrentColumn] = useState(1);
  
  // UI state
  const [isMaximized, setIsMaximized] = useState(false);
  const [showFind, setShowFind] = useState(false);
  const [findText, setFindText] = useState("");
  const [replaceText, setReplaceText] = useState("");
  
  // Formatting state
  const [isBold, setIsBold] = useState(false);
  const [isItalic, setIsItalic] = useState(false);
  const [isUnderlined, setIsUnderlined] = useState(false);
  
  const fileInputRef = useRef(null);
  const autoSaveTimeoutRef = useRef(null);

  // Mock documents for demonstration
  const mockDocuments = [
    {
      name: "Welcome.txt",
      content: `Welcome to Text Editor!\n\nThis is a powerful text editor with the following features:\n\n• Rich text editing capabilities\n• Find and replace functionality\n• Multiple font options\n• Line numbers and word wrap\n• Auto-save functionality\n• Keyboard shortcuts support\n\nKeyboard Shortcuts:\n- Ctrl+N: New document\n- Ctrl+O: Open document\n- Ctrl+S: Save document\n- Ctrl+Z: Undo\n- Ctrl+Y: Redo\n- Ctrl+F: Find\n- Ctrl+H: Replace\n- Ctrl+B: Bold\n- Ctrl+I: Italic\n- Ctrl+U: Underline\n\nStart typing to create your document!`
    },
    {
      name: "Sample Code.js",
      content: `// Sample JavaScript Code\nfunction calculateSum(a, b) {\n    return a + b;\n}\n\nconst numbers = [1, 2, 3, 4, 5];\nconst sum = numbers.reduce((acc, num) => acc + num, 0);\n\nconsole.log('Sum:', sum);\n\n// Object example\nconst user = {\n    name: 'John Doe',\n    age: 30,\n    email: 'john@example.com'\n};\n\n// Array methods\nconst evenNumbers = numbers.filter(num => num % 2 === 0);\nconst doubledNumbers = numbers.map(num => num * 2);\n\nconsole.log('Even numbers:', evenNumbers);\nconsole.log('Doubled numbers:', doubledNumbers);`
    },
    {
      name: "Meeting Notes.md",
      content: `# Team Meeting Notes\n## Date: July 31, 2025\n\n### Attendees\n- John Smith (Project Manager)\n- Sarah Johnson (Developer)\n- Mike Wilson (Designer)\n- Lisa Brown (QA Engineer)\n\n### Agenda Items\n\n#### 1. Project Status Update\n- Frontend development: 85% complete\n- Backend API: 90% complete\n- Testing phase: 60% complete\n- Documentation: 40% complete\n\n#### 2. Upcoming Deadlines\n- **August 5**: Feature freeze\n- **August 12**: Beta release\n- **August 20**: Final testing\n- **August 25**: Production deployment\n\n#### 3. Action Items\n- [ ] Complete user authentication module (Sarah)\n- [ ] Finalize UI designs (Mike)\n- [ ] Set up automated testing (Lisa)\n- [ ] Update project documentation (John)\n\n#### 4. Blockers\n- Third-party API integration delays\n- Server configuration issues\n- Need approval for additional resources\n\n### Next Meeting\n**Date:** August 7, 2025\n**Time:** 10:00 AM\n**Location:** Conference Room B`
    }
  ];

  // Calculate document statistics
  const wordCount = content?.trim() ? content?.trim()?.split(/\s+/)?.length : 0;
  const characterCount = content?.length;
  const lineCount = content?.split('\n')?.length;

  // Update cursor position
  const updateCursorPosition = useCallback((start) => {
    const lines = content?.substring(0, start)?.split('\n');
    setCurrentLine(lines?.length);
    setCurrentColumn(lines?.[lines?.length - 1]?.length + 1);
  }, [content]);

  // Handle content change
  const handleContentChange = useCallback((newContent) => {
    if (newContent !== content) {
      // Add to undo stack
      setUndoStack(prev => [...prev?.slice(-49), content]);
      setRedoStack([]);
      
      setContent(newContent);
      setIsModified(newContent !== originalContent);
      
      // Auto-save after 2 seconds of inactivity
      if (autoSaveTimeoutRef?.current) {
        clearTimeout(autoSaveTimeoutRef?.current);
      }
      autoSaveTimeoutRef.current = setTimeout(() => {
        console.log('Auto-saving document...');
      }, 2000);
    }
  }, [content, originalContent]);

  // Handle selection change
  const handleSelectionChange = useCallback((start, end) => {
    setSelectionStart(start);
    setSelectionEnd(end);
    updateCursorPosition(start);
  }, [updateCursorPosition]);

  // File operations
  const handleNewFile = useCallback(() => {
    if (isModified) {
      const shouldSave = window.confirm('Do you want to save changes to the current document?');
      if (shouldSave) {
        handleSaveFile();
      }
    }
    setContent("");
    setFileName("Untitled");
    setIsModified(false);
    setOriginalContent("");
    setUndoStack([]);
    setRedoStack([]);
  }, [isModified]);

  const handleOpenFile = useCallback(() => {
    // Simulate file picker with mock documents
    const documentNames = mockDocuments?.map(doc => doc?.name);
    const selectedIndex = Math.floor(Math.random() * mockDocuments?.length);
    const selectedDoc = mockDocuments?.[selectedIndex];
    
    setContent(selectedDoc?.content);
    setFileName(selectedDoc?.name);
    setOriginalContent(selectedDoc?.content);
    setIsModified(false);
    setUndoStack([]);
    setRedoStack([]);
    
    console.log(`Opened: ${selectedDoc?.name}`);
  }, []);

  const handleSaveFile = useCallback(() => {
    setOriginalContent(content);
    setIsModified(false);
    console.log(`Saved: ${fileName}`);
  }, [content, fileName]);

  const handleSaveAsFile = useCallback(() => {
    const newFileName = prompt('Enter file name:', fileName);
    if (newFileName) {
      setFileName(newFileName);
      setOriginalContent(content);
      setIsModified(false);
      console.log(`Saved as: ${newFileName}`);
    }
  }, [content, fileName]);

  // Edit operations
  const handleUndo = useCallback(() => {
    if (undoStack?.length > 0) {
      const previousContent = undoStack?.[undoStack?.length - 1];
      setRedoStack(prev => [content, ...prev?.slice(0, 49)]);
      setUndoStack(prev => prev?.slice(0, -1));
      setContent(previousContent);
      setIsModified(previousContent !== originalContent);
    }
  }, [undoStack, content, originalContent]);

  const handleRedo = useCallback(() => {
    if (redoStack?.length > 0) {
      const nextContent = redoStack?.[0];
      setUndoStack(prev => [...prev?.slice(-49), content]);
      setRedoStack(prev => prev?.slice(1));
      setContent(nextContent);
      setIsModified(nextContent !== originalContent);
    }
  }, [redoStack, content, originalContent]);

  const handleCut = useCallback(() => {
    if (selectionStart !== selectionEnd) {
      const selectedText = content?.substring(selectionStart, selectionEnd);
      navigator.clipboard?.writeText(selectedText);
      const newContent = content?.substring(0, selectionStart) + content?.substring(selectionEnd);
      handleContentChange(newContent);
    }
  }, [content, selectionStart, selectionEnd, handleContentChange]);

  const handleCopy = useCallback(() => {
    if (selectionStart !== selectionEnd) {
      const selectedText = content?.substring(selectionStart, selectionEnd);
      navigator.clipboard?.writeText(selectedText);
    }
  }, [content, selectionStart, selectionEnd]);

  const handlePaste = useCallback(async () => {
    try {
      const clipboardText = await navigator.clipboard?.readText();
      const newContent = content?.substring(0, selectionStart) + clipboardText + content?.substring(selectionEnd);
      handleContentChange(newContent);
    } catch (err) {
      console.error('Failed to paste:', err);
    }
  }, [content, selectionStart, selectionEnd, handleContentChange]);

  // View operations
  const handleToggleWordWrap = useCallback(() => {
    setWordWrap(prev => !prev);
  }, []);

  const handleToggleLineNumbers = useCallback(() => {
    setLineNumbers(prev => !prev);
  }, []);

  const handleZoomIn = useCallback(() => {
    setFontSize(prev => Math.min(prev + 2, 72));
    setZoomLevel(prev => Math.min(prev + 10, 300));
  }, []);

  const handleZoomOut = useCallback(() => {
    setFontSize(prev => Math.max(prev - 2, 8));
    setZoomLevel(prev => Math.max(prev - 10, 50));
  }, []);

  const handleZoomReset = useCallback(() => {
    setFontSize(14);
    setZoomLevel(100);
  }, []);

  // Format operations
  const handleToggleBold = useCallback(() => {
    setIsBold(prev => !prev);
  }, []);

  const handleToggleItalic = useCallback(() => {
    setIsItalic(prev => !prev);
  }, []);

  const handleToggleUnderline = useCallback(() => {
    setIsUnderlined(prev => !prev);
  }, []);

  // Find/Replace operations
  const handleFind = useCallback(() => {
    setShowFind(true);
  }, []);

  const handleReplace = useCallback(() => {
    setShowFind(true);
  }, []);

  const handleFindClose = useCallback(() => {
    setShowFind(false);
    setFindText("");
    setReplaceText("");
  }, []);

  // Window operations
  const handleMinimize = useCallback(() => {
    console.log('Window minimized');
  }, []);

  const handleMaximize = useCallback(() => {
    setIsMaximized(prev => !prev);
  }, []);

  const handleClose = useCallback(() => {
    if (isModified) {
      const shouldSave = window.confirm('Do you want to save changes before closing?');
      if (shouldSave) {
        handleSaveFile();
      }
    }
    navigate('/desktop-environment');
  }, [isModified, navigate, handleSaveFile]);

  // Keyboard shortcuts
  useEffect(() => {
    const handleKeyDown = (e) => {
      if (e?.ctrlKey || e?.metaKey) {
        switch (e?.key?.toLowerCase()) {
          case 'n':
            e?.preventDefault();
            handleNewFile();
            break;
          case 'o':
            e?.preventDefault();
            handleOpenFile();
            break;
          case 's':
            e?.preventDefault();
            if (e?.shiftKey) {
              handleSaveAsFile();
            } else {
              handleSaveFile();
            }
            break;
          case 'z':
            e?.preventDefault();
            if (e?.shiftKey) {
              handleRedo();
            } else {
              handleUndo();
            }
            break;
          case 'y':
            e?.preventDefault();
            handleRedo();
            break;
          case 'x':
            e?.preventDefault();
            handleCut();
            break;
          case 'c':
            e?.preventDefault();
            handleCopy();
            break;
          case 'v':
            e?.preventDefault();
            handlePaste();
            break;
          case 'f':
            e?.preventDefault();
            handleFind();
            break;
          case 'h':
            e?.preventDefault();
            handleReplace();
            break;
          case 'b':
            e?.preventDefault();
            handleToggleBold();
            break;
          case 'i':
            e?.preventDefault();
            handleToggleItalic();
            break;
          case 'u':
            e?.preventDefault();
            handleToggleUnderline();
            break;
          case '=': case'+':
            e?.preventDefault();
            handleZoomIn();
            break;
          case '-':
            e?.preventDefault();
            handleZoomOut();
            break;
          case '0':
            e?.preventDefault();
            handleZoomReset();
            break;
        }
      }
    };

    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [
    handleNewFile, handleOpenFile, handleSaveFile, handleSaveAsFile,
    handleUndo, handleRedo, handleCut, handleCopy, handlePaste,
    handleFind, handleReplace, handleToggleBold, handleToggleItalic,
    handleToggleUnderline, handleZoomIn, handleZoomOut, handleZoomReset
  ]);

  // Auto-save cleanup
  useEffect(() => {
    return () => {
      if (autoSaveTimeoutRef?.current) {
        clearTimeout(autoSaveTimeoutRef?.current);
      }
    };
  }, []);

  // Load welcome document on first visit
  useEffect(() => {
    if (!content && !isModified) {
      const welcomeDoc = mockDocuments?.[0];
      setContent(welcomeDoc?.content);
      setFileName(welcomeDoc?.name);
      setOriginalContent(welcomeDoc?.content);
    }
  }, []);

  return (
    <div className={`bg-background text-foreground ${isMaximized ? 'fixed inset-0 z-50' : 'h-screen'} flex flex-col`}>
      {/* Window Controls */}
      <WindowControls
        title={fileName}
        onMinimize={handleMinimize}
        onMaximize={handleMaximize}
        onClose={handleClose}
        isMaximized={isMaximized}
        isModified={isModified}
      />
      {/* Menu Bar */}
      <MenuBar
        onNewFile={handleNewFile}
        onOpenFile={handleOpenFile}
        onSaveFile={handleSaveFile}
        onSaveAsFile={handleSaveAsFile}
        onUndo={handleUndo}
        onRedo={handleRedo}
        onCut={handleCut}
        onCopy={handleCopy}
        onPaste={handlePaste}
        onFind={handleFind}
        onReplace={handleReplace}
        onToggleWordWrap={handleToggleWordWrap}
        onToggleLineNumbers={handleToggleLineNumbers}
        onZoomIn={handleZoomIn}
        onZoomOut={handleZoomOut}
        onZoomReset={handleZoomReset}
        onToggleBold={handleToggleBold}
        onToggleItalic={handleToggleItalic}
        onToggleUnderline={handleToggleUnderline}
        onFontSize={setFontSize}
        onFontFamily={setFontFamily}
        canUndo={undoStack?.length > 0}
        canRedo={redoStack?.length > 0}
        wordWrap={wordWrap}
        lineNumbers={lineNumbers}
        fontSize={fontSize}
        fontFamily={fontFamily}
      />
      {/* Toolbar */}
      <Toolbar
        onNewFile={handleNewFile}
        onOpenFile={handleOpenFile}
        onSaveFile={handleSaveFile}
        onUndo={handleUndo}
        onRedo={handleRedo}
        onCut={handleCut}
        onCopy={handleCopy}
        onPaste={handlePaste}
        onToggleBold={handleToggleBold}
        onToggleItalic={handleToggleItalic}
        onToggleUnderline={handleToggleUnderline}
        onFind={handleFind}
        onReplace={handleReplace}
        canUndo={undoStack?.length > 0}
        canRedo={redoStack?.length > 0}
        isBold={isBold}
        isItalic={isItalic}
        isUnderlined={isUnderlined}
      />
      {/* Editor Area */}
      <EditorArea
        content={content}
        onChange={handleContentChange}
        fontSize={fontSize}
        fontFamily={fontFamily}
        wordWrap={wordWrap}
        lineNumbers={lineNumbers}
        onSelectionChange={handleSelectionChange}
        findText={findText}
        replaceText={replaceText}
        showFind={showFind}
        onFindClose={handleFindClose}
      />
      {/* Status Bar */}
      <StatusBar
        wordCount={wordCount}
        characterCount={characterCount}
        lineCount={lineCount}
        currentLine={currentLine}
        currentColumn={currentColumn}
        isModified={isModified}
        fileName={fileName}
        encoding="UTF-8"
        lineEnding="LF"
        fontSize={fontSize}
        zoomLevel={zoomLevel}
      />
    </div>
  );
};

export default TextEditorApplicationWindow;