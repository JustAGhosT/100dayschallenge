export interface User {
  id: string;
  email: string;
  name: string;
  picture?: string;
  created_at: Date;
}

export interface Session {
  id: string;
  user_id: string;
  session_token: string;
  expires_at: Date;
  created_at: Date;
}

export interface Challenge {
  id: string;
  user_id: string;
  title: string;
  description: string;
  goals: string[];
  rules: string[];
  duration_days: number;
  start_date: Date;
  end_date: Date;
  created_at: Date;
  updated_at: Date;
}

export interface Project {
  id: string;
  challenge_id: string;
  user_id: string;
  title: string;
  description: string;
  repository_url?: string;
  demo_url?: string;
  tech_stack: string[];
  status: 'not_started' | 'in_progress' | 'completed';
  progress_percentage?: number;
  created_at: Date;
  updated_at: Date;
  url_status?: {
    repository?: {
      url: string;
      status: 'online' | 'offline' | 'unknown';
      last_checked: Date;
    };
    demo?: {
      url: string;
      status: 'online' | 'offline' | 'unknown';
      last_checked: Date;
    };
  };
  last_url_check?: Date;
}

export interface ApiResponse<T> {
  data?: T;
  error?: string;
  message?: string;
}