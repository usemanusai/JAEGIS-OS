import React, { useState, useEffect } from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';
import Input from '../../../components/ui/Input';

const FileToolbar = ({ 
  currentPath, 
  onNavigate, 
  onBack, 
  onForward, 
  onUp, 
  canGoBack, 
  canGoForward,
  viewMode,
  onViewModeChange,
  onSearch,
  onRefresh
}) => {
  const [addressBarValue, setAddressBarValue] = useState(currentPath);
  const [isEditingAddress, setIsEditingAddress] = useState(false);
  const [searchQuery, setSearchQuery] = useState('');

  const handleAddressSubmit = (e) => {
    e?.preventDefault();
    onNavigate(addressBarValue);
    setIsEditingAddress(false);
  };

  const handleSearchSubmit = (e) => {
    e?.preventDefault();
    onSearch(searchQuery);
  };

  const pathSegments = currentPath?.split('/')?.filter(segment => segment);

  const handleBreadcrumbClick = (index) => {
    const newPath = '/' + pathSegments?.slice(0, index + 1)?.join('/');
    onNavigate(newPath);
  };

  React.useEffect(() => {
    setAddressBarValue(currentPath);
  }, [currentPath]);

  return (
    <div className="bg-surface border-b border-border p-2 space-y-2">
      {/* Navigation Controls */}
      <div className="flex items-center space-x-2">
        {/* Back/Forward/Up buttons */}
        <div className="flex items-center space-x-1">
          <Button
            variant="ghost"
            size="icon"
            onClick={onBack}
            disabled={!canGoBack}
            className="w-8 h-8"
            title="Back"
          >
            <Icon name="ChevronLeft" size={16} />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={onForward}
            disabled={!canGoForward}
            className="w-8 h-8"
            title="Forward"
          >
            <Icon name="ChevronRight" size={16} />
          </Button>
          <Button
            variant="ghost"
            size="icon"
            onClick={onUp}
            className="w-8 h-8"
            title="Up"
          >
            <Icon name="ChevronUp" size={16} />
          </Button>
        </div>

        <div className="w-px h-6 bg-border" />

        {/* Address Bar */}
        <div className="flex-1">
          {isEditingAddress ? (
            <form onSubmit={handleAddressSubmit} className="flex">
              <Input
                type="text"
                value={addressBarValue}
                onChange={(e) => setAddressBarValue(e?.target?.value)}
                onBlur={() => setIsEditingAddress(false)}
                className="flex-1 h-8 text-sm"
                autoFocus
              />
            </form>
          ) : (
            <div 
              className="flex items-center h-8 px-3 bg-input border border-border rounded-md cursor-text hover:bg-muted/20"
              onClick={() => setIsEditingAddress(true)}
            >
              <Icon name="Folder" size={14} className="mr-2 text-muted-foreground" />
              <div className="flex items-center space-x-1 text-sm overflow-hidden">
                <Button
                  variant="ghost"
                  size="sm"
                  onClick={() => onNavigate('/')}
                  className="h-6 px-2 text-xs hover:bg-primary/20"
                >
                  <Icon name="HardDrive" size={12} className="mr-1" />
                  Root
                </Button>
                {pathSegments?.map((segment, index) => (
                  <React.Fragment key={index}>
                    <Icon name="ChevronRight" size={12} className="text-muted-foreground" />
                    <Button
                      variant="ghost"
                      size="sm"
                      onClick={() => handleBreadcrumbClick(index)}
                      className="h-6 px-2 text-xs hover:bg-primary/20 max-w-32 truncate"
                    >
                      {segment}
                    </Button>
                  </React.Fragment>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Refresh Button */}
        <Button
          variant="ghost"
          size="icon"
          onClick={onRefresh}
          className="w-8 h-8"
          title="Refresh"
        >
          <Icon name="RefreshCw" size={16} />
        </Button>
      </div>
      {/* Search and View Controls */}
      <div className="flex items-center justify-between">
        {/* Search Bar */}
        <form onSubmit={handleSearchSubmit} className="flex items-center space-x-2">
          <div className="relative">
            <Icon 
              name="Search" 
              size={14} 
              className="absolute left-2 top-1/2 transform -translate-y-1/2 text-muted-foreground" 
            />
            <Input
              type="search"
              placeholder="Search files..."
              value={searchQuery}
              onChange={(e) => setSearchQuery(e?.target?.value)}
              className="pl-8 w-64 h-8 text-sm"
            />
          </div>
        </form>

        {/* View Mode Controls */}
        <div className="flex items-center space-x-1">
          <span className="text-xs text-muted-foreground mr-2">View:</span>
          <Button
            variant={viewMode === 'grid' ? 'secondary' : 'ghost'}
            size="icon"
            onClick={() => onViewModeChange('grid')}
            className="w-8 h-8"
            title="Grid View"
          >
            <Icon name="Grid3X3" size={16} />
          </Button>
          <Button
            variant={viewMode === 'list' ? 'secondary' : 'ghost'}
            size="icon"
            onClick={() => onViewModeChange('list')}
            className="w-8 h-8"
            title="List View"
          >
            <Icon name="List" size={16} />
          </Button>
          <Button
            variant={viewMode === 'details' ? 'secondary' : 'ghost'}
            size="icon"
            onClick={() => onViewModeChange('details')}
            className="w-8 h-8"
            title="Details View"
          >
            <Icon name="AlignJustify" size={16} />
          </Button>
        </div>
      </div>
    </div>
  );
};

export default FileToolbar;