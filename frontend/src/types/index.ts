export interface User {
  id: string;
  email: string;
  user_metadata?: {
    full_name?: string;
    avatar_url?: string;
  };
}

export interface Challenge {
  id: string;
  name: string;
  description: string;
  goal_apps: number;
  is_template: boolean;
  is_featured?: boolean;
  created_at: string;
}

export interface Project {
  id: string;
  name: string;
  description: string;
  technology?: string;
  category?: string;
  github_url?: string;
  live_url?: string;
  difficulty: 'beginner' | 'intermediate' | 'advanced';
  status: 'in_progress' | 'completed';
  user_id: string;
  challenge_id: string;
  created_at: string;
  completed_at?: string;
}

export interface UserProfile {
  id: string;
  full_name?: string;
  avatar_url?: string;
  bio?: string;
}

export interface ChallengeState {
  id: string;
  user_id: string;
  challenge_id: string;
  start_date: string;
  challenges?: Challenge;
}