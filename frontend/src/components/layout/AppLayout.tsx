import { Outlet } from 'react-router-dom';
import { Sidebar } from './Sidebar';
import { DashboardHeader } from './DashboardHeader';

export function AppLayout() {
  return (
    <div className="grid min-h-screen w-full lg:grid-cols-[auto_1fr]">
      <Sidebar />
      
      <div className="flex flex-col">
        <main className="flex-1 overflow-y-auto bg-slate-50 p-6 sm:p-8">
          <div className="max-w-7xl mx-auto">
            <DashboardHeader />
            <Outlet />
          </div>
        </main>
      </div>
    </div>
  );
}
