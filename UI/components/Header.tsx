import { Moon, Sun } from 'lucide-react';
import { NavLink } from 'react-router-dom';
import { useTheme } from '../contexts/ThemeContext';

const navLinkClass = ({ isActive }: { isActive: boolean }) =>
  `transition-colors ${
    isActive
      ? 'text-blue-600 dark:text-blue-400 border-b-2 border-blue-600 dark:border-blue-400'
      : 'text-gray-600 dark:text-gray-300 hover:text-gray-900 dark:hover:text-white'
  }`;

export function Header() {
  const { isDark, toggleTheme } = useTheme();

  return (
    <header className="bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 transition-colors">
      <div className="max-w-7xl mx-auto px-8 py-6 flex items-center justify-between">
        <div className="flex items-center gap-4">
          <div className="text-xl text-gray-900 dark:text-white">SocialBoost AI</div>
        </div>
        
        <div className="flex items-center gap-6">
          <nav className="flex gap-8">
            <NavLink to="/" end className={navLinkClass}>
              Home
            </NavLink>
            <NavLink to="/plan" className={navLinkClass}>
              Plan
            </NavLink>
            <NavLink to="/analyze" className={navLinkClass}>
              Analyze
            </NavLink>
            <NavLink to="/profile" className={navLinkClass}>
              Profile
            </NavLink>
          </nav>
          
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
      </div>
    </header>
  );
}