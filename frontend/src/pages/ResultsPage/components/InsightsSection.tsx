// frontend/src/pages/ResultsPage/components/InsightsSection.tsx
import { Insight } from '@/types/api.types';
import React from 'react';
import { InsightCard } from './InsightCard';

interface InsightsSectionProps {
    insights: Insight[];
}

export const InsightsSection = ({ insights }: InsightsSectionProps) => {
    const positiveInsights = insights.filter(
        (i) => i.level === 'SUCCESS' || i.level === 'OPPORTUNITY'
    );

    if (positiveInsights.length === 0) {
        return null;
    }

    return (
        <div className="p-4 rounded-lg">
            <h2 className="text-lg font-semibold text-slate-800 mb-4">💡 Oportunidades e Pontos Fortes</h2>
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
        </div>
    );
};
