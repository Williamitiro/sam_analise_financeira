import { ConfigurationForm } from "./components/ConfigurationForm";

export function ConfigurationPage() {
  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-slate-900">
          ⚙️ Configuração do Modelo
        </h1>
        <p className="text-sm text-slate-600 mt-1">
          Ajuste as premissas e os parâmetros para simular cenários financeiros.
        </p>
      </div>
      <ConfigurationForm />
    </div>
  );
}
