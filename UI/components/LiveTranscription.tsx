import { useState } from 'react';

export function LiveTranscription() {
  return (
    <div className="bg-white dark:bg-gray-800 border border-blue-200 dark:border-blue-700 rounded-lg h-full flex flex-col">
      {/* Sidebar Header */}
      <div className="p-6 border-b border-gray-200 dark:border-gray-700">
        <div className="flex items-center gap-3">
          <h3 className="text-lg text-gray-900 dark:text-white">Live AI Transcription</h3>
          <div className="flex items-center gap-1.5 bg-red-600 text-white px-2 py-1 rounded-full text-xs">
            <span className="w-2 h-2 bg-white rounded-full animate-pulse"></span>
            LIVE
          </div>
        </div>
      </div>

      {/* Transcription Log - Empty, will be populated with AI output */}
      <div className="flex-1 p-6 overflow-y-auto bg-gray-50 dark:bg-gray-900/30">
        {/* Content will be dynamically added here */}
      </div>
    </div>
  );
}