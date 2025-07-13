
import React from 'react';
import { motion } from 'framer-motion';
import { Button } from '@/components/ui/button';
import { Rocket, Target, Trophy, Users, Zap } from 'lucide-react';

export function WelcomeScreen({ onStartChallenge }) {
  return (
    <motion.div 
      initial={{ opacity: 0, scale: 0.9 }}
      animate={{ opacity: 1, scale: 1 }}
      className="text-center py-20 px-4"
    >
      <div className="bg-white/10 backdrop-blur-lg rounded-3xl p-12 max-w-4xl mx-auto border border-white/20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2 }}
        >
          <div className="bg-gradient-to-r from-purple-500 to-blue-500 p-6 rounded-full w-24 h-24 mx-auto mb-8">
            <Rocket className="h-12 w-12 text-white mx-auto" />
          </div>
          <h2 className="text-5xl font-bold text-white mb-6 bg-gradient-to-r from-purple-400 to-blue-400 bg-clip-text text-transparent">
            100 Apps in 100 Days
          </h2>
          <p className="text-xl text-purple-200 mb-8 max-w-2xl mx-auto">
            Transform your coding skills with the ultimate development challenge. Build, learn, and showcase 100 applications while documenting your incredible journey.
          </p>
          
          <div className="grid md:grid-cols-3 gap-6 mb-12">
            <div className="bg-white/5 rounded-xl p-6 border border-white/10">
              <Target className="h-8 w-8 text-purple-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-white mb-2">Track Progress</h3>
              <p className="text-purple-200 text-sm">Monitor your daily progress and maintain momentum</p>
            </div>
            <div className="bg-white/5 rounded-xl p-6 border border-white/10">
              <Trophy className="h-8 w-8 text-blue-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-white mb-2">Build Portfolio</h3>
              <p className="text-purple-200 text-sm">Create an impressive showcase for employers</p>
            </div>
            <div className="bg-white/5 rounded-xl p-6 border border-white/10">
              <Users className="h-8 w-8 text-indigo-400 mx-auto mb-4" />
              <h3 className="text-lg font-semibold text-white mb-2">Join Community</h3>
              <p className="text-purple-200 text-sm">Connect with fellow developers on the same journey</p>
            </div>
          </div>

          <Button 
            onClick={onStartChallenge}
            size="lg"
            className="bg-gradient-to-r from-purple-500 to-blue-500 hover:from-purple-600 hover:to-blue-600 text-white px-12 py-6 text-lg font-semibold rounded-xl shadow-2xl transform hover:scale-105 transition-all duration-200"
          >
            <Zap className="h-6 w-6 mr-3" />
            Start Your Challenge
          </Button>
        </motion.div>
      </div>
    </motion.div>
  );
}
