import React from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const MenuHeader = ({ onClose }) => {
  return (
    <div className="mb-6">
      <div className="flex items-center justify-between mb-2">
        <h2 className="text-xl font-semibold text-slate-50">Applications</h2>
        <Button
          variant="ghost"
          size="icon"
          onClick={onClose}
          className="w-8 h-8 hover:bg-slate-700/50 text-slate-400 hover:text-slate-200"
        >
          <Icon name="X" size={16} />
        </Button>
      </div>
      <p className="text-sm text-slate-400">Launch your favorite applications</p>
    </div>
  );
};

export default MenuHeader;