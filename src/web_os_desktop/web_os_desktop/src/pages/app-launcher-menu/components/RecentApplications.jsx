import React from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const RecentApplications = ({ recentApps, onAppLaunch }) => {
  if (!recentApps || recentApps?.length === 0) {
    return null;
  }

  return (
    <div className="mb-6">
      <h3 className="text-sm font-medium text-slate-400 mb-3 uppercase tracking-wide">
        Recently Used
      </h3>
      <div className="flex space-x-2 overflow-x-auto pb-2">
        {recentApps?.map((app) => (
          <Button
            key={`recent-${app?.id}`}
            variant="ghost"
            onClick={() => onAppLaunch(app)}
            className="flex-shrink-0 flex flex-col items-center space-y-2 p-3 hover:bg-slate-700/50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-slate-800 rounded-lg min-w-[80px]"
          >
            <Icon name={app?.icon} size={32} className="text-indigo-400" />
            <span className="text-xs text-slate-300 text-center truncate max-w-full">
              {app?.name}
            </span>
          </Button>
        ))}
      </div>
    </div>
  );
};

export default RecentApplications;