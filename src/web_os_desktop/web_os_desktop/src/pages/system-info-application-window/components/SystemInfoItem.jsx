import React, { useState } from 'react';

const SystemInfoItem = ({ label, value, type = 'text', copyable = false }) => {
  const [copied, setCopied] = React.useState(false);

  const handleCopy = async () => {
    if (copyable && value) {
      try {
        await navigator.clipboard?.writeText(value?.toString());
        setCopied(true);
        setTimeout(() => setCopied(false), 2000);
      } catch (err) {
        console.error('Failed to copy:', err);
      }
    }
  };

  const formatValue = (val, valueType) => {
    if (!val && val !== 0) return 'N/A';
    
    switch (valueType) {
      case 'bytes':
        const bytes = parseInt(val);
        if (bytes >= 1024 ** 3) return `${(bytes / (1024 ** 3))?.toFixed(2)} GB`;
        if (bytes >= 1024 ** 2) return `${(bytes / (1024 ** 2))?.toFixed(2)} MB`;
        if (bytes >= 1024) return `${(bytes / 1024)?.toFixed(2)} KB`;
        return `${bytes} B`;
      case 'percentage':
        return `${parseFloat(val)?.toFixed(1)}%`;
      case 'uptime':
        const hours = Math.floor(val / 3600);
        const minutes = Math.floor((val % 3600) / 60);
        return `${hours}h ${minutes}m`;
      case 'date':
        return new Date(val)?.toLocaleDateString('en-US', {
          month: 'short',
          day: 'numeric',
          year: 'numeric',
          hour: '2-digit',
          minute: '2-digit',
          hour12: true
        });
      default:
        return val?.toString();
    }
  };

  return (
    <div className="flex items-center justify-between py-2 border-b border-border/30 last:border-b-0">
      <span className="text-sm text-muted-foreground font-medium min-w-0 flex-1 mr-4">
        {label}
      </span>
      <div className="flex items-center space-x-2">
        <span 
          className={`
            text-sm text-foreground font-mono text-right
            ${copyable ? 'cursor-pointer hover:text-primary' : ''}
          `}
          onClick={copyable ? handleCopy : undefined}
          title={copyable ? 'Click to copy' : undefined}
        >
          {formatValue(value, type)}
        </span>
        {copyable && (
          <span className={`text-xs transition-opacity ${copied ? 'opacity-100' : 'opacity-0'}`}>
            {copied ? '✓' : ''}
          </span>
        )}
      </div>
    </div>
  );
};

export default SystemInfoItem;