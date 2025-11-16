import { AlertHub } from "../insights/AlertHub";

export function DashboardHeader() {
  return (
    <div className="flex items-center justify-between border-b border-slate-200/80 pb-5 mb-8">
      <div>
        <h1 className="text-2xl font-bold text-slate-900">
          Visão Geral
        </h1>
        <p className="text-sm text-slate-600 mt-1">
          Projeção até Dez/2027 • <span className="text-green-600 font-medium">✓ Dados atualizados</span>
        </p>
      </div>
      
      <div className="flex items-center gap-4">
        <div className="flex items-center gap-2 bg-white rounded-lg border border-slate-200 p-1 shadow-sm">
          <button className="px-3 py-1.5 text-sm font-medium rounded-md bg-slate-900 text-white">
            Realista
          </button>
          <button className="px-3 py-1.5 text-sm text-slate-600 hover:bg-slate-100 rounded-md transition-colors">
            Otimista
          </button>
          <button className="px-3 py-1.5 text-sm text-slate-600 hover:bg-slate-100 rounded-md transition-colors">
            Pessimista
          </button>
        </div>
        <AlertHub />
      </div>
    </div>
  );
}
