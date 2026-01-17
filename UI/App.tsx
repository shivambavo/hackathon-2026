import { Header } from "./components/Header";
import { ThemeProvider } from "./contexts/ThemeContext";
import { LandingPage } from "./pages/LandingPage";
import { StrategyPage } from "./pages/StrategyPage";
import { AnalyzePage } from "./pages/AnalyzePage";
import { FeedbackPage } from "./pages/FeedbackPage";
import { FeedbackDashboard } from "./pages/FeedbackDashboard";
import { useState } from "react";
import {
  BrowserRouter,
  Navigate,
  Route,
  Routes,
  useLocation,
  useNavigate,
} from "react-router-dom";

function AppContent() {
  const location = useLocation();
  const navigate = useNavigate();
  const [recordingData, setRecordingData] = useState<{
    duration: number;
    date: Date;
  } | null>(null);
  const [planData, setPlanData] = useState<{
    linkedinProfile: string;
    conversationType: string;
  } | null>(null);

  const handleStartPlan = (data: {
    linkedinProfile: string;
    conversationType: string;
  }) => {
    setPlanData(data);
    navigate("/plan");
  };

  const showHeader = location.pathname !== "/";

  return (
    <div className="min-h-screen bg-white dark:bg-gray-900 transition-colors">
      {showHeader && <Header />}

      <Routes>
        <Route path="/" element={<LandingPage onStart={handleStartPlan} />} />
        <Route path="/plan" element={<StrategyPage planData={planData} />} />
        <Route
          path="/analyze"
          element={<AnalyzePage onRecordingComplete={setRecordingData} />}
        />
        <Route
          path="/feedback"
          element={<FeedbackPage recordingData={recordingData} />}
        />
        <Route path="/dashboard" element={<FeedbackDashboard />} />
        <Route
          path="/profile"
          element={
            <main className="max-w-7xl mx-auto px-8 py-12">
              <h1 className="text-3xl mb-12 text-gray-900 dark:text-white">
                Profile
              </h1>
              <p className="text-gray-600 dark:text-gray-400">
                Profile page coming soon...
              </p>
            </main>
          }
        />
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </div>
  );
}

export default function App() {
  return (
    <ThemeProvider>
      <BrowserRouter>
        <AppContent />
      </BrowserRouter>
    </ThemeProvider>
  );
}