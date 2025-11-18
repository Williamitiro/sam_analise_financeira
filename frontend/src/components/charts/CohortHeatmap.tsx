// frontend/src/components/charts/CohortHeatmap.tsx
import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { Card } from '../ui/Card';
import { Tooltip, TooltipContent, TooltipProvider, TooltipTrigger } from '../ui/tooltip';

interface CohortHeatmapProps {
  title: string;
  data: {
    cohort: string;
    size: number;
    retention: (number | null)[];
  }[];
}

// Function to get color based on value (0-100)
const getColor = (value: number) => {
  if (value > 80) return 'bg-green-600';
  if (value > 60) return 'bg-green-500';
  if (value > 40) return 'bg-green-400';
  if (value > 20) return 'bg-green-300';
  if (value > 0) return 'bg-green-200';
  return 'bg-slate-100';
};

export const CohortHeatmap = ({ title, data }: CohortHeatmapProps) => {
  if (!data || data.length === 0) {
    return <div>No data</div>;
  }

  const maxMonths = data[0].retention.length;

  return (
    <Card className="p-4 h-full flex flex-col col-span-2">
      <h3 className="text-lg font-semibold text-slate-800 mb-4">{title}</h3>
      <TooltipProvider>
        <div className="overflow-x-auto">
            <Table>
            <TableHeader>
                <TableRow>
                <TableHead className="w-[100px]">Cohort</TableHead>
                <TableHead className="w-[80px]">Tamanho</TableHead>
                {Array.from({ length: maxMonths }).map((_, index) => (
                    <TableHead key={index} className="text-center">{`Mês ${index}`}</TableHead>
                ))}
                </TableRow>
            </TableHeader>
            <TableBody>
                {data.map((row, rowIndex) => (
                <TableRow key={rowIndex}>
                    <TableCell className="font-medium">{row.cohort}</TableCell>
                    <TableCell>{row.size}</TableCell>
                    {row.retention.map((value, colIndex) => (
                    <TableCell key={colIndex} className="p-0 text-center">
                        {value !== null ? (
                        <Tooltip>
                            <TooltipTrigger asChild>
                                <div className={`h-full w-full flex items-center justify-center text-white text-xs font-bold ${getColor(value)}`}>
                                    {`${value}%`}
                                </div>
                            </TooltipTrigger>
                            <TooltipContent>
                                <p>{`${row.cohort}, Mês ${colIndex}: ${value}% de retenção`}</p>
                            </TooltipContent>
                        </Tooltip>
                        ) : (
                        <div className="bg-slate-50 h-full w-full" />
                        )}
                    </TableCell>
                    ))}
                </TableRow>
                ))}
            </TableBody>
            </Table>
        </div>
      </TooltipProvider>
    </Card>
  );
};
