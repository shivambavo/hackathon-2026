import { useState, useEffect, useRef } from 'react';
import { Mic, MicOff, Video, VideoOff, Settings, Circle, Camera } from 'lucide-react';

interface VideoRecorderProps {
  onRecordingComplete?: (duration: number, date: Date) => void;
}

export function VideoRecorder({ onRecordingComplete }: VideoRecorderProps) {
  const [isRecording, setIsRecording] = useState(false);
  const [isMicOn, setIsMicOn] = useState(true);
  const [isCameraOn, setIsCameraOn] = useState(true);
  const [timer, setTimer] = useState('00:00:00');
  const [status, setStatus] = useState('Initializing...');
  const [cameraError, setCameraError] = useState<string | null>(null);
  const videoRef = useRef<HTMLVideoElement>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const timerIntervalRef = useRef<number | null>(null);
  const recordingStartTimeRef = useRef<number>(0);
  const recordingStartDateRef = useRef<Date | null>(null);

  // Initialize camera when component mounts
  useEffect(() => {
    const initCamera = async () => {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({
          video: true,
          audio: true
        });
        streamRef.current = stream;
        if (videoRef.current) {
          videoRef.current.srcObject = stream;
        }
        setStatus('Ready');
        setCameraError(null);
      } catch (err) {
        // Handle camera access errors gracefully without console logging
        if (err instanceof Error) {
          if (err.name === 'NotAllowedError') {
            setCameraError('Camera access denied. Please allow camera permissions in your browser.');
          } else if (err.name === 'NotFoundError') {
            setCameraError('No camera found. Please connect a camera device.');
          } else {
            setCameraError('Unable to access camera. Please check your settings.');
          }
        }
        setStatus('Error');
      }
    };

    initCamera();

    // Cleanup function to stop camera when component unmounts
    return () => {
      if (streamRef.current) {
        streamRef.current.getTracks().forEach(track => track.stop());
      }
    };
  }, []);

  // Handle camera toggle
  useEffect(() => {
    if (streamRef.current) {
      const videoTrack = streamRef.current.getVideoTracks()[0];
      if (videoTrack) {
        videoTrack.enabled = isCameraOn;
      }
    }
  }, [isCameraOn]);

  // Handle microphone toggle
  useEffect(() => {
    if (streamRef.current) {
      const audioTrack = streamRef.current.getAudioTracks()[0];
      if (audioTrack) {
        audioTrack.enabled = isMicOn;
      }
    }
  }, [isMicOn]);

  const handleRecord = () => {
    if (!isRecording) {
      setIsRecording(true);
      setStatus('Recording');
      recordingStartTimeRef.current = Date.now();
      recordingStartDateRef.current = new Date();
      timerIntervalRef.current = window.setInterval(() => {
        const elapsed = Date.now() - recordingStartTimeRef.current;
        const hours = Math.floor(elapsed / 3600000);
        const minutes = Math.floor((elapsed % 3600000) / 60000);
        const seconds = Math.floor((elapsed % 60000) / 1000);
        setTimer(`${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`);
      }, 1000);
    } else {
      setIsRecording(false);
      setStatus('Ready');
      setTimer('00:00:00');
      if (timerIntervalRef.current) {
        clearInterval(timerIntervalRef.current);
        timerIntervalRef.current = null;
      }
      if (onRecordingComplete && recordingStartDateRef.current) {
        const duration = Date.now() - recordingStartTimeRef.current;
        onRecordingComplete(duration, recordingStartDateRef.current);
      }
    }
  };

  const requestCameraAccess = async () => {
    setCameraError(null);
    setStatus('Requesting access...');
    try {
      const stream = await navigator.mediaDevices.getUserMedia({
        video: true,
        audio: true
      });
      streamRef.current = stream;
      if (videoRef.current) {
        videoRef.current.srcObject = stream;
      }
      setStatus('Ready');
      setCameraError(null);
    } catch (err) {
      // Handle camera access errors gracefully
      if (err instanceof Error) {
        if (err.name === 'NotAllowedError') {
          setCameraError('Camera access denied. Please allow camera permissions in your browser settings.');
        } else if (err.name === 'NotFoundError') {
          setCameraError('No camera found. Please connect a camera device.');
        } else {
          setCameraError('Unable to access camera. Please check your settings.');
        }
      }
      setStatus('Error');
    }
  };

  return (
    <div className="space-y-4">
      {/* Video Container */}
      <div className="relative w-full aspect-video bg-gray-900 rounded-lg overflow-hidden">
        {cameraError ? (
          <div className="absolute inset-0 flex flex-col items-center justify-center bg-gray-800 p-8">
            <Camera className="w-16 h-16 text-gray-500 mb-4" />
            <p className="text-white text-lg mb-2 text-center">Camera Access Required</p>
            <p className="text-gray-400 text-sm mb-6 text-center max-w-md">{cameraError}</p>
            <button
              onClick={requestCameraAccess}
              className="px-6 py-3 bg-blue-600 hover:bg-blue-700 text-white rounded-lg transition-colors"
            >
              Request Camera Access
            </button>
          </div>
        ) : (
          <>
            <video
              ref={videoRef}
              autoPlay
              playsInline
              muted
              className="w-full h-full object-cover"
            />
            {!isCameraOn && (
              <div className="absolute inset-0 flex items-center justify-center bg-gray-900">
                <p className="text-white text-xl">Camera Off</p>
              </div>
            )}
          </>
        )}
        
        {/* Recording indicator */}
        {isRecording && !cameraError && (
          <div className="absolute top-4 right-4 flex items-center gap-2 bg-red-600 text-white px-3 py-1.5 rounded-full">
            <Circle className="w-3 h-3 fill-white animate-pulse" />
            <span className="text-sm">REC</span>
          </div>
        )}
      </div>

      {/* Status & Timer */}
      <div className="flex items-center justify-between px-4">
        <div className="flex items-center gap-4">
          <span className="text-gray-700 dark:text-gray-300">
            Status: <span className={isRecording ? 'text-red-600 font-medium' : status === 'Error' ? 'text-red-600 font-medium' : 'text-green-600 font-medium'}>{status}</span>
          </span>
          <span className="text-gray-700 dark:text-gray-300 font-mono text-lg">{timer}</span>
        </div>
      </div>

      {/* Control Bar */}
      <div className="bg-gray-100 dark:bg-gray-800 rounded-lg p-6">
        <div className="flex items-center justify-center gap-6">
          {/* Microphone Toggle */}
          <button
            onClick={() => setIsMicOn(!isMicOn)}
            className={`p-3 rounded-full transition-colors ${
              isMicOn 
                ? 'bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600' 
                : 'bg-red-500 hover:bg-red-600'
            }`}
            aria-label="Toggle Microphone"
          >
            {isMicOn ? (
              <Mic className="w-5 h-5 text-gray-700 dark:text-gray-300" />
            ) : (
              <MicOff className="w-5 h-5 text-white" />
            )}
          </button>

          {/* Record Button */}
          <button
            onClick={handleRecord}
            className={`px-8 py-4 rounded-full flex items-center gap-3 transition-colors ${
              isRecording
                ? 'bg-red-600 hover:bg-red-700 text-white'
                : 'bg-blue-600 hover:bg-blue-700 text-white'
            }`}
          >
            <Circle className={`w-5 h-5 ${isRecording ? 'fill-white' : ''}`} />
            <span className="text-lg">{isRecording ? 'Stop Recording' : 'Start Recording'}</span>
          </button>

          {/* Camera Toggle */}
          <button
            onClick={() => setIsCameraOn(!isCameraOn)}
            className={`p-3 rounded-full transition-colors ${
              isCameraOn 
                ? 'bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600' 
                : 'bg-red-500 hover:bg-red-600'
            }`}
            aria-label="Toggle Camera"
          >
            {isCameraOn ? (
              <Video className="w-5 h-5 text-gray-700 dark:text-gray-300" />
            ) : (
              <VideoOff className="w-5 h-5 text-white" />
            )}
          </button>

          {/* Settings */}
          <button
            className="p-3 rounded-full bg-gray-200 dark:bg-gray-700 hover:bg-gray-300 dark:hover:bg-gray-600 transition-colors"
            aria-label="Settings"
          >
            <Settings className="w-5 h-5 text-gray-700 dark:text-gray-300" />
          </button>
        </div>
      </div>
    </div>
  );
}