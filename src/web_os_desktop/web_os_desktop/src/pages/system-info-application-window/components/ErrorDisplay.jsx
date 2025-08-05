import React from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const ErrorDisplay = ({ error, onRetry }) => {
  return (
    <div className="flex flex-col items-center justify-center py-12 text-center">
      <div className="w-16 h-16 bg-error/10 rounded-full flex items-center justify-center mb-4">
        <Icon name="AlertTriangle" size={32} className="text-error" />
      </div>
      
      <h3 className="text-lg font-medium text-foreground mb-2">
        Failed to Load System Information
      </h3>
      
      <p className="text-sm text-muted-foreground mb-6 max-w-md">
        {error?.message || "Unable to retrieve system information. Please check your connection and try again."}
      </p>
      
      <Button
        variant="outline"
        onClick={onRetry}
        iconName="RefreshCw"
        iconPosition="left"
      >
        Try Again
      </Button>
    </div>
  );
};

export default ErrorDisplay;