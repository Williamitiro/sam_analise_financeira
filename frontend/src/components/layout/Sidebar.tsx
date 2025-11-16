import { useState } from 'react';
import { NavLink } from 'react-router-dom';
import { 
  LayoutDashboard, 
  DollarSign, 
  TrendingDown, 
  Wallet,
  Users,
  Megaphone,
  Target,
  GitCompare,
  Table,
  ChevronLeft,
  ChevronRight,
  Settings,
  BarChart,
} from 'lucide-react';
import { cn } from '@/lib/utils/cn';

interface NavItem {
  id: string;
  label: string;
  icon: React.ReactNode;
  path: string;
  badge?: string;
}

const NAV_ITEMS: NavItem[] = [
  { id: 'overview', label: 'Visão Geral', icon: <LayoutDashboard size={20} />, path: '/' },
  { id: 'revenue', label: 'Receita', icon: <DollarSign size={20} />, path: '/receita' },
  { id: 'costs', label: 'Custos', icon: <TrendingDown size={20} />, path: '/custos' },
  { id: 'cash', label: 'Caixa', icon: <Wallet size={20} />, path: '/caixa' },
  { id: 'team', label: 'Equipe', icon: <Users size={20} />, path: '/equipe', badge: 'Em breve' },
  { id: 'marketing', label: 'Marketing', icon: <Megaphone size={20} />, path: '/marketing', badge: 'Em breve' },
  { id: 'economics', label: 'Unit Economics', icon: <Target size={20} />, path: '/economics', badge: 'Em breve' },
  { id: 'sensitivity', label: 'Sensibilidade', icon: <BarChart size={20} />, path: '/sensibilidade', badge: 'Em breve' },
  { id: 'scenarios', label: 'Cenários', icon: <GitCompare size={20} />, path: '/cenarios', badge: 'Em breve' },
  { id: 'tables', label: 'Tabelas', icon: <Table size={20} />, path: '/tabelas', badge: 'Em breve' },
];

const NavLinkItem = ({ item, isCollapsed }: { item: NavItem; isCollapsed: boolean }) => (
  <NavLink
    to={item.path}
    className={({ isActive }) =>
      cn(
        'flex items-center gap-3 rounded-lg px-3 py-2 text-gray-600 transition-all hover:bg-gray-100 hover:text-gray-900',
        isActive && 'bg-gray-100 text-gray-900 font-semibold',
        isCollapsed && 'justify-center'
      )
    }
  >
    {item.icon}
    {!isCollapsed && <span className="flex-1">{item.label}</span>}
    {item.badge && !isCollapsed && (
      <span className="ml-auto text-xs bg-gray-200 text-gray-600 px-2 py-0.5 rounded-full">
        {item.badge}
      </span>
    )}
  </NavLink>
);

export function Sidebar() {
  const [isCollapsed, setIsCollapsed] = useState(false);

  return (
    <aside className={cn(
      "hidden lg:flex flex-col h-screen bg-white border-r transition-all duration-300 ease-in-out",
      isCollapsed ? "w-20" : "w-64"
    )}>
      <div className="flex items-center justify-between h-16 border-b px-4">
        {!isCollapsed && (
          <h1 className="text-lg font-bold text-primary-600">SAM</h1>
        )}
        <button 
          onClick={() => setIsCollapsed(!isCollapsed)} 
          className="p-2 rounded-md hover:bg-gray-100"
        >
          {isCollapsed ? <ChevronRight size={20} /> : <ChevronLeft size={20} />}
        </button>
      </div>
      <nav className="flex-1 overflow-auto p-2 space-y-1">
        {NAV_ITEMS.map((item) => (
          <NavLinkItem key={item.id} item={item} isCollapsed={isCollapsed} />
        ))}
      </nav>
      <div className="mt-auto p-2 border-t">
        <NavLinkItem 
          item={{ id: 'config', label: 'Configuração', icon: <Settings size={20} />, path: '/configuracao' }}
          isCollapsed={isCollapsed}
        />
      </div>
    </aside>
  );
}
