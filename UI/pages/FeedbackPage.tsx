import { Link } from 'react-router-dom';

interface FeedbackPageProps {
  recordingData?: {duration: number, date: Date} | null;
}

export function FeedbackPage({ recordingData }: FeedbackPageProps) {
  const formatDuration = (milliseconds: number) => {
    const totalSeconds = Math.floor(milliseconds / 1000);
    const minutes = Math.floor(totalSeconds / 60);
    const seconds = totalSeconds % 60;
    return `${minutes}:${seconds.toString().padStart(2, '0')}`;
  };

  const formatDate = (date: Date) => {
    return date.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' });
  };

  return (
    <main className="max-w-7xl mx-auto px-8 py-12">
      <h1 className="text-3xl mb-8 text-gray-900 dark:text-white">
        Performance Analysis & Feedback
      </h1>

      {/* Video Summary Section */}
      <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-6 mb-12 flex items-center gap-6">
        <div className="w-32 h-20 bg-gray-200 dark:bg-gray-700 rounded-lg flex items-center justify-center text-gray-500 dark:text-gray-400 flex-shrink-0">
          <svg width="40" height="40" viewBox="0 0 40 40" fill="none" className="text-gray-400">
            <path d="M15 12L27 20L15 28V12Z" fill="currentColor"/>
          </svg>
        </div>
        <div className="text-gray-700 dark:text-gray-300">
          {recordingData ? (
            <>
              <span className="font-medium">Session Recording:</span> {formatDate(recordingData.date)} | <span className="font-medium">Duration:</span> {formatDuration(recordingData.duration)}
            </>
          ) : (
            <span className="text-gray-400 dark:text-gray-500 italic">No recording data available</span>
          )}
        </div>
      </div>

      {/* Feedback Output */}
      <div className="bg-white dark:bg-gray-800 border border-blue-200 dark:border-blue-700 rounded-lg p-8 h-[400px] mb-12"></div>

      {/* Footer - Try Again Section */}
      <div className="bg-gray-100 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 rounded-lg p-8">
        <h3 className="text-xl text-gray-900 dark:text-white mb-6">Ready to practice again?</h3>
        <Link
          to="/plan"
          className="inline-block px-8 py-3 bg-blue-600 dark:bg-blue-500 text-white rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors"
        >
          Try Again
        </Link>
      </div>
    </main>
  );
}