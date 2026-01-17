import { useState } from 'react';
import { Moon, Sun } from 'lucide-react';
import { useTheme } from '../contexts/ThemeContext';
import { Card } from '../components/ui/card';
import { Input } from '../components/ui/input';
import { Label } from '../components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '../components/ui/select';
import { Button } from '../components/ui/button';

interface LandingPageProps {
  onStart: (data: { linkedinProfile: string; conversationType: string }) => void;
}

export function LandingPage({ onStart }: LandingPageProps) {
  const { isDark, toggleTheme } = useTheme();
  const [linkedinProfile, setLinkedinProfile] = useState('');
  const [conversationType, setConversationType] = useState('Networking');

  const handleGeneratePlan = () => {
    onStart({ linkedinProfile, conversationType });
  };

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 transition-colors relative overflow-hidden">
      {/* Theme Toggle - Top Right */}
      <div className="absolute top-6 right-8 z-10">
        <button
          onClick={toggleTheme}
          className="p-2 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-700 transition-colors"
          aria-label="Toggle theme"
        >
          {isDark ? (
            <Sun className="w-5 h-5 text-gray-600 dark:text-gray-300" />
          ) : (
            <Moon className="w-5 h-5 text-gray-600" />
          )}
        </button>
      </div>

      {/* Main Content - Centered */}
      <div className="flex items-center justify-center min-h-screen px-8 py-12">
        <div className="w-full max-w-xl">
          {/* Title */}
          <div className="text-center mb-12">
            <h1 className="text-4xl mb-4 text-gray-900 dark:text-white text-[64px]">
              SocialBoost AI
            </h1>
            <p className="text-lg text-gray-600 dark:text-gray-400">
              Improve your social interaction skills with AI-powered conversation planning
            </p>
          </div>

          {/* Card with Gradient Glow */}
          <div className="relative">
            {/* Gradient Glow Effect */}
            <div className="absolute -inset-1 bg-gradient-to-r from-blue-400 to-blue-600 rounded-lg blur-lg opacity-20 dark:opacity-30"></div>
            
            {/* Card */}
            <Card className="relative bg-white dark:bg-gray-800 border border-gray-200 dark:border-gray-700 rounded-lg p-8 shadow-lg">
              <div className="space-y-6">
                {/* LinkedIn Profile Input */}
                <div className="space-y-2">
                  <Label htmlFor="linkedin-profile" className="text-gray-900 dark:text-white">
                    LinkedIn Profile URL
                  </Label>
                  <Input
                    id="linkedin-profile"
                    type="text"
                    placeholder="https://linkedin.com/in/username"
                    value={linkedinProfile}
                    onChange={(e) => setLinkedinProfile(e.target.value)}
                    className="bg-white dark:bg-gray-900 border-gray-300 dark:border-gray-600 rounded-lg"
                  />
                </div>

                {/* Conversation Type Dropdown */}
                <div className="space-y-2">
                  <Label htmlFor="conversation-type" className="text-gray-900 dark:text-white">
                    Conversation Type
                  </Label>
                  <Select value={conversationType} onValueChange={setConversationType}>
                    <SelectTrigger className="bg-white dark:bg-gray-900 border-gray-300 dark:border-gray-600 rounded-lg">
                      <SelectValue placeholder="Select conversation type" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="Networking">Networking</SelectItem>
                      <SelectItem value="Job Interview">Job Interview</SelectItem>
                      <SelectItem value="Casual Chat">Casual Chat</SelectItem>
                      <SelectItem value="Sales Pitch">Sales Pitch</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                {/* Generate Plan Button */}
                <Button
                  onClick={handleGeneratePlan}
                  className="w-full bg-blue-600 hover:bg-blue-700 text-white rounded-lg py-6 text-base transition-colors"
                >
                  Generate Plan
                </Button>
              </div>
            </Card>
          </div>

          {/* Footer Text */}
          <div className="text-center mt-8">
            <p className="text-sm text-gray-500 dark:text-gray-400">
              Get personalized conversation starters, topic trees, and social tips
            </p>
          </div>
        </div>
      </div>
    </div>
  );
}