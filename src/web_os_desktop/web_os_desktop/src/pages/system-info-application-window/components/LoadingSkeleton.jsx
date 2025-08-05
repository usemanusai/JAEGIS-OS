import React from 'react';

const LoadingSkeleton = () => {
  const SkeletonItem = () => (
    <div className="flex items-center justify-between py-2 border-b border-border/30">
      <div className="h-4 bg-muted/30 rounded w-1/3 animate-pulse"></div>
      <div className="h-4 bg-muted/30 rounded w-1/4 animate-pulse"></div>
    </div>
  );

  const SkeletonSection = ({ title }) => (
    <div className="mb-6 bg-surface/50 rounded-lg border border-border overflow-hidden">
      <div className="flex items-center space-x-3 p-4 bg-muted/10 border-b border-border">
        <div className="w-5 h-5 bg-muted/30 rounded animate-pulse"></div>
        <div className="h-5 bg-muted/30 rounded w-32 animate-pulse"></div>
      </div>
      <div className="p-4 space-y-2">
        {[...Array(4)]?.map((_, i) => (
          <SkeletonItem key={i} />
        ))}
      </div>
    </div>
  );

  return (
    <div className="space-y-6">
      {/* Header Skeleton */}
      <div className="flex items-center justify-between mb-6 pb-4 border-b border-border">
        <div>
          <div className="h-8 bg-muted/30 rounded w-48 mb-2 animate-pulse"></div>
          <div className="h-4 bg-muted/30 rounded w-32 animate-pulse"></div>
        </div>
        <div className="h-10 bg-muted/30 rounded w-24 animate-pulse"></div>
      </div>

      {/* Sections Skeleton */}
      <SkeletonSection />
      <SkeletonSection />
      <SkeletonSection />
      <SkeletonSection />
    </div>
  );
};

export default LoadingSkeleton;