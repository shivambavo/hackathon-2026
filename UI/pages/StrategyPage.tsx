import { useState } from 'react';
import { InputSection } from '../components/InputSection';
import { OutputSection } from '../components/OutputSection';

interface StrategyPageProps {
  planData?: {
    linkedinProfile: string;
    conversationType: string;
  } | null;
}

interface PlanSection {
  title: string;
  items: string[];
}

interface PlanOutput {
  title: string;
  summary: string;
  sections: PlanSection[];
}

export function StrategyPage({ planData }: StrategyPageProps) {
  const [planOutput, setPlanOutput] = useState<PlanOutput | null>(null);

  const handleGenerate = () => {
    // Backend integration will populate the plan output.
    setPlanOutput(null);
  };

  return (
    <main className="max-w-7xl mx-auto px-8 py-12">
      <h1 className="text-3xl mb-12 text-gray-900 dark:text-white">
        Phase 1: Strategy Generation
      </h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-12">
        <InputSection initialData={planData} onGenerate={handleGenerate} />
        <OutputSection plan={planOutput} />
      </div>
    </main>
  );
}