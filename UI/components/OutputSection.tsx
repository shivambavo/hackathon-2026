import { Copy } from 'lucide-react';

interface PlanSection {
  title: string;
  items: string[];
}

interface PlanOutput {
  title: string;
  summary: string;
  sections: PlanSection[];
}

interface OutputSectionProps {
  plan?: PlanOutput | null;
}

export function OutputSection({ plan }: OutputSectionProps) {
  const planText = plan
    ? [
        plan.title,
        plan.summary,
        '',
        ...plan.sections.flatMap((section) => [
          section.title,
          ...section.items.map((item) => `- ${item}`),
          '',
        ]),
      ]
        .join('\n')
        .trim()
    : '';

  const handleCopyAll = async () => {
    if (!planText) {
      return;
    }
    try {
      await navigator.clipboard.writeText(planText);
    } catch {
      // no-op if clipboard access is blocked
    }
  };

  return (
    <div>
      <h2 className="text-xl mb-8 text-gray-900 dark:text-white">
        Generated Strategy Plan
      </h2>
      
      {/* Single large container with all content */}
      <div className="bg-white dark:bg-gray-800 border border-blue-200 dark:border-blue-700 rounded-lg p-8">
        {/* Global action buttons at top right */}
        <div className="flex justify-end gap-3 mb-6">
          <button
            onClick={handleCopyAll}
            className="flex items-center gap-2 px-4 py-2 hover:bg-blue-50 dark:hover:bg-gray-700 rounded-lg transition-colors text-gray-700 dark:text-gray-300 text-sm"
            aria-label="Copy All"
          >
            <Copy className="w-4 h-4" />
            Copy All
          </button>
        </div>

        {/* Content area */}
        {!plan && (
          <div className="flex items-center justify-center h-64 text-gray-400 dark:text-gray-500 text-sm">
            Your strategy plan will appear here after generation.
          </div>
        )}

        {plan && (
          <div className="space-y-6 text-gray-700 dark:text-gray-200">
            <div>
              <h3 className="text-lg text-gray-900 dark:text-white mb-2">
                {plan.title}
              </h3>
              <p className="text-sm text-gray-600 dark:text-gray-400">
                {plan.summary}
              </p>
            </div>

            <div className="space-y-4">
              {plan.sections.map((section) => (
                <div key={section.title}>
                  <h4 className="text-sm font-semibold text-gray-900 dark:text-white mb-2">
                    {section.title}
                  </h4>
                  <ul className="list-disc pl-5 space-y-1 text-sm text-gray-600 dark:text-gray-300">
                    {section.items.map((item, index) => (
                      <li key={`${section.title}-${index}`}>{item}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}