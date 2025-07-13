import { Handler } from '@netlify/functions';
import { connectToDatabase } from '../../utils/db';
import { withAuth } from '../../utils/auth';

export const handler: Handler = async (event, context) => {
  // Set CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, OPTIONS'
  };

  // Handle OPTIONS request for CORS
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 204,
      headers,
      body: ''
    };
  }

  // Only allow GET requests
  if (event.httpMethod !== 'GET') {
    return {
      statusCode: 405,
      headers,
      body: JSON.stringify({ error: 'Method not allowed' })
    };
  }

  return withAuth(getDashboardData)(event, context);
};

const getDashboardData = withAuth(async (event) => {
  try {
    const { db } = await connectToDatabase();
    const userId = event.user.id;
    
    // Get all challenges for the user
    const challenges = await db.collection('challenges')
      .find({ user_id: userId })
      .sort({ created_at: -1 })
      .toArray();
    
    // Get all projects for the user
    const projects = await db.collection('projects')
      .find({ user_id: userId })
      .sort({ created_at: -1 })
      .toArray();
    
    // Calculate stats
    const now = new Date();
    const activeChallengesToday = challenges.filter(c => 
      new Date(c.start_date) <= now && new Date(c.end_date) >= now
    );
    
    const completedChallenges = challenges.filter(c => 
      new Date(c.end_date) < now
    );
    
    const completedProjects = projects.filter(p => 
      p.status === 'completed'
    );
    
    // Calculate overall progress
    const totalProjects = projects.length;
    const overallProgress = totalProjects > 0 
      ? Math.round((completedProjects.length / totalProjects) * 100) 
      : 0;
    
    // Get tech stack distribution
    const techStackMap: Record<string, number> = {};
    projects.forEach(project => {
      project.tech_stack.forEach(tech => {
        techStackMap[tech] = (techStackMap[tech] || 0) + 1;
      });
    });
    
    // Get recent challenges and projects
    const recentChallenges = challenges.slice(0, 5);
    const recentProjects = projects.slice(0, 5);
    
    return {
      statusCode: 200,
      body: JSON.stringify({
        user: {
          id: event.user.id,
          name: event.user.name,
          email: event.user.email
        },
        stats: {
          total_challenges: challenges.length,
          active_challenges: activeChallengesToday.length,
          completed_challenges: completedChallenges.length,
          total_projects: projects.length,
          completed_projects: completedProjects.length,
          overall_progress: overallProgress
        },
        recent_challenges: recentChallenges,
        recent_projects: recentProjects,
        tech_stack_distribution: techStackMap
      })
    };
  } catch (error) {
    console.error('Error getting dashboard data:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to get dashboard data' })
    };
  }
});