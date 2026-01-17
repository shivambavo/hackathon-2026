import { ArrowDown } from 'lucide-react';
import { useState, useEffect } from 'react';

export function TranscriptionSidebar() {
  const [autoScroll, setAutoScroll] = useState(true);

  return (
    <div className="w-full" style={{ maxWidth: '30%' }}>
      <div className="bg-white dark:bg-gray-800 border border-blue-200 dark:border-blue-700 rounded-lg overflow-hidden h-full flex flex-col" style={{ minHeight: '600px' }}>
        {/* Sidebar Header */}
        <div className="px-6 py-4 border-b border-gray-200 dark:border-gray-700 flex items-center gap-3">
          <h3 className="text-lg text-gray-900 dark:text-white">Live AI Transcription</h3>
          <span className="flex items-center gap-1.5">
            <span className="w-2 h-2 bg-red-500 rounded-full animate-pulse"></span>
            <span className="text-xs text-red-500">LIVE</span>
          </span>
        </div>

        {/* Transcription Log */}
        <div className="flex-1 overflow-y-auto bg-gray-50 dark:bg-gray-900 p-4 relative">
          <div className="space-y-4">
            <div className="text-sm">
              <span className="text-gray-500 dark:text-gray-400">[00:05]</span>
              <span className="text-gray-700 dark:text-gray-300 ml-2">
                You: "Hi there, thanks for meeting with me today."
              </span>
            </div>

            <div className="text-sm">
              <span className="text-gray-500 dark:text-gray-400">[00:12]</span>
              <span className="text-gray-700 dark:text-gray-300 ml-2">
                You: "I wanted to discuss the new project proposal..."
              </span>
            </div>

            <div className="text-sm">
              <span className="text-gray-500 dark:text-gray-400">[00:18]</span>
              <span className="text-gray-700 dark:text-gray-300 ml-2">
                You: "I believe this could really benefit the team."
              </span>
            </div>

            <div className="text-sm">
              <span className="text-gray-500 dark:text-gray-400">[00:23]</span>
              <span className="text-gray-500 dark:text-gray-400 ml-2 italic">
                ... (listening)
              </span>
            </div>
          </div>

          {/* Auto-scroll button */}
          <button
            onClick={() => setAutoScroll(!autoScroll)}
            className={`absolute bottom-4 right-4 p-2 rounded-full shadow-lg transition-colors ${
              autoScroll
                ? 'bg-blue-600 text-white'
                : 'bg-white dark:bg-gray-700 text-gray-700 dark:text-gray-300'
            }`}
            aria-label="Toggle auto-scroll"
          >
            <ArrowDown className="w-4 h-4" />
          </button>
        </div>
      </div>
    </div>
  );
}
