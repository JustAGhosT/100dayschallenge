import React from 'react';
import { motion } from 'framer-motion';
import { Code, Share2, LogOut } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import { useToast } from '@/components/ui/use-toast';

export function Header({ userProfile, completedProjects, daysElapsed, signOut }) {
  const { toast } = useToast();

  const shareProgress = () => {
    const text = `🚀 I'm taking on the #100AppsIn100Days challenge! Currently at ${completedProjects}/100 apps completed in ${daysElapsed} days. Join me on this coding journey!`;
    
    if (navigator.share) {
      navigator.share({
        title: '100 Apps in 100 Days Challenge',
        text: text,
        url: window.location.href
      });
    } else {
      navigator.clipboard.writeText(text);
      toast({
        title: "📋 Copied to clipboard!",
        description: "Share your progress on social media!"
      });
    }
  };

  return (
    <motion.header 
      initial={{ opacity: 0, y: -50 }}
      animate={{ opacity: 1, y: 0 }}
      className="bg-black/20 backdrop-blur-lg border-b border-white/10"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-4">
            <div className="bg-gradient-to-r from-purple-500 to-blue-500 p-3 rounded-xl">
              <Code className="h-8 w-8 text-white" />
            </div>
            <div>
              <h1 className="text-2xl font-bold text-white">100 Apps Challenge</h1>
              <p className="text-purple-200">Build. Learn. Grow. Repeat.</p>
            </div>
          </div>
          <div className="flex items-center space-x-4">
            <Button onClick={shareProgress} variant="outline" className="hidden sm:flex bg-white/10 border-white/20 text-white hover:bg-white/20">
              <Share2 className="h-4 w-4 mr-2" />
              Share
            </Button>
            <Avatar className="h-10 w-10 border-2 border-purple-400">
              <AvatarImage src={userProfile?.avatar} />
              <AvatarFallback className="bg-gradient-to-r from-purple-500 to-blue-500 text-white">
                {userProfile?.name?.charAt(0) || 'D'}
              </AvatarFallback>
            </Avatar>
            <Button onClick={signOut} variant="ghost" size="icon" className="text-white/70 hover:text-white hover:bg-white/10">
                <LogOut className="h-5 w-5" />
            </Button>
          </div>
        </div>
      </div>
    </motion.header>
  );
}