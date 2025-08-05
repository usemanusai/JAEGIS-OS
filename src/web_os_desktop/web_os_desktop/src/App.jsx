import React, { useState, useEffect } from "react";
import Routes from "./Routes";
import LoginForm from "./components/auth/LoginForm";
import { useAuth } from "./hooks/useAuth";
import { appRegistry } from "./services/AppRegistry";

function App() {
  const { isAuthenticated, loading } = useAuth();
  const [appRegistryInitialized, setAppRegistryInitialized] = useState(false);

  useEffect(() => {
    // Initialize app registry when authenticated
    if (isAuthenticated && !appRegistryInitialized) {
      const initializeRegistry = async () => {
        try {
          // We'll pass the window manager once it's available
          await appRegistry.initialize(null);
          setAppRegistryInitialized(true);
          console.log('✅ App Registry initialized');
        } catch (error) {
          console.error('❌ Failed to initialize App Registry:', error);
        }
      };

      initializeRegistry();
    }
  }, [isAuthenticated, appRegistryInitialized]);

  // Show loading screen during initial auth check
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center bg-gray-900">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-500 mx-auto mb-4"></div>
          <p className="text-gray-400">Loading JAEGIS Web OS...</p>
        </div>
      </div>
    );
  }

  // Show login form if not authenticated
  if (!isAuthenticated) {
    return <LoginForm onSuccess={() => console.log('Login successful')} />;
  }

  // Show main application if authenticated
  return (
    <Routes />
  );
}

export default App;
