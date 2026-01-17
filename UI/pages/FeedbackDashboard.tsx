import { Play, Pause, Volume2, CheckCircle, AlertTriangle, ArrowRight } from 'lucide-react';
import { useState } from 'react';
import { Link } from 'react-router-dom';

export function FeedbackDashboard() {
  const [isPlaying, setIsPlaying] = useState(false);
  const [progress, setProgress] = useState(45);
  const [volume, setVolume] = useState(80);

  return (
    <main className="max-w-7xl mx-auto px-8 py-12">
      {/* Top Section - Video Playback */}
      <div className="mb-12">
        <h2 className="text-xl mb-6 text-gray-900 dark:text-white">
          Review Session Recording
        </h2>
        
        <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden">
          {/* Video Player */}
          <div className="aspect-video bg-gray-200 dark:bg-gray-700 flex items-center justify-center">
            <div className="text-center">
              <svg 
                width="80" 
                height="80" 
                viewBox="0 0 80 80" 
                fill="none" 
                className="mx-auto mb-4 text-gray-400 dark:text-gray-500"
              >
                <circle cx="40" cy="40" r="30" stroke="currentColor" strokeWidth="2"/>
                <path d="M35 28L53 40L35 52V28Z" fill="currentColor"/>
              </svg>
              <p className="text-gray-500 dark:text-gray-400">Video Captured</p>
            </div>
          </div>
          
          {/* Video Controls */}
          <div className="p-4 bg-white dark:bg-gray-800 border-t border-gray-200 dark:border-gray-700">
            <div className="flex items-center gap-4">
              {/* Play/Pause Button */}
              <button 
                onClick={() => setIsPlaying(!isPlaying)}
                className="w-10 h-10 flex items-center justify-center rounded-full bg-blue-600 dark:bg-blue-500 text-white hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors"
              >
                {isPlaying ? <Pause className="w-5 h-5" /> : <Play className="w-5 h-5 ml-0.5" />}
              </button>
              
              {/* Progress Bar */}
              <div className="flex-1">
                <div className="flex items-center gap-2 mb-1">
                  <span className="text-xs text-gray-600 dark:text-gray-400">
                    {Math.floor((progress / 100) * 225)}:{String(Math.floor(((progress / 100) * 225) % 60)).padStart(2, '0')}
                  </span>
                  <span className="text-xs text-gray-400 dark:text-gray-500">/</span>
                  <span className="text-xs text-gray-600 dark:text-gray-400">3:45</span>
                </div>
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={progress}
                  onChange={(e) => setProgress(Number(e.target.value))}
                  className="w-full h-2 bg-gray-200 dark:bg-gray-700 rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-4 [&::-webkit-slider-thumb]:h-4 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-blue-600 [&::-webkit-slider-thumb]:cursor-pointer"
                  style={{
                    background: `linear-gradient(to right, rgb(37, 99, 235) 0%, rgb(37, 99, 235) ${progress}%, rgb(229, 231, 235) ${progress}%, rgb(229, 231, 235) 100%)`
                  }}
                />
              </div>
              
              {/* Volume Control */}
              <div className="flex items-center gap-2 w-32">
                <Volume2 className="w-5 h-5 text-gray-600 dark:text-gray-400" />
                <input
                  type="range"
                  min="0"
                  max="100"
                  value={volume}
                  onChange={(e) => setVolume(Number(e.target.value))}
                  className="flex-1 h-2 bg-gray-200 dark:bg-gray-700 rounded-full appearance-none cursor-pointer [&::-webkit-slider-thumb]:appearance-none [&::-webkit-slider-thumb]:w-3 [&::-webkit-slider-thumb]:h-3 [&::-webkit-slider-thumb]:rounded-full [&::-webkit-slider-thumb]:bg-blue-600 [&::-webkit-slider-thumb]:cursor-pointer"
                />
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Middle Section - AI Analysis Grid */}
      <div className="mb-12">
        <h2 className="text-xl mb-6 text-gray-900 dark:text-white">
          AI-Powered Analysis
        </h2>
        
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          {/* Slot 1 - What Worked */}
          <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden h-[400px] flex flex-col">
            <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center gap-3">
              <CheckCircle className="w-5 h-5 text-green-500 dark:text-green-400" />
              <h3 className="text-gray-900 dark:text-white">What Worked (AI Generated)</h3>
            </div>
            <div className="flex-1 p-6 flex items-center justify-center">
              <div className="space-y-3 w-full">
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse w-5/6"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse w-4/6"></div>
                <div className="mt-6 h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse w-5/6"></div>
                <p className="text-center text-sm text-gray-400 dark:text-gray-500 mt-8">Analysis Pending...</p>
              </div>
            </div>
          </div>

          {/* Slot 2 - What Hurt */}
          <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden h-[400px] flex flex-col">
            <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center gap-3">
              <AlertTriangle className="w-5 h-5 text-amber-500 dark:text-amber-400" />
              <h3 className="text-gray-900 dark:text-white">What Hurt (AI Generated)</h3>
            </div>
            <div className="flex-1 p-6 flex items-center justify-center">
              <div className="space-y-3 w-full">
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse w-5/6"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse w-4/6"></div>
                <div className="mt-6 h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse w-5/6"></div>
                <p className="text-center text-sm text-gray-400 dark:text-gray-500 mt-8">Analysis Pending...</p>
              </div>
            </div>
          </div>

          {/* Slot 3 - Concrete Suggestions */}
          <div className="bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg overflow-hidden h-[400px] flex flex-col">
            <div className="p-4 border-b border-gray-200 dark:border-gray-700 flex items-center gap-3">
              <ArrowRight className="w-5 h-5 text-blue-500 dark:text-blue-400" />
              <h3 className="text-gray-900 dark:text-white">Concrete Suggestions (AI Generated)</h3>
            </div>
            <div className="flex-1 p-6 flex items-center justify-center">
              <div className="space-y-3 w-full">
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse w-5/6"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse w-4/6"></div>
                <div className="mt-6 h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse"></div>
                <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded animate-pulse w-5/6"></div>
                <p className="text-center text-sm text-gray-400 dark:text-gray-500 mt-8">Analysis Pending...</p>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Bottom Section - Action Buttons */}
      <div className="bg-gray-100 dark:bg-gray-800/50 border border-gray-200 dark:border-gray-700 rounded-lg p-8">
        <h3 className="text-xl text-gray-900 dark:text-white mb-6">Try Again</h3>
        <div className="flex gap-4">
          <Link
            to="/plan"
            className="flex-1 px-6 py-3 bg-white dark:bg-gray-800 text-blue-600 dark:text-blue-400 border-2 border-blue-600 dark:border-blue-400 rounded-lg hover:bg-blue-50 dark:hover:bg-gray-700 transition-colors text-center"
          >
            Retry Same Scenario
          </Link>
          <Link
            to="/plan"
            className="flex-1 px-6 py-3 bg-blue-600 dark:bg-blue-500 text-white rounded-lg hover:bg-blue-700 dark:hover:bg-blue-600 transition-colors text-center"
          >
            Level Up: Harder Version
          </Link>
        </div>
      </div>
    </main>
  );
}