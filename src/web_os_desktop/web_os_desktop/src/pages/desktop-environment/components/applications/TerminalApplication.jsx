import React, { useState, useRef, useEffect } from 'react';
import Button from '../../../../components/ui/Button';


const TerminalApplication = ({ windowId }) => {
  const [commandHistory, setCommandHistory] = useState([
    { type: 'output', content: 'Web OS Terminal v1.0.0' },
    { type: 'output', content: 'Type "help" for available commands.' },
    { type: 'prompt', content: 'user@webos:~$ ' }
  ]);
  const [currentCommand, setCurrentCommand] = useState('');
  const [isProcessing, setIsProcessing] = useState(false);
  const terminalRef = useRef(null);
  const inputRef = useRef(null);

  const availableCommands = {
    help: 'Available commands: help, sudo, su, clear, date, whoami, pwd, ls, cat, echo, uname, ps, top, history',
    clear: '',
    date: new Date()?.toString(),
    whoami: 'user',
    pwd: '/home/user',
    ls: 'Documents  Downloads  Pictures  Videos  Desktop',
    uname: 'Web OS 1.0.0 (Browser Environment)',
    ps: `PID  COMMAND
1    init
2    terminal
3    file-explorer
4    text-editor`,
    top: `Tasks: 4 total, 1 running, 3 sleeping
%Cpu(s): 12.5 us, 2.1 sy, 0.0 ni, 85.4 id
Memory: 8192MB total, 2048MB used, 6144MB free`,
    history: 'Command history will be shown here'
  };

  useEffect(() => {
    if (terminalRef?.current) {
      terminalRef.current.scrollTop = terminalRef?.current?.scrollHeight;
    }
  }, [commandHistory]);

  useEffect(() => {
    if (inputRef?.current) {
      inputRef?.current?.focus();
    }
  }, []);

  const processCommand = async (command) => {
    const trimmedCommand = command?.trim()?.toLowerCase();
    
    if (trimmedCommand === 'clear') {
      setCommandHistory([
        { type: 'output', content: 'Web OS Terminal v1.0.0' },
        { type: 'output', content: 'Type "help" for available commands.' },
        { type: 'prompt', content: 'user@webos:~$ ' }
      ]);
      return;
    }

    // Add command to history
    setCommandHistory(prev => [
      ...prev,
      { type: 'command', content: `user@webos:~$ ${command}` }
    ]);

    setIsProcessing(true);

    // Simulate processing delay
    await new Promise(resolve => setTimeout(resolve, 300));

    let output = '';
    
    if (trimmedCommand?.startsWith('echo ')) {
      output = command?.substring(5);
    } else if (trimmedCommand?.startsWith('cat ')) {
      const filename = command?.substring(4)?.trim();
      output = `cat: ${filename}: No such file or directory`;
    } else if (availableCommands?.[trimmedCommand]) {
      output = availableCommands?.[trimmedCommand];
    } else if (trimmedCommand === '') {
      // Empty command, just show new prompt
    } else {
      output = `bash: ${trimmedCommand}: command not found`;
    }

    setCommandHistory(prev => [
      ...prev,
      ...(output ? [{ type: 'output', content: output }] : []),
      { type: 'prompt', content: 'user@webos:~$ ' }
    ]);

    setIsProcessing(false);
  };

  const handleSubmit = (e) => {
    e?.preventDefault();
    if (currentCommand?.trim() && !isProcessing) {
      processCommand(currentCommand);
      setCurrentCommand('');
    }
  };

  const handleKeyDown = (e) => {
    if (e?.key === 'Enter') {
      handleSubmit(e);
    } else if (e?.key === 'Tab') {
      e?.preventDefault();
      // Basic tab completion for commands
      const partial = currentCommand?.toLowerCase();
      const matches = Object.keys(availableCommands)?.filter(cmd => cmd?.startsWith(partial));
      if (matches?.length === 1) {
        setCurrentCommand(matches?.[0]);
      }
    }
  };

  return (
    <div className="h-full flex flex-col bg-slate-900 text-green-400 font-mono text-sm">
      {/* Terminal Output */}
      <div 
        ref={terminalRef}
        className="flex-1 overflow-y-auto p-4 space-y-1"
        onClick={() => inputRef?.current?.focus()}
      >
        {commandHistory?.map((entry, index) => (
          <div key={index} className="whitespace-pre-wrap">
            {entry?.type === 'output' && (
              <div className="text-green-300">{entry?.content}</div>
            )}
            {entry?.type === 'command' && (
              <div className="text-green-400">{entry?.content}</div>
            )}
            {entry?.type === 'prompt' && index === commandHistory?.length - 1 && (
              <div className="flex items-center">
                <span className="text-green-400 mr-2">{entry?.content}</span>
                <div className="flex-1">
                  <input
                    ref={inputRef}
                    type="text"
                    value={currentCommand}
                    onChange={(e) => setCurrentCommand(e?.target?.value)}
                    onKeyDown={handleKeyDown}
                    disabled={isProcessing}
                    className="bg-transparent border-none outline-none text-green-400 w-full font-mono"
                    autoComplete="off"
                    spellCheck="false"
                  />
                  {isProcessing && (
                    <span className="text-yellow-400 ml-2">Processing...</span>
                  )}
                </div>
              </div>
            )}
            {entry?.type === 'prompt' && index !== commandHistory?.length - 1 && (
              <div className="text-green-400">{entry?.content}</div>
            )}
          </div>
        ))}
      </div>
      {/* Terminal Footer */}
      <div className="border-t border-slate-700 p-2 bg-slate-800">
        <div className="flex items-center justify-between text-xs text-slate-400">
          <span>Terminal - {windowId}</span>
          <div className="flex items-center space-x-4">
            <span>Lines: {commandHistory?.length}</span>
            <Button
              variant="ghost"
              size="xs"
              onClick={() => processCommand('clear')}
              className="text-slate-400 hover:text-green-400"
            >
              Clear
            </Button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default TerminalApplication;