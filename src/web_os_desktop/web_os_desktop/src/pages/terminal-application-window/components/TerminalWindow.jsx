import React, { useState, useCallback, useRef, useEffect } from 'react';
import TerminalHeader from './TerminalHeader';
import TerminalOutput from './TerminalOutput';
import TerminalInput from './TerminalInput';

const TerminalWindow = ({ 
  position = { x: 100, y: 100 }, 
  size = { width: 800, height: 500 },
  onClose,
  onMinimize,
  onFocus,
  isMaximized = false,
  onMaximize
}) => {
  const [commandHistory, setCommandHistory] = useState([]);
  const [isExecuting, setIsExecuting] = useState(false);
  const [isDragging, setIsDragging] = useState(false);
  const [isResizing, setIsResizing] = useState(false);
  const [dragStart, setDragStart] = useState({ x: 0, y: 0 });
  const [windowPosition, setWindowPosition] = useState(position);
  const [windowSize, setWindowSize] = useState(size);
  
  const windowRef = useRef(null);

  // Mock terminal commands with realistic responses
  const executeCommand = useCallback(async (command) => {
    const timestamp = Date.now();
    const newEntry = {
      command,
      timestamp,
      loading: true,
      output: "",
      error: false
    };

    setCommandHistory(prev => [...prev, newEntry]);
    setIsExecuting(true);

    // Simulate API delay
    await new Promise(resolve => setTimeout(resolve, 500 + Math.random() * 1000));

    let output = "";
    let error = false;

    const args = command?.split(' ');
    const cmd = args?.[0]?.toLowerCase();

    switch (cmd) {
      case 'help':
        output = `Available commands:
  help          - Show this help message
  ls            - List directory contents
  pwd           - Print working directory
  whoami        - Display current user
  date          - Show current date and time
  clear         - Clear terminal screen
  echo [text]   - Display text
  cat [file]    - Display file contents
  mkdir [dir]   - Create directory
  rm [file]     - Remove file
  cp [src] [dst] - Copy file
  mv [src] [dst] - Move file
  ps            - Show running processes
  top           - Display system processes
  df            - Show disk usage
  free          - Display memory usage
  uname         - System information
  history       - Show command history`;
        break;

      case 'ls':
        output = `total 12
drwxr-xr-x  2 user user 4096 Jul 31 19:35 Documents
drwxr-xr-x  2 user user 4096 Jul 31 19:35 Downloads
drwxr-xr-x  2 user user 4096 Jul 31 19:35 Pictures
-rw-r--r--  1 user user  256 Jul 31 19:35 README.txt
-rw-r--r--  1 user user  512 Jul 31 19:35 config.json`;
        break;

      case 'pwd':
        output = '/home/user';
        break;

      case 'whoami':
        output = 'user';
        break;

      case 'date':
        output = new Date()?.toString();
        break;

      case 'clear':
        setCommandHistory([]);
        setIsExecuting(false);
        return;

      case 'echo':
        output = args?.slice(1)?.join(' ') || '';
        break;

      case 'cat':
        if (args?.[1]) {
          if (args?.[1] === 'README.txt') {
            output = `Welcome to WebOS Terminal!

This is a browser-based terminal emulator that provides
a command-line interface within the desktop environment.

Features:
- Command history navigation
- Tab completion
- Scrollable output
- Resizable window
- Dark theme interface

Type 'help' to see available commands.`;
          } else if (args?.[1] === 'config.json') {
            output = `{
  "terminal": {
    "theme": "dark",
    "fontSize": 14,
    "fontFamily": "JetBrains Mono",
    "cursorBlink": true
  },
  "system": {
    "version": "1.0.0",
    "build": "2025.07.31"
  }
}`;
          } else {
            output = `cat: ${args?.[1]}: No such file or directory`;
            error = true;
          }
        } else {
          output = 'cat: missing file operand';
          error = true;
        }
        break;

      case 'ps':
        output = `  PID TTY          TIME CMD
 1234 pts/0    00:00:01 terminal
 1235 pts/0    00:00:00 webos-desktop
 1236 pts/0    00:00:00 window-manager
 1237 pts/0    00:00:00 system-info`;
        break;

      case 'top':
        output = `Tasks: 4 total,   1 running,   3 sleeping,   0 stopped,   0 zombie
%Cpu(s):  2.3 us,  1.2 sy,  0.0 ni, 96.5 id,  0.0 wa,  0.0 hi,  0.0 si,  0.0 st
MiB Mem :   8192.0 total,   6144.0 free,   1536.0 used,    512.0 buff/cache

  PID USER      PR  NI    VIRT    RES    SHR S  %CPU  %MEM     TIME+ COMMAND
 1234 user      20   0  102400  15360   8192 S   1.3   0.2   0:01.23 terminal
 1235 user      20   0   81920  12288   6144 S   0.7   0.1   0:00.45 webos-desktop`;
        break;

      case 'df':
        output = `Filesystem     1K-blocks    Used Available Use% Mounted on
/dev/sda1       20971520 8388608  12582912  40% /
tmpfs            4194304       0   4194304   0% /dev/shm
/dev/sda2       10485760 2097152   8388608  20% /home`;
        break;

      case 'free':
        output = `              total        used        free      shared  buff/cache   available
Mem:        8388608     1572864     6291456           0      524288     6815744
Swap:       2097152           0     2097152`;
        break;

      case 'uname':
        if (args?.[1] === '-a') {
          output = 'WebOS 1.0.0 webos-desktop x86_64 x86_64 x86_64 GNU/Linux';
        } else {
          output = 'WebOS';
        }
        break;

      case 'history':
        output = commandHistory?.filter(entry => !entry?.loading)?.map((entry, index) => `${index + 1}  ${entry?.command}`)?.join('\n');
        break;

      case 'mkdir':
        if (args?.[1]) {
          output = `Directory '${args?.[1]}' created successfully`;
        } else {
          output = 'mkdir: missing operand';
          error = true;
        }
        break;

      case 'rm':
        if (args?.[1]) {
          output = `File '${args?.[1]}' removed successfully`;
        } else {
          output = 'rm: missing operand';
          error = true;
        }
        break;

      case 'cp':
        if (args?.[1] && args?.[2]) {
          output = `'${args?.[1]}' copied to '${args?.[2]}'`;
        } else {
          output = 'cp: missing file operand';
          error = true;
        }
        break;

      case 'mv':
        if (args?.[1] && args?.[2]) {
          output = `'${args?.[1]}' moved to '${args?.[2]}'`;
        } else {
          output = 'mv: missing file operand';
          error = true;
        }
        break;

      default:
        output = `bash: ${command}: command not found`;
        error = true;
        break;
    }

    setCommandHistory(prev => 
      prev?.map(entry => 
        entry?.timestamp === timestamp 
          ? { ...entry, output, error, loading: false }
          : entry
      )
    );
    setIsExecuting(false);
  }, [commandHistory]);

  // Window dragging functionality
  const handleMouseDown = useCallback((e) => {
    if (e?.target?.closest('.window-controls')) return;
    
    setIsDragging(true);
    setDragStart({
      x: e?.clientX - windowPosition?.x,
      y: e?.clientY - windowPosition?.y
    });
    onFocus?.();
  }, [windowPosition, onFocus]);

  const handleMouseMove = useCallback((e) => {
    if (!isDragging) return;

    const newX = e?.clientX - dragStart?.x;
    const newY = Math.max(0, e?.clientY - dragStart?.y);

    setWindowPosition({ x: newX, y: newY });
  }, [isDragging, dragStart]);

  const handleMouseUp = useCallback(() => {
    setIsDragging(false);
  }, []);

  useEffect(() => {
    if (isDragging) {
      document.addEventListener('mousemove', handleMouseMove);
      document.addEventListener('mouseup', handleMouseUp);
      return () => {
        document.removeEventListener('mousemove', handleMouseMove);
        document.removeEventListener('mouseup', handleMouseUp);
      };
    }
  }, [isDragging, handleMouseMove, handleMouseUp]);

  const windowStyle = isMaximized 
    ? { 
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 64,
        width: 'auto',
        height: 'auto',
        zIndex: 1000
      }
    : {
        position: 'absolute',
        left: windowPosition?.x,
        top: windowPosition?.y,
        width: windowSize?.width,
        height: windowSize?.height,
        zIndex: 1000
      };

  return (
    <div
      ref={windowRef}
      className="app-window bg-slate-800 border border-slate-700 rounded-lg overflow-hidden shadow-2xl"
      style={windowStyle}
      onClick={onFocus}
    >
      <div 
        className="cursor-move"
        onMouseDown={handleMouseDown}
      >
        <TerminalHeader
          onMinimize={onMinimize}
          onMaximize={onMaximize}
          onClose={onClose}
          isMaximized={isMaximized}
        />
      </div>
      <div className="flex flex-col h-full">
        <TerminalOutput commandHistory={commandHistory} />
        <TerminalInput
          onExecuteCommand={executeCommand}
          commandHistory={commandHistory?.filter(entry => !entry?.loading)}
          disabled={isExecuting}
        />
      </div>
    </div>
  );
};

export default TerminalWindow;