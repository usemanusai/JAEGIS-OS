import React, { useState } from 'react';
import Icon from '../../../components/AppIcon';

const SystemInfoSection = ({ title, icon, children, isCollapsible = false }) => {
  const [isExpanded, setIsExpanded] = React.useState(true);

  const toggleExpanded = () => {
    if (isCollapsible) {
      setIsExpanded(!isExpanded);
    }
  };

  return (
    <div className="mb-6 bg-surface/50 rounded-lg border border-border overflow-hidden">
      <div 
        className={`
          flex items-center space-x-3 p-4 bg-muted/10 border-b border-border
          ${isCollapsible ? 'cursor-pointer hover:bg-muted/20' : ''}
        `}
        onClick={toggleExpanded}
      >
        <Icon name={icon} size={20} className="text-primary" />
        <h2 className="text-lg font-medium text-foreground flex-1">{title}</h2>
        {isCollapsible && (
          <Icon 
            name={isExpanded ? "ChevronUp" : "ChevronDown"} 
            size={16} 
            className="text-muted-foreground" 
          />
        )}
      </div>
      {isExpanded && (
        <div className="p-4">
          {children}
        </div>
      )}
    </div>
  );
};

export default SystemInfoSection;