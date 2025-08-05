import React, { useEffect, useRef } from 'react';

const TerminalOutput = ({ commandHistory }) => {
  const outputRef = useRef(null);

  useEffect(() => {
    if (outputRef?.current) {
      outputRef.current.scrollTop = outputRef?.current?.scrollHeight;
    }
  }, [commandHistory]);

  const formatTimestamp = (timestamp) => {
    return new Date(timestamp)?.toLocaleTimeString('en-US', {
      hour12: false,
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit'
    });
  };

  return (
    <div 
      ref={outputRef}
      className="flex-1 overflow-y-auto p-4 bg-slate-900 text-green-400 font-mono text-sm leading-relaxed"
    >
      {commandHistory?.length === 0 ? (
        <div className="text-slate-500">
          <div className="mb-2">WebOS Terminal v1.0.0</div>
          <div className="mb-2">Type 'help' for available commands</div>
          <div className="mb-4">---</div>
        </div>
      ) : (
        commandHistory?.map((entry, index) => (
          <div key={index} className="mb-3">
            <div className="flex items-center text-cyan-400 mb-1">
              <span className="text-slate-500 mr-2">[{formatTimestamp(entry?.timestamp)}]</span>
              <span className="text-green-400">user@webos:~$</span>
              <span className="ml-2 text-white">{entry?.command}</span>
            </div>
            
            {entry?.output && (
              <div className="ml-4 whitespace-pre-wrap">
                {entry?.error ? (
                  <span className="text-red-400">{entry?.output}</span>
                ) : (
                  <span className="text-green-300">{entry?.output}</span>
                )}
              </div>
            )}
            
            {entry?.loading && (
              <div className="ml-4 text-yellow-400 flex items-center">
                <div className="animate-spin mr-2">⟳</div>
                Executing command...
              </div>
            )}
          </div>
        ))
      )}
    </div>
  );
};

export default TerminalOutput;