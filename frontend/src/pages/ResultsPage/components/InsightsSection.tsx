// frontend/src/pages/ResultsPage/components/InsightsSection.tsx
import { Insight } from '@/types/api.types';
import React from 'react';
import { InsightCard } from './InsightCard';

interface InsightsSectionProps {
    insights: Insight[];
}

export const InsightsSection = ({ insights }: InsightsSectionProps) => {
    if (!insights) {
        return null;
    }

    const positiveInsights = insights.filter(
        (i) => i.category === 'opportunity'
    );

    if (positiveInsights.length === 0) {
        return null;
    }

    return (
        <section className="bg-white border border-slate-200 rounded-xl shadow-sm p-6">
            <h2 className="text-xl font-bold text-slate-800 mb-6 flex items-center gap-2">
                <span className="text-2xl">💡</span>
                Oportunidades e Pontos Fortes
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                {positiveInsights.map((insight, index) => (
                    <InsightCard
                        key={index}
                        level={insight.level}
                        title={insight.title}
                        description={insight.description}
                    />
                ))}
            </div>
        </section>
    );
};
