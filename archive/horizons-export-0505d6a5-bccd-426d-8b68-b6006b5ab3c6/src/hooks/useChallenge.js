
import { useState, useEffect, useCallback } from 'react';
import { supabase } from '@/lib/customSupabaseClient';
import { useToast } from '@/components/ui/use-toast';

export function useChallenge(userId) {
  const { toast } = useToast();
  const [projects, setProjects] = useState([]);
  const [activeChallenge, setActiveChallenge] = useState(null);
  const [userProfile, setUserProfile] = useState(null);
  const [isLoading, setIsLoading] = useState(true);

  const fetchActiveChallenge = useCallback(async () => {
    if (!userId) {
      setIsLoading(false);
      return null;
    }
    
    const { data, error } = await supabase
      .from('challenge_state')
      .select('*, challenges(*)')
      .eq('user_id', userId)
      .single();

    if (error && error.code !== 'PGRST116') {
      toast({ variant: "destructive", title: "Error fetching challenge", description: error.message });
      return null;
    }
    
    return data ? { ...data, ...data.challenges } : null;
  }, [userId, toast]);

  const fetchProjects = useCallback(async (challengeId) => {
    if (!userId || !challengeId) return;
    try {
      const { data, error } = await supabase
        .from('projects')
        .select('*')
        .eq('user_id', userId)
        .eq('challenge_id', challengeId)
        .order('created_at', { ascending: false });

      if (error) throw error;
      setProjects(data || []);
    } catch (error) {
      toast({ variant: "destructive", title: "Error fetching projects", description: error.message });
    }
  }, [userId, toast]);
  
  const fetchUserProfile = useCallback(async () => {
    if (!userId) return;
    try {
      const { data, error } = await supabase
        .from('profiles')
        .select('*')
        .eq('id', userId)
        .single();
      
      if (error) throw error;
      setUserProfile({
        name: data.full_name || 'Developer',
        avatar: data.avatar_url || '',
        bio: data.bio || 'On a coding adventure!',
      });

    } catch (error) {
       toast({ variant: "destructive", title: "Error fetching profile", description: error.message });
    }
  }, [userId, toast]);


  useEffect(() => {
    const loadData = async () => {
      setIsLoading(true);
      if(userId) {
        await fetchUserProfile();
        const challenge = await fetchActiveChallenge();
        if (challenge) {
          setActiveChallenge(challenge);
          await fetchProjects(challenge.id);
        }
      }
      setIsLoading(false);
    }
    loadData();
  }, [userId, fetchActiveChallenge, fetchProjects, fetchUserProfile]);


  const startChallenge = async (challengeId) => {
    if (!userId) return;
    
    const { data, error } = await supabase
      .from('challenge_state')
      .insert({ user_id: userId, challenge_id: challengeId, start_date: new Date().toISOString() })
      .select('*, challenges(*)')
      .single();

    if (error) {
      toast({ variant: "destructive", title: "Failed to start challenge", description: error.message });
      return;
    }
    
    setActiveChallenge({ ...data, ...data.challenges });
    toast({ title: "🚀 Challenge Started!", description: "Your journey begins now!" });
  };

  const addProject = async (projectData) => {
    if (!userId || !activeChallenge) return;

    const { data, error } = await supabase
      .from('projects')
      .insert({ ...projectData, user_id: userId, challenge_id: activeChallenge.id })
      .select()
      .single();

    if (error) {
      toast({ variant: "destructive", title: "Failed to add project", description: error.message });
      return;
    }
    
    setProjects(prevProjects => [data, ...prevProjects]);
    toast({ title: "✨ Project Added!", description: `${projectData.name} is in!` });
  };
  
  const completeProject = async (projectId) => {
    if (!userId) return;

    const { data, error } = await supabase
      .from('projects')
      .update({ status: 'completed', completed_at: new Date().toISOString() })
      .eq('id', projectId)
      .eq('user_id', userId)
      .select()
      .single();
      
    if (error) {
      toast({ variant: "destructive", title: "Failed to complete project", description: error.message });
      return;
    }

    setProjects(projects.map(p => (p.id === projectId ? data : p)));
    toast({ title: "🎉 Project Completed!", description: "Awesome work! One step closer!" });
  };

  return {
    projects,
    activeChallenge,
    userProfile,
    isLoading,
    startChallenge,
    addProject,
    completeProject,
  };
}
