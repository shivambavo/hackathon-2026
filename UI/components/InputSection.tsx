import { useState, useEffect } from 'react';

interface InputSectionProps {
  initialData?: {
    linkedinProfile: string;
    conversationType: string;
  } | null;
  onGenerate?: (data: {
    linkedinProfile: string;
    conversationType: string;
  }) => void;
}

export function InputSection({ initialData, onGenerate }: InputSectionProps) {
  const [profileLink, setProfileLink] = useState('');
  const [conversationType, setConversationType] = useState('Networking');

  // Update state when initialData changes
  useEffect(() => {
    if (initialData) {
      setProfileLink(initialData.linkedinProfile);
      setConversationType(initialData.conversationType);
    }
  }, [initialData]);

  const handleGenerate = () => {
    onGenerate?.({ linkedinProfile: profileLink, conversationType });
  };

  return (
    <div>
      <h2 className="text-xl mb-8 text-gray-900 dark:text-white">
        Target Profile Input
      </h2>
      
      <div className="space-y-6">
        {/* Profile Link Input */}
        <div>
          <label htmlFor="profile-link" className="block text-sm mb-2 text-gray-700 dark:text-gray-300">
            Target's LinkedIn Profile Link
          </label>
          <input
            id="profile-link"
            type="text"
            value={profileLink}
            onChange={(e) => setProfileLink(e.target.value)}
            placeholder="https://linkedin.com/in/username"
            className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white placeholder-gray-400 dark:placeholder-gray-500"
          />
        </div>

        {/* Conversation Type Dropdown */}
        <div>
          <label htmlFor="conversation-type" className="block text-sm mb-2 text-gray-700 dark:text-gray-300">
            Conversation Type
          </label>
          <select
            id="conversation-type"
            value={conversationType}
            onChange={(e) => setConversationType(e.target.value)}
            className="w-full px-4 py-3 border border-gray-300 dark:border-gray-600 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent bg-white dark:bg-gray-800 text-gray-900 dark:text-white"
          >
            <option>Networking</option>
            <option>Job Interview</option>
            <option>Casual Chat</option>
            <option>Sales Pitch</option>
          </select>
        </div>

        {/* Generate Button */}
        <button
          onClick={handleGenerate}
          className="w-full bg-blue-600 hover:bg-blue-700 text-white py-4 rounded-lg transition-colors"
        >
          Generate Plan
        </button>
      </div>
    </div>
  );
}