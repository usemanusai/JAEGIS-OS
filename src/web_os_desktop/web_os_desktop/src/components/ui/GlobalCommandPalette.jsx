// GlobalCommandPalette.jsx - Global Command Palette with N.L.D.S. Integration
import React, { useState, useEffect, useRef } from 'react';
import { useNLDS } from '../../hooks/useCoreServices';
import { appRegistry } from '../../services/AppRegistry';
import { useWindowManager } from './WindowManager';

const GlobalCommandPalette = ({ isOpen, onClose }) => {
  const [query, setQuery] = useState('');
  const [results, setResults] = useState([]);
  const [selectedIndex, setSelectedIndex] = useState(0);
  const [loading, setLoading] = useState(false);
  const [confidence, setConfidence] = useState(0);
  const [suggestions, setSuggestions] = useState([]);
  const inputRef = useRef(null);
  
  const { service: nldsService, isHealthy: nldsHealthy } = useNLDS();
  const { createWindow } = useWindowManager();
  
  useEffect(() => {
    if (isOpen && inputRef.current) {
      inputRef.current.focus();
    }
  }, [isOpen]);
  
  useEffect(() => {
    if (query.length > 0) {
      processQuery(query);
    } else {
      setResults([]);
      setConfidence(0);
      setSuggestions([]);
    }
  }, [query]);
  
  // Process query with N.L.D.S. and local search
  const processQuery = async (searchQuery) => {
    setLoading(true);
    
    try {
      const localResults = await searchLocalCommands(searchQuery);
      let nldsResults = [];
      let queryConfidence = 0;
      
      // Try N.L.D.S. processing if available
      if (nldsHealthy && nldsService) {
        try {
          const nldsResponse = await nldsService.processCommand(searchQuery);
          queryConfidence = nldsResponse.confidence || 0;
          
          if (queryConfidence >= 0.85) {
            nldsResults = [{
              id: 'nlds-command',
              type: 'nlds',
              title: nldsResponse.intent || 'Execute Command',
              description: `N.L.D.S. Command (${Math.round(queryConfidence * 100)}% confidence)`,
              action: () => executeNLDSCommand(nldsResponse),
              icon: 'Zap',
              confidence: queryConfidence
            }];
          }
          
          // Get suggestions
          const suggestionsResponse = await nldsService.getCommandSuggestions(searchQuery);
          setSuggestions(suggestionsResponse.suggestions || []);
        } catch (error) {
          console.error('N.L.D.S. processing failed:', error);
        }
      }
      
      setConfidence(queryConfidence);
      setResults([...nldsResults, ...localResults]);
    } catch (error) {
      console.error('Query processing failed:', error);
    } finally {
      setLoading(false);
    }
  };
  
  // Search local commands and applications
  const searchLocalCommands = async (searchQuery) => {
    const results = [];
    const query = searchQuery.toLowerCase();
    
    // Search applications
    const apps = appRegistry.getRegisteredApps();
    apps.forEach(app => {
      if (app.name.toLowerCase().includes(query) || 
          app.description.toLowerCase().includes(query)) {
        results.push({
          id: `app-${app.id}`,
          type: 'application',
          title: `Open ${app.name}`,
          description: app.description,
          action: () => launchApplication(app.id),
          icon: app.icon || 'Square',
          category: app.category
        });
      }
    });
    
    // Search system commands
    const systemCommands = [
      {
        id: 'open-settings',
        title: 'Open Settings',
        description: 'System preferences and configuration',
        action: () => openSettings(),
        icon: 'Settings',
        keywords: ['settings', 'preferences', 'config']
      },
      {
        id: 'open-task-manager',
        title: 'Open Task Manager',
        description: 'View running processes and system performance',
        action: () => openTaskManager(),
        icon: 'Activity',
        keywords: ['task', 'manager', 'processes', 'performance']
      },
      {
        id: 'open-file-explorer',
        title: 'Open File Explorer',
        description: 'Browse files and folders',
        action: () => launchApplication('file-explorer'),
        icon: 'Folder',
        keywords: ['files', 'folders', 'explorer', 'browse']
      },
      {
        id: 'open-terminal',
        title: 'Open Terminal',
        description: 'Command line interface',
        action: () => launchApplication('terminal'),
        icon: 'Terminal',
        keywords: ['terminal', 'command', 'cli', 'shell']
      }
    ];
    
    systemCommands.forEach(cmd => {
      if (cmd.title.toLowerCase().includes(query) ||
          cmd.description.toLowerCase().includes(query) ||
          cmd.keywords.some(keyword => keyword.includes(query))) {
        results.push({
          ...cmd,
          type: 'system'
        });
      }
    });
    
    return results.slice(0, 8); // Limit results
  };
  
  // Execute N.L.D.S. command
  const executeNLDSCommand = async (nldsResponse) => {
    try {
      const { intent, parameters } = nldsResponse;
      
      switch (intent) {
        case 'open_application':
          await launchApplication(parameters.appName);
          break;
        case 'create_window':
          createWindow(parameters);
          break;
        case 'system_command':
          await executeSystemCommand(parameters.command);
          break;
        default:
          console.log('Executing N.L.D.S. command:', intent, parameters);
      }
      
      onClose();
    } catch (error) {
      console.error('Failed to execute N.L.D.S. command:', error);
    }
  };
  
  // Launch application
  const launchApplication = async (appId) => {
    try {
      await appRegistry.launchApp(appId);
      onClose();
    } catch (error) {
      console.error('Failed to launch application:', error);
    }
  };
  
  // Execute system command
  const executeSystemCommand = async (command) => {
    console.log('Executing system command:', command);
    // Implementation for system commands
  };
  
  // Open settings
  const openSettings = () => {
    createWindow({
      title: 'Settings',
      component: () => <div className="p-4">Settings Panel</div>,
      icon: 'Settings',
      size: { width: 800, height: 600 }
    });
    onClose();
  };
  
  // Open task manager
  const openTaskManager = () => {
    createWindow({
      title: 'Task Manager',
      component: () => <div className="p-4">Task Manager</div>,
      icon: 'Activity',
      size: { width: 900, height: 700 }
    });
    onClose();
  };
  
  // Handle keyboard navigation
  const handleKeyDown = (e) => {
    switch (e.key) {
      case 'ArrowDown':
        e.preventDefault();
        setSelectedIndex(prev => Math.min(prev + 1, results.length - 1));
        break;
      case 'ArrowUp':
        e.preventDefault();
        setSelectedIndex(prev => Math.max(prev - 1, 0));
        break;
      case 'Enter':
        e.preventDefault();
        if (results[selectedIndex]) {
          results[selectedIndex].action();
        }
        break;
      case 'Escape':
        e.preventDefault();
        onClose();
        break;
    }
  };
  
  // Handle suggestion click
  const handleSuggestionClick = (suggestion) => {
    setQuery(suggestion);
  };
  
  if (!isOpen) return null;
  
  return (
    <div className="fixed inset-0 bg-black bg-opacity-50 flex items-start justify-center pt-20 z-50">
      <div className="bg-gray-800 rounded-lg shadow-2xl w-full max-w-2xl mx-4">
        {/* Search Input */}
        <div className="p-4 border-b border-gray-700">
          <div className="relative">
            <input
              ref={inputRef}
              type="text"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Type a command or search for applications..."
              className="w-full px-4 py-3 bg-gray-700 text-white rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            />
            {loading && (
              <div className="absolute right-3 top-1/2 transform -translate-y-1/2">
                <div className="animate-spin rounded-full h-5 w-5 border-b-2 border-blue-500"></div>
              </div>
            )}
          </div>
          
          {/* Confidence Score */}
          {confidence > 0 && (
            <div className="mt-2 flex items-center space-x-2">
              <span className="text-xs text-gray-400">N.L.D.S. Confidence:</span>
              <div className="flex-1 bg-gray-700 rounded-full h-2">
                <div 
                  className={`h-2 rounded-full ${confidence >= 0.85 ? 'bg-green-500' : confidence >= 0.7 ? 'bg-yellow-500' : 'bg-red-500'}`}
                  style={{ width: `${confidence * 100}%` }}
                ></div>
              </div>
              <span className="text-xs text-gray-400">{Math.round(confidence * 100)}%</span>
            </div>
          )}
        </div>
        
        {/* Results */}
        <div className="max-h-96 overflow-y-auto">
          {results.length > 0 ? (
            results.map((result, index) => (
              <div
                key={result.id}
                onClick={result.action}
                className={`p-4 cursor-pointer border-b border-gray-700 last:border-b-0 ${
                  index === selectedIndex ? 'bg-blue-600' : 'hover:bg-gray-700'
                }`}
              >
                <div className="flex items-center space-x-3">
                  <div className="flex-shrink-0">
                    <div className="w-8 h-8 bg-gray-600 rounded flex items-center justify-center">
                      <span className="text-sm">🔍</span>
                    </div>
                  </div>
                  <div className="flex-1">
                    <div className="text-white font-medium">{result.title}</div>
                    <div className="text-gray-400 text-sm">{result.description}</div>
                    {result.type && (
                      <div className="text-xs text-gray-500 mt-1 capitalize">{result.type}</div>
                    )}
                  </div>
                  {result.confidence && (
                    <div className="text-xs text-gray-400">
                      {Math.round(result.confidence * 100)}%
                    </div>
                  )}
                </div>
              </div>
            ))
          ) : query.length > 0 ? (
            <div className="p-8 text-center text-gray-400">
              No results found for "{query}"
            </div>
          ) : (
            <div className="p-8 text-center text-gray-400">
              Start typing to search applications and commands
            </div>
          )}
        </div>
        
        {/* Suggestions */}
        {suggestions.length > 0 && (
          <div className="p-4 border-t border-gray-700">
            <div className="text-xs text-gray-400 mb-2">Suggestions:</div>
            <div className="flex flex-wrap gap-2">
              {suggestions.slice(0, 5).map((suggestion, index) => (
                <button
                  key={index}
                  onClick={() => handleSuggestionClick(suggestion)}
                  className="px-3 py-1 bg-gray-700 text-gray-300 rounded-full text-xs hover:bg-gray-600 transition-colors"
                >
                  {suggestion}
                </button>
              ))}
            </div>
          </div>
        )}
        
        {/* Footer */}
        <div className="p-3 border-t border-gray-700 text-xs text-gray-500 flex justify-between">
          <span>↑↓ Navigate • Enter Select • Esc Close</span>
          <span>Powered by N.L.D.S.</span>
        </div>
      </div>
    </div>
  );
};

export default GlobalCommandPalette;
