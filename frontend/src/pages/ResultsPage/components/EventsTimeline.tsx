// frontend/src/pages/ResultsPage/components/EventsTimeline.tsx
import { KPIs, ProjectionData } from '@/types/api.types';
import { formatCurrency } from '@/lib/utils/formatters';
import { Milestone, TrendingUp, UserPlus, Users, Skull, PartyPopper, Flag, MapPin } from 'lucide-react';
import React, { useMemo } from 'react';

interface EventsTimelineProps {
    data: ProjectionData;
    kpis: KPIs;
}

interface TimelineEvent {
    month: number;
    description: string;
    value?: string;
    type: 'critical' | 'milestone' | 'hiring' | 'info';
    icon: React.ReactNode;
}

export const EventsTimeline = ({ data, kpis }: EventsTimelineProps) => {
    const events = useMemo(() => {
        const allEvents: TimelineEvent[] = [];

        // Critical Events from KPIs
        if (kpis.Vale_da_Morte_Month) {
            allEvents.push({
                month: kpis.Vale_da_Morte_Month,
                description: 'Vale da Morte',
                value: formatCurrency(kpis.Vale_da_Morte_Valor),
                type: 'critical',
                icon: <Skull className="w-5 h-5 text-red-500" />
            });
        }
        if (kpis.Breakeven_Month) {
            allEvents.push({
                month: kpis.Breakeven_Month,
                description: 'Break-Even Point',
                value: `MRR: ${formatCurrency(kpis.Breakeven_MRR)}`,
                type: 'milestone',
                icon: <PartyPopper className="w-5 h-5 text-green-500" />
            });
        }

        // Placeholder for "You are here"
        allEvents.push({
            month: 12, // Assuming current month is 12 for demo
            description: 'Você está aqui',
            type: 'info',
            icon: <MapPin className="w-5 h-5 text-blue-500" />
        });
        
        // Placeholder for hiring events - this needs real data logic
        allEvents.push({ month: 6, description: 'Contratação: Designer PJ', value: 'R$3k', type: 'hiring', icon: <UserPlus className="w-5 h-5 text-slate-500" /> });
        allEvents.push({ month: 13, description: 'Contratação: Dev Backend', value: 'R$13.4k', type: 'hiring', icon: <UserPlus className="w-5 h-5 text-slate-500" /> });

        // Placeholder for milestone
        allEvents.push({ month: 24, description: 'MRR > R$50k', type: 'milestone', icon: <TrendingUp className="w-5 h-5 text-indigo-500" /> });


        // Sort events by month
        return allEvents.sort((a, b) => a.month - b.month);

    }, [data, kpis]);

    const TYPE_STYLES = {
        critical: 'border-red-200 bg-red-50 text-red-700',
        milestone: 'border-green-200 bg-green-50 text-green-700',
        hiring: 'border-slate-200 bg-slate-100 text-slate-700',
        info: 'border-blue-200 bg-blue-50 text-blue-700',
    }

    return (
        <div className="p-4 rounded-lg">
            <h2 className="text-lg font-semibold text-slate-800 mb-4">🎯 Timeline de Eventos Críticos</h2>
            <div className="relative pl-6">
                {/* Vertical line */}
                <div className="absolute left-9 top-0 bottom-0 w-0.5 bg-slate-200" />

                <div className="space-y-6">
                    {events.map((event, index) => (
                        <div key={index} className="relative flex items-start gap-4">
                            <div className="absolute left-0 top-1.5 flex items-center justify-center w-6 h-6 bg-white rounded-full border-2 border-slate-300">
                                <div className="w-2 h-2 bg-slate-400 rounded-full" />
                            </div>
                            <div className="flex-shrink-0 w-16 text-sm font-semibold text-slate-600 text-right pr-4">
                                Mês {event.month}
                            </div>
                            <div className={`flex-grow flex items-center gap-3 p-3 rounded-lg border ${TYPE_STYLES[event.type]}`}>
                                {event.icon}
                                <div className="flex flex-col">
                                    <span className="font-semibold">{event.description}</span>
                                    {event.value && <span className="text-xs">{event.value}</span>}
                                </div>
                            </div>
                        </div>
                    ))}
                </div>
            </div>
        </div>
    );
};