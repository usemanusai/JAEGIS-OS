import React from 'react';
import Icon from '../../../components/AppIcon';
import Button from '../../../components/ui/Button';

const ApplicationGrid = ({ applications, onAppLaunch, searchTerm = '' }) => {
  const filteredApps = applications?.filter(app =>
    app?.name?.toLowerCase()?.includes(searchTerm?.toLowerCase()) ||
    app?.description?.toLowerCase()?.includes(searchTerm?.toLowerCase())
  );

  const categories = [...new Set(filteredApps.map(app => app.category))];

  const handleKeyDown = (event, app) => {
    if (event.key === 'Enter' || event.key === ' ') {
      event.preventDefault();
      onAppLaunch(app);
    }
  };

  return (
    <div className="overflow-y-auto max-h-80">
      {categories?.map((category) => (
        <div key={category} className="mb-6">
          <h3 className="text-sm font-medium text-slate-400 mb-3 uppercase tracking-wide">
            {category}
          </h3>
          <div className="grid grid-cols-2 gap-2">
            {filteredApps?.filter(app => app?.category === category)?.map((app) => (
                <Button
                  key={app?.id}
                  variant="ghost"
                  onClick={() => onAppLaunch(app)}
                  onKeyDown={(e) => handleKeyDown(e, app)}
                  className="h-auto p-3 flex items-center space-x-3 hover:bg-slate-700/50 focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:ring-offset-2 focus:ring-offset-slate-800 text-left justify-start"
                >
                  <div className="flex-shrink-0">
                    <Icon name={app?.icon} size={24} className="text-indigo-400" />
                  </div>
                  <div className="flex-1 min-w-0">
                    <div className="text-sm font-medium text-slate-50 truncate">
                      {app?.name}
                    </div>
                    <div className="text-xs text-slate-400 truncate">
                      {app?.description}
                    </div>
                  </div>
                </Button>
              ))}
          </div>
        </div>
      ))}
      {filteredApps?.length === 0 && searchTerm && (
        <div className="text-center py-8">
          <Icon name="Search" size={48} className="text-slate-600 mx-auto mb-4" />
          <p className="text-slate-400">No applications found matching "{searchTerm}"</p>
        </div>
      )}
    </div>
  );
};

export default ApplicationGrid;