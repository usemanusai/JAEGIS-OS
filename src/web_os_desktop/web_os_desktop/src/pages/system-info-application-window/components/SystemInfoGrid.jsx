import React from 'react';
import SystemInfoItem from './SystemInfoItem';

const SystemInfoGrid = ({ data, columns = 1 }) => {
  if (!data || data?.length === 0) {
    return (
      <div className="text-center py-8 text-muted-foreground">
        <p>No data available</p>
      </div>
    );
  }

  const gridClass = columns === 2 
    ? 'grid grid-cols-1 lg:grid-cols-2 gap-x-8' :'space-y-0';

  return (
    <div className={gridClass}>
      {data?.map((item, index) => (
        <SystemInfoItem
          key={index}
          label={item?.label}
          value={item?.value}
          type={item?.type}
          copyable={item?.copyable}
        />
      ))}
    </div>
  );
};

export default SystemInfoGrid;