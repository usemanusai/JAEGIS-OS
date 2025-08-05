// useCoreServices.js - React Hook for Core Services Integration
import { useState, useEffect, useCallback } from 'react';
import { coreServiceManager } from '../services/CoreServiceClients';

export function useCoreServices() {
  const [serviceStatuses, setServiceStatuses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    // Initialize core services
    const initializeServices = async () => {
      try {
        await coreServiceManager.initialize();
        setLoading(false);
      } catch (err) {
        setError(err.message);
        setLoading(false);
      }
    };
    
    initializeServices();
    
    // Subscribe to status updates
    const unsubscribe = coreServiceManager.onStatusUpdate((statuses) => {
      setServiceStatuses(statuses);
    });
    
    return () => {
      unsubscribe();
      coreServiceManager.stopHealthMonitoring();
    };
  }, []);
  
  // Get specific service
  const getService = useCallback((serviceName) => {
    return coreServiceManager.getService(serviceName);
  }, []);
  
  // Perform health check
  const performHealthCheck = useCallback(async () => {
    try {
      setLoading(true);
      await coreServiceManager.performHealthChecks();
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  }, []);
  
  // Get service status by name
  const getServiceStatus = useCallback((serviceName) => {
    return serviceStatuses.find(status => 
      status.service.toLowerCase() === serviceName.toLowerCase()
    );
  }, [serviceStatuses]);
  
  // Check if all services are healthy
  const allServicesHealthy = useCallback(() => {
    return serviceStatuses.every(status => status.status === 'healthy');
  }, [serviceStatuses]);
  
  // Get healthy services count
  const getHealthyServicesCount = useCallback(() => {
    return serviceStatuses.filter(status => status.status === 'healthy').length;
  }, [serviceStatuses]);
  
  return {
    serviceStatuses,
    loading,
    error,
    getService,
    performHealthCheck,
    getServiceStatus,
    allServicesHealthy,
    getHealthyServicesCount,
    totalServices: serviceStatuses.length
  };
}

// Hook for specific service
export function useService(serviceName) {
  const { getService, getServiceStatus } = useCoreServices();
  
  const service = getService(serviceName);
  const status = getServiceStatus(serviceName);
  
  return {
    service,
    status,
    isHealthy: status?.status === 'healthy',
    isAvailable: !!service
  };
}

// Hook for S.C.R.I.P.T. service
export function useSCRIPT() {
  return useService('script');
}

// Hook for A.T.L.A.S. service
export function useATLAS() {
  return useService('atlas');
}

// Hook for H.E.L.M. service
export function useHELM() {
  return useService('helm');
}

// Hook for M.A.S.T.R. service
export function useMASTR() {
  return useService('mastr');
}

// Hook for A.S.C.E.N.D. service
export function useASCEND() {
  return useService('ascend');
}

// Hook for C.O.R.I. service
export function useCORI() {
  return useService('cori');
}

// Hook for N.L.D.S. service
export function useNLDS() {
  return useService('nlds');
}
