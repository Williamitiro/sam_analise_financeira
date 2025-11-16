import { Bell, Menu } from 'lucide-react';

interface HeaderProps {
  onMenuClick: () => void;
}

export function Header({ onMenuClick }: HeaderProps) {
  return (
    <header className="sticky top-0 z-30 flex h-14 items-center gap-4 border-b bg-white px-4 sm:static sm:h-auto sm:border-0 sm:bg-transparent sm:px-6">
      <button
        onClick={onMenuClick}
        className="lg:hidden p-2 -ml-2 text-gray-600 hover:text-gray-900"
      >
        <Menu size={24} />
        <span className="sr-only">Abrir menu</span>
      </button>
      <div className="flex-1">
        <h1 className="font-semibold text-lg">Dashboard de Visão Geral</h1>
      </div>
      <div className="flex items-center gap-4">
        <button className="p-2 text-gray-600 hover:text-gray-900">
          <Bell size={20} />
          <span className="sr-only">Notificações</span>
        </button>
        {/* User menu can be added here */}
      </div>
    </header>
  );
}
