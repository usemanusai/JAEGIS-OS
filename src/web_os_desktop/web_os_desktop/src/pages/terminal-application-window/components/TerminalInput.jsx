import React, { useState, useRef, useEffect } from 'react';

const TerminalInput = ({ onExecuteCommand, commandHistory, disabled }) => {
  const [currentCommand, setCurrentCommand] = useState("");
  const [historyIndex, setHistoryIndex] = useState(-1);
  const [cursorVisible, setCursorVisible] = useState(true);
  const inputRef = useRef(null);

  useEffect(() => {
    const interval = setInterval(() => {
      setCursorVisible(prev => !prev);
    }, 500);

    return () => clearInterval(interval);
  }, []);

  useEffect(() => {
    if (inputRef?.current && !disabled) {
      inputRef?.current?.focus();
    }
  }, [disabled]);

  const handleKeyDown = (e) => {
    if (disabled) return;

    if (e?.key === 'Enter') {
      e?.preventDefault();
      if (currentCommand?.trim()) {
        onExecuteCommand(currentCommand?.trim());
        setCurrentCommand("");
        setHistoryIndex(-1);
      }
    } else if (e?.key === 'ArrowUp') {
      e?.preventDefault();
      const commands = commandHistory?.map(entry => entry?.command);
      if (commands?.length > 0) {
        const newIndex = historyIndex === -1 ? commands?.length - 1 : Math.max(0, historyIndex - 1);
        setHistoryIndex(newIndex);
        setCurrentCommand(commands?.[newIndex]);
      }
    } else if (e?.key === 'ArrowDown') {
      e?.preventDefault();
      const commands = commandHistory?.map(entry => entry?.command);
      if (historyIndex !== -1) {
        const newIndex = Math.min(commands?.length - 1, historyIndex + 1);
        if (newIndex === commands?.length - 1 && historyIndex === commands?.length - 1) {
          setHistoryIndex(-1);
          setCurrentCommand("");
        } else {
          setHistoryIndex(newIndex);
          setCurrentCommand(commands?.[newIndex]);
        }
      }
    } else if (e?.key === 'Tab') {
      e?.preventDefault();
      // Basic tab completion for common commands
      const commonCommands = ['help', 'ls', 'pwd', 'whoami', 'date', 'clear', 'echo', 'cat', 'mkdir', 'rm', 'cp', 'mv'];
      const matches = commonCommands?.filter(cmd => cmd?.startsWith(currentCommand?.toLowerCase()));
      if (matches?.length === 1) {
        setCurrentCommand(matches?.[0]);
      }
    }
  };

  const handleInputChange = (e) => {
    setCurrentCommand(e?.target?.value);
    setHistoryIndex(-1);
  };

  return (
    <div className="border-t border-slate-700 bg-slate-900 p-4">
      <div className="flex items-center text-green-400 font-mono text-sm">
        <span className="text-cyan-400 mr-2">user@webos:~$</span>
        <div className="flex-1 relative">
          <input
            ref={inputRef}
            type="text"
            value={currentCommand}
            onChange={handleInputChange}
            onKeyDown={handleKeyDown}
            disabled={disabled}
            className="w-full bg-transparent border-none outline-none text-white caret-transparent"
            placeholder={disabled ? "Executing command..." : "Type a command..."}
            autoComplete="off"
            spellCheck="false"
          />
          <span 
            className={`absolute left-0 top-0 pointer-events-none text-white ${cursorVisible ? 'opacity-100' : 'opacity-0'}`}
            style={{ left: `${currentCommand?.length * 0.6}em` }}
          >
            █
          </span>
        </div>
      </div>
      <div className="mt-2 text-xs text-slate-500">
        Press Tab for command completion • Use ↑↓ arrows for command history • Type 'help' for available commands
      </div>
    </div>
  );
};

export default TerminalInput;