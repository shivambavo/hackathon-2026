import { Link } from 'react-router-dom';
import { VideoRecorder } from '../components/VideoRecorder';
import { LiveTranscription } from '../components/LiveTranscription';

interface AnalyzePageProps {
  onRecordingComplete?: (data: {duration: number, date: Date}) => void;
}

export function AnalyzePage({ onRecordingComplete }: AnalyzePageProps) {
  const handleRecordingComplete = (duration: number, date: Date) => {
    if (onRecordingComplete) {
      onRecordingComplete({ duration, date });
    }
  };

  return (
    <main className="max-w-7xl mx-auto px-8 py-12">
      <h1 className="text-3xl mb-12 text-gray-900 dark:text-white">
        Phase 2: Performance Recording & Live Analysis
      </h1>
      
      <div className="grid grid-cols-1 lg:grid-cols-[70%_30%] gap-8">
        <VideoRecorder onRecordingComplete={handleRecordingComplete} />
        <LiveTranscription />
      </div>

      {/* Complete Session Button */}
      <div className="mt-8 flex justify-end">
        <Link
          to="/feedback"
          className="px-8 py-3 bg-green-600 hover:bg-green-700 text-white rounded-lg transition-colors"
        >
          Complete Session & View Feedback
        </Link>
      </div>
    </main>
  );
}