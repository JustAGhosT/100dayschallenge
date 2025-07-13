import React from 'react';
import { motion } from 'framer-motion';
import { Code, Github } from 'lucide-react';

interface LandingPageProps {
  onSignInGitHub: () => void;
  onSignInGoogle: () => void;
}

const GoogleIcon = () => (
    <svg className="w-5 h-5 mr-2" viewBox="0 0 24 24">
        <path d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z" fill="#4285F4" />
        <path d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z" fill="#34A853" />
        <path d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.07H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.93l3.66-2.84z" fill="#FBBC05" />
        <path d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.07l3.66 2.84c.87-2.6 3.3-4.53 6.16-4.53z" fill="#EA4335" />
    </svg>
);

export function LandingPage({ onSignInGitHub, onSignInGoogle }: LandingPageProps) {
  return (
    <div className="flex flex-col items-center justify-center min-h-screen text-center p-4">
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.8 }}
        className="bg-white/5 backdrop-blur-xl rounded-3xl p-8 md:p-12 max-w-4xl mx-auto border border-white/10 shadow-2xl"
      >
        <div className="flex justify-center items-center mb-6">
           <div className="bg-gradient-to-r from-purple-500 to-blue-500 p-4 rounded-2xl">
              <Code className="h-10 w-10 text-white" />
            </div>
        </div>
        <h1 className="text-4xl md:text-6xl font-bold text-white mb-4 bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
          100 Apps in 100 Days
        </h1>
        <p className="text-lg md:text-xl text-purple-200 mb-8 max-w-2xl mx-auto">
          Track, document, and showcase your coding journey. Build your portfolio and accelerate your growth.
        </p>

        <div className="flex flex-col md:flex-row gap-4 justify-center mb-10">
          <button 
            onClick={onSignInGitHub}
            className="bg-gray-800 hover:bg-gray-700 text-white px-6 py-3 text-base font-semibold rounded-xl shadow-lg w-full md:w-auto flex items-center justify-center"
          >
            <Github className="w-5 h-5 mr-2" /> Sign In with GitHub
          </button>
          <button 
            onClick={onSignInGoogle}
            className="bg-white hover:bg-gray-100 text-gray-800 px-6 py-3 text-base font-semibold rounded-xl shadow-lg w-full md:w-auto flex items-center justify-center"
          >
            <GoogleIcon /> Sign In with Google
          </button>
        </div>
      </motion.div>
    </div>
  );
}