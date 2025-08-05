import React from 'react';
import Icon from '../../../components/AppIcon';

const SystemInfoHeader = ({ onRefresh, isLoading, lastUpdated }) => {
  const formatLastUpdated = (date) => {
    return date?.toLocaleString('en-US', {
      month: 'short',
      day: 'numeric',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true
    });
  };

  return (
    <div className="flex items-center justify-between mb-6 pb-4 border-b border-border">
      <div>
        <h1 className="text-2xl font-semibold text-foreground mb-1">System Information</h1>
        <p className="text-sm text-muted-foreground">
          Last updated: {formatLastUpdated(lastUpdated)}
        </p>
      </div>
      <button
        onClick={onRefresh}
        disabled={isLoading}
        className={`
          flex items-center space-x-2 px-4 py-2 rounded-md border border-border
          bg-surface hover:bg-muted/20 text-foreground transition-colors
          ${isLoading ? 'opacity-50 cursor-not-allowed' : 'hover:border-primary/30'}
        `}
      >
        <Icon 
          name="RefreshCw" 
          size={16} 
          className={isLoading ? 'animate-spin' : ''} 
        />
        <span className="text-sm">Refresh</span>
      </button>
    </div>
  );
};

export default SystemInfoHeader;