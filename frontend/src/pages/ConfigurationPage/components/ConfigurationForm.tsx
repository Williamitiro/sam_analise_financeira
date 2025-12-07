// frontend/src/pages/ConfigurationPage/components/ConfigurationForm.tsx
import { Button } from "@/components/ui/Button";
import {
  Card,
  CardContent,
  CardDescription,
  CardFooter,
  CardHeader,
  CardTitle,
} from "@/components/ui/Card";
import { Input } from "@/components/ui/Input";
import { Label } from "@/components/ui/Label";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/Table";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";
import { useToast } from "@/hooks/use-toast";
import { useConfigurationStore } from "@/stores/configurationStore";
import { useProjectionStore } from "@/stores/projectionStore";
import { Loader2, PlusCircle } from "lucide-react";

export function ConfigurationForm() {
  const { config, setConfig } = useConfigurationStore();
  const { runProjection, isLoading } = useProjectionStore();
  const { toast } = useToast();

  const handleNumberChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const { name, value } = e.target;
    setConfig({ [name]: Number(value) });
  };

  const handleSave = async () => {
    toast({
      title: "Salvando e recalculando...",
      description: "A nova projeção está sendo gerada com base nas suas alterações.",
    });
    try {
      await runProjection(config);
      toast({
        title: "Sucesso!",
        description: "Projeção atualizada com sucesso.",
        variant: "success",
      });
    } catch (error) {
      toast({
        title: "Erro ao recalcular",
        description: "Não foi possível gerar a projeção. Tente novamente.",
        variant: "destructive",
      });
    }
  };
  
  const SaveButton = () => (
    <Button onClick={handleSave} disabled={isLoading}>
      {isLoading && <Loader2 className="mr-2 h-4 w-4 animate-spin" />}
      {isLoading ? "Salvando..." : "Salvar e Recalcular"}
    </Button>
  );

  return (
    <Tabs defaultValue="geral" className="w-full">
      <TabsList className="grid w-full grid-cols-4">
        <TabsTrigger value="geral">Geral</TabsTrigger>
        <TabsTrigger value="receita">Receita</TabsTrigger>
        <TabsTrigger value="custos">Custos</TabsTrigger>
        <TabsTrigger value="equipe">Equipe</TabsTrigger>
      </TabsList>

      <TabsContent value="geral">
        <Card>
          <CardHeader>
            <CardTitle>Capital e Financiamento</CardTitle>
            <CardDescription>
              Defina o capital inicial e os aportes para a projeção.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="space-y-2">
                <Label htmlFor="capital_inicial_caixa">Capital Inicial (R$)</Label>
                <Input
                  id="capital_inicial_caixa"
                  name="capital_inicial_caixa"
                  type="number"
                  value={config.capital_inicial_caixa}
                  onChange={handleNumberChange}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="aporte_mensal_fixo">Aporte Mensal (R$)</Label>
                <Input
                  id="aporte_mensal_fixo"
                  name="aporte_mensal_fixo"
                  type="number"
                  value={config.aporte_mensal_fixo}
                  onChange={handleNumberChange}
                />
              </div>
              <div className="space-y-2">
                <Label htmlFor="meses_aporte_fixo">Meses de Aporte</Label>
                <Input
                  id="meses_aporte_fixo"
                  name="meses_aporte_fixo"
                  type="number"
                  value={config.meses_aporte_fixo}
                  onChange={handleNumberChange}
                />
              </div>
            </div>
          </CardContent>
          <CardFooter>
            <SaveButton />
          </CardFooter>
        </Card>
      </TabsContent>

      <TabsContent value="receita">
        <Card>
          <CardHeader>
            <CardTitle>Receita</CardTitle>
            <CardDescription>
              Configure o funil de aquisição e o modelo de precificação.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-8">
            {/* Seção Funil de Aquisição */}
            <div className="space-y-4">
              <h3 className="text-md font-medium text-slate-800">Funil de Aquisição</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="visitantes_mes_1">Visitantes Iniciais</Label>
                  <Input id="visitantes_mes_1" name="visitantes_mes_1" type="number" value={config.visitantes_mes_1} onChange={handleNumberChange} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="taxa_crescimento_trafego_mensal">Crescimento do Tráfego (%)</Label>
                  <Input id="taxa_crescimento_trafego_mensal" name="taxa_crescimento_trafego_mensal" type="number" step="0.01" value={config.taxa_crescimento_trafego_mensal} onChange={handleNumberChange} />
                </div>
                 <div className="space-y-2">
                  <Label htmlFor="churn_mensal">Churn Mensal (%)</Label>
                  <Input id="churn_mensal" name="churn_mensal" type="number" step="0.01" value={config.churn_mensal} onChange={handleNumberChange} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="taxa_conversao_visitante_trial">Conversão Visitante → Trial (%)</Label>
                  <Input id="taxa_conversao_visitante_trial" name="taxa_conversao_visitante_trial" type="number" step="0.01" value={config.taxa_conversao_visitante_trial} onChange={handleNumberChange} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="taxa_conversao_trial_pagante">Conversão Trial → Pagante (%)</Label>
                  <Input id="taxa_conversao_trial_pagante" name="taxa_conversao_trial_pagante" type="number" step="0.01" value={config.taxa_conversao_trial_pagante} onChange={handleNumberChange} />
                </div>
              </div>
            </div>
            
            {/* Seção Modelo de Precificação */}
            <div className="space-y-4">
              <h3 className="text-md font-medium text-slate-800">Modelo de Precificação</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                 <div className="space-y-2">
                  <Label htmlFor="preco_plano_lite">Preço Lite (R$)</Label>
                  <Input id="preco_plano_lite" name="preco_plano_lite" type="number" value={config.preco_plano_lite} onChange={handleNumberChange} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="preco_plano_trader">Preço Trader (R$)</Label>
                  <Input id="preco_plano_trader" name="preco_plano_trader" type="number" value={config.preco_plano_trader} onChange={handleNumberChange} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="preco_plano_pro">Preço Pro (R$)</Label>
                  <Input id="preco_plano_pro" name="preco_plano_pro" type="number" value={config.preco_plano_pro} onChange={handleNumberChange} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="mix_plano_lite">Mix Plano Lite (%)</Label>
                  <Input id="mix_plano_lite" name="mix_plano_lite" type="number" step="0.01" value={config.mix_plano_lite} onChange={handleNumberChange} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="mix_plano_trader">Mix Plano Trader (%)</Label>
                  <Input id="mix_plano_trader" name="mix_plano_trader" type="number" step="0.01" value={config.mix_plano_trader} onChange={handleNumberChange} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="mix_plano_pro">Mix Plano Pro (%)</Label>
                  <Input id="mix_plano_pro" name="mix_plano_pro" type="number" step="0.01" value={config.mix_plano_pro} onChange={handleNumberChange} />
                </div>
              </div>
            </div>
          </CardContent>
          <CardFooter>
            <SaveButton />
          </CardFooter>
        </Card>
      </TabsContent>

      <TabsContent value="custos">
        <Card>
          <CardHeader>
            <CardTitle>Custos</CardTitle>
            <CardDescription>
              Configure os custos variáveis, fixos e de infraestrutura.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-8">
            {/* Seção Custos Variáveis (COGS) */}
            <div className="space-y-4">
              <h3 className="text-md font-medium text-slate-800">Custos Variáveis (COGS)</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
                <div className="space-y-2">
                  <Label htmlFor="custo_ia_por_usuario">Custo de IA / Usuário (R$)</Label>
                  <Input id="custo_ia_por_usuario" name="custo_ia_por_usuario" type="number" value={config.custo_ia_por_usuario} onChange={handleNumberChange} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="aliquota_impostos">Impostos (%)</Label>
                  <Input id="aliquota_impostos" name="aliquota_impostos" type="number" step="0.01" value={config.aliquota_impostos} onChange={handleNumberChange} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="taxa_pagamento_percentual">Taxa de Pagamento (%)</Label>
                  <Input id="taxa_pagamento_percentual" name="taxa_pagamento_percentual" type="number" step="0.001" value={config.taxa_pagamento_percentual} onChange={handleNumberChange} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="taxa_pagamento_fixa_por_transacao">Taxa Fixa de Pagamento (R$)</Label>
                  <Input id="taxa_pagamento_fixa_por_transacao" name="taxa_pagamento_fixa_por_transacao" type="number" step="0.01" value={config.taxa_pagamento_fixa_por_transacao} onChange={handleNumberChange} />
                </div>
              </div>
            </div>
            
            {/* Seção Serviços Profissionais */}
            <div className="space-y-4">
              <h3 className="text-md font-medium text-slate-800">Serviços Profissionais</h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                 <div className="space-y-2">
                  <Label htmlFor="contabilidade_mensal">Contabilidade (R$ / Mês)</Label>
                  <Input id="contabilidade_mensal" name="contabilidade_mensal" type="number" value={config.contabilidade_mensal} onChange={handleNumberChange} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="advogado_retainer_mensal">Advocacia (R$ / Mês)</Label>
                  <Input id="advogado_retainer_mensal" name="advogado_retainer_mensal" type="number" value={config.advogado_retainer_mensal} onChange={handleNumberChange} />
                </div>
                <div className="space-y-2">
                  <Label htmlFor="consultorias_outras_mensal">Consultorias (R$ / Mês)</Label>
                  <Input id="consultorias_outras_mensal" name="consultorias_outras_mensal" type="number" value={config.consultorias_outras_mensal} onChange={handleNumberChange} />
                </div>
              </div>
            </div>
          </CardContent>
          <CardFooter>
            <SaveButton />
          </CardFooter>
        </Card>
      </TabsContent>

       <TabsContent value="equipe">
        <Card>
          <CardHeader>
            <CardTitle>Equipe</CardTitle>
            <CardDescription>
              Gerencie os membros da equipe e seus custos.
            </CardDescription>
          </CardHeader>
          <CardContent className="space-y-4">
            <p>Formulário de equipe aqui.</p>
          </CardContent>
          <CardFooter>
            <SaveButton />
          </CardFooter>
        </Card>
      </TabsContent>
    </Tabs>
  );
}
