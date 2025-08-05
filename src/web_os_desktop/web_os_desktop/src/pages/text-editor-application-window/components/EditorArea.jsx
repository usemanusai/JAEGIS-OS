import React, { useRef, useEffect, useState } from 'react';

const EditorArea = ({ 
  content, 
  onChange, 
  fontSize, 
  fontFamily, 
  wordWrap, 
  lineNumbers, 
  onSelectionChange,
  findText,
  replaceText,
  showFind,
  onFindClose
}) => {
  const textareaRef = useRef(null);
  const lineNumbersRef = useRef(null);
  const [selectionStart, setSelectionStart] = useState(0);
  const [selectionEnd, setSelectionEnd] = useState(0);
  const [scrollTop, setScrollTop] = useState(0);

  const lines = content?.split('\n');
  const lineCount = lines?.length;

  useEffect(() => {
    if (lineNumbersRef?.current && textareaRef?.current) {
      lineNumbersRef.current.scrollTop = textareaRef?.current?.scrollTop;
    }
  }, [scrollTop]);

  useEffect(() => {
    if (textareaRef?.current && onSelectionChange) {
      const textarea = textareaRef?.current;
      const start = textarea?.selectionStart;
      const end = textarea?.selectionEnd;
      setSelectionStart(start);
      setSelectionEnd(end);
      onSelectionChange(start, end);
    }
  }, [content, onSelectionChange]);

  const handleScroll = (e) => {
    const scrollTop = e?.target?.scrollTop;
    setScrollTop(scrollTop);
    if (lineNumbersRef?.current) {
      lineNumbersRef.current.scrollTop = scrollTop;
    }
  };

  const handleSelectionChange = () => {
    if (textareaRef?.current && onSelectionChange) {
      const textarea = textareaRef?.current;
      const start = textarea?.selectionStart;
      const end = textarea?.selectionEnd;
      setSelectionStart(start);
      setSelectionEnd(end);
      onSelectionChange(start, end);
    }
  };

  const getLineHeight = () => {
    return Math.max(fontSize * 1.4, 20);
  };

  const highlightText = (text, searchTerm) => {
    if (!searchTerm || !showFind) return text;
    
    const regex = new RegExp(`(${searchTerm.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
    return text?.replace(regex, '<mark class="bg-yellow-300 text-black">$1</mark>');
  };

  return (
    <div className="flex-1 flex relative bg-background">
      {/* Line Numbers */}
      {lineNumbers && (
        <div 
          ref={lineNumbersRef}
          className="bg-muted/10 border-r border-border text-muted-foreground text-right select-none overflow-hidden"
          style={{
            width: `${Math.max(String(lineCount)?.length * 8 + 16, 40)}px`,
            fontSize: `${fontSize}px`,
            fontFamily: 'monospace',
            lineHeight: `${getLineHeight()}px`
          }}
        >
          <div className="py-2 px-2">
            {Array.from({ length: lineCount }, (_, i) => (
              <div key={i + 1} className="whitespace-nowrap">
                {i + 1}
              </div>
            ))}
          </div>
        </div>
      )}
      {/* Editor */}
      <div className="flex-1 relative">
        <textarea
          ref={textareaRef}
          value={content}
          onChange={(e) => onChange(e?.target?.value)}
          onScroll={handleScroll}
          onSelect={handleSelectionChange}
          onKeyUp={handleSelectionChange}
          onClick={handleSelectionChange}
          className="w-full h-full resize-none outline-none bg-transparent text-foreground p-4 font-mono"
          style={{
            fontSize: `${fontSize}px`,
            fontFamily: fontFamily,
            lineHeight: `${getLineHeight()}px`,
            whiteSpace: wordWrap ? 'pre-wrap' : 'pre',
            wordWrap: wordWrap ? 'break-word' : 'normal',
            overflowWrap: wordWrap ? 'break-word' : 'normal'
          }}
          placeholder="Start typing your document..."
          spellCheck={false}
        />

        {/* Find/Replace Panel */}
        {showFind && (
          <div className="absolute top-4 right-4 bg-surface border border-border rounded-lg shadow-lg p-4 min-w-80 z-10">
            <div className="flex items-center justify-between mb-3">
              <h3 className="text-sm font-medium text-foreground">Find & Replace</h3>
              <button
                onClick={onFindClose}
                className="text-muted-foreground hover:text-foreground"
              >
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2">
                  <line x1="18" y1="6" x2="6" y2="18"></line>
                  <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
              </button>
            </div>
            
            <div className="space-y-2">
              <input
                type="text"
                placeholder="Find..."
                value={findText}
                className="w-full px-3 py-2 bg-input border border-border rounded text-sm text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
              />
              <input
                type="text"
                placeholder="Replace with..."
                value={replaceText}
                className="w-full px-3 py-2 bg-input border border-border rounded text-sm text-foreground placeholder-muted-foreground focus:outline-none focus:ring-2 focus:ring-ring"
              />
              <div className="flex space-x-2">
                <button className="px-3 py-1 bg-primary text-primary-foreground rounded text-sm hover:bg-primary/90">
                  Find Next
                </button>
                <button className="px-3 py-1 bg-secondary text-secondary-foreground rounded text-sm hover:bg-secondary/90">
                  Replace
                </button>
                <button className="px-3 py-1 bg-secondary text-secondary-foreground rounded text-sm hover:bg-secondary/90">
                  Replace All
                </button>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
};

export default EditorArea;