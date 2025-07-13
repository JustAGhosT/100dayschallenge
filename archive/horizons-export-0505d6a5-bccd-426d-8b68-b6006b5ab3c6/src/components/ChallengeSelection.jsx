import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { supabase } from '@/lib/customSupabaseClient';
import { useToast } from '@/components/ui/use-toast';
import { Button } from '@/components/ui/button';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import { Plus, Rocket } from 'lucide-react';

export function ChallengeSelection({ onChallengeSelect }) {
  const { toast } = useToast();
  const [templates, setTemplates] = useState([]);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newChallenge, setNewChallenge] = useState({ name: '', description: '', goal_apps: 100 });
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
        setTemplates(data);
      }
      setLoading(false);
    };
    fetchTemplates();
  }, [toast]);
  
  const handleCreateChallenge = async (e) => {
    e.preventDefault();
    if (!newChallenge.name || !newChallenge.goal_apps) {
        toast({ variant: "destructive", title: "Error", description: "Please fill in all required fields."});
        return;
    }

    const { data, error } = await supabase
        .from('challenges')
        .insert({
            ...newChallenge,
            goal_apps: parseInt(newChallenge.goal_apps, 10),
            is_template: false,
        })
        .select()
        .single();
    
    if (error) {
        toast({ variant: "destructive", title: "Error", description: "Could not create challenge." });
    } else {
        onChallengeSelect(data.id);
    }
  };


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
          <p className="text-purple-200">Select a template or create your own path.</p>
        </div>

        {!showCreateForm ? (
          <>
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
            <div className="text-center">
              <Button variant="outline" onClick={() => setShowCreateForm(true)} className="bg-transparent border-white/20 text-white hover:bg-white/10">
                <Plus className="h-4 w-4 mr-2" />
                Create a Personal Challenge
              </Button>
            </div>
          </>
        ) : (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }}>
            <Card className="max-w-lg mx-auto bg-white/10 border-white/20">
              <CardHeader>
                <CardTitle>Create Your Personal Challenge</CardTitle>
              </CardHeader>
              <CardContent>
                <form onSubmit={handleCreateChallenge} className="space-y-4">
                  <div>
                    <Label htmlFor="name" className="text-white">Challenge Name</Label>
                    <Input id="name" value={newChallenge.name} onChange={e => setNewChallenge({...newChallenge, name: e.target.value})} required className="bg-gray-800 border-gray-600 text-white" />
                  </div>
                  <div>
                    <Label htmlFor="description" className="text-white">Description</Label>
                    <Textarea id="description" value={newChallenge.description} onChange={e => setNewChallenge({...newChallenge, description: e.target.value})} className="bg-gray-800 border-gray-600 text-white" />
                  </div>
                  <div>
                    <Label htmlFor="goal" className="text-white">Number of Apps</Label>
                    <Input id="goal" type="number" value={newChallenge.goal_apps} onChange={e => setNewChallenge({...newChallenge, goal_apps: e.target.value})} required className="bg-gray-800 border-gray-600 text-white" />
                  </div>
                  <div className="flex gap-4">
                    <Button type="button" variant="outline" onClick={() => setShowCreateForm(false)} className="w-full bg-transparent border-white/20 text-white hover:bg-white/10">Cancel</Button>
                    <Button type="submit" className="w-full bg-gradient-to-r from-purple-500 to-blue-500">Create & Start</Button>
                  </div>
                </form>
              </CardContent>
            </Card>
          </motion.div>
        )}
      </motion.div>
    </div>
  );
}
