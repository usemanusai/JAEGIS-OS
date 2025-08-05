import React from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const MenuFooter = () => {
  const handleProfileClick = () => {
    console.log('Profile clicked');
  };

  const handleSettingsClick = () => {
    console.log('Settings clicked');
  };

  const handlePowerClick = () => {
    console.log('Power options clicked');
  };

  return (
    <div className="mt-6 pt-4 border-t border-slate-600">
      <div className="flex justify-between items-center">
        <div className="flex space-x-2">
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={handleProfileClick}
            className="text-slate-400 hover:text-slate-200 hover:bg-slate-700/50"
          >
            <Icon name="User" size={16} className="mr-2" />
            Profile
          </Button>
          <Button 
            variant="ghost" 
            size="sm" 
            onClick={handleSettingsClick}
            className="text-slate-400 hover:text-slate-200 hover:bg-slate-700/50"
          >
            <Icon name="Settings" size={16} className="mr-2" />
            Settings
          </Button>
        </div>
        <Button 
          variant="ghost" 
          size="sm" 
          onClick={handlePowerClick}
          className="text-slate-400 hover:text-red-400 hover:bg-slate-700/50"
        >
          <Icon name="Power" size={16} className="mr-2" />
          Power
        </Button>
      </div>
    </div>
  );
};

export default MenuFooter;