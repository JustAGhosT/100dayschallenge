import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { supabase } from '@/lib/customSupabaseClient';
import { useToast } from '@/components/ui/use-toast';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Rocket } from 'lucide-react';
import type { Challenge } from '@/types';

interface ChallengeSelectionProps {
  onChallengeSelect: (challengeId: string) => void;
}

export function ChallengeSelection({ onChallengeSelect }: ChallengeSelectionProps) {
  const { toast } = useToast();
  const [templates, setTemplates] = useState<Challenge[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchTemplates = async () => {
      setLoading(true);
      const { data, error } = await supabase
        .from('challenges')
        .select('*')
        .eq('is_template', true);
      
      if (error) {
        toast({ variant: "destructive", title: "Error", description: "Could not fetch challenge templates." });
      } else {
        setTemplates(data || []);
      }
      setLoading(false);
    };
    fetchTemplates();
  }, [toast]);

  if (loading) {
    return <div className="flex items-center justify-center h-full">Loading templates...</div>;
  }

  return (
    <div className="flex flex-col items-center justify-center min-h-screen p-4">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        className="max-w-4xl w-full"
      >
        <div className="text-center mb-10">
          <h1 className="text-4xl font-bold mb-2">Choose Your Challenge</h1>
          <p className="text-purple-200">Select a template to start your journey.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6 mb-8">
          {templates.map((template, index) => (
            <motion.div
              key={template.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: index * 0.1 }}
            >
              <Card className="bg-white/10 border-white/20 hover:border-purple-400 transition-all h-full flex flex-col">
                <CardHeader>
                  <CardTitle className="text-white">{template.name}</CardTitle>
                </CardHeader>
                <CardContent className="flex-grow flex flex-col justify-between">
                  <p className="text-purple-200 mb-4">{template.description}</p>
                  <Button onClick={() => onChallengeSelect(template.id)} className="w-full mt-auto bg-gradient-to-r from-purple-500 to-blue-500">
                    <Rocket className="h-4 w-4 mr-2" />
                    Start This Challenge
                  </Button>
                </CardContent>
              </Card>
            </motion.div>
          ))}
        </div>
      </motion.div>
    </div>
  );
}