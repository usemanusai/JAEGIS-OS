import React from "react";
import { BrowserRouter, Routes as RouterRoutes, Route } from "react-router-dom";
import ScrollToTop from "components/ScrollToTop";
import ErrorBoundary from "components/ErrorBoundary";
import NotFound from "pages/NotFound";
import TextEditorApplicationWindow from './pages/text-editor-application-window';
import AppLauncherMenu from './pages/app-launcher-menu';
import FileExplorerApplicationWindow from './pages/file-explorer-application-window';
import SystemInfoApplicationWindow from './pages/system-info-application-window';
import TerminalApplicationWindow from './pages/terminal-application-window';
import DesktopEnvironment from './pages/desktop-environment';

const Routes = () => {
  return (
    <BrowserRouter>
      <ErrorBoundary>
      <ScrollToTop />
      <RouterRoutes>
        {/* Define your route here */}
        <Route path="/" element={<DesktopEnvironment />} />
        <Route path="/text-editor-application-window" element={<TextEditorApplicationWindow />} />
        <Route path="/app-launcher-menu" element={<AppLauncherMenu />} />
        <Route path="/file-explorer-application-window" element={<FileExplorerApplicationWindow />} />
        <Route path="/system-info-application-window" element={<SystemInfoApplicationWindow />} />
        <Route path="/terminal-application-window" element={<TerminalApplicationWindow />} />
        <Route path="/desktop-environment" element={<DesktopEnvironment />} />
        <Route path="*" element={<NotFound />} />
      </RouterRoutes>
      </ErrorBoundary>
    </BrowserRouter>
  );
};

export default Routes;
