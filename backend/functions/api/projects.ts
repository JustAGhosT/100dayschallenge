import { Handler } from '@netlify/functions';
import { v4 as uuidv4 } from 'uuid';
import { connectToDatabase } from '../../utils/db';
import { withAuth } from '../../utils/auth';
import { Project } from '../../types';

export const handler: Handler = async (event, context) => {
  // Set CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type, Authorization',
    'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
  };

  // Handle OPTIONS request for CORS
  if (event.httpMethod === 'OPTIONS') {
    return {
      statusCode: 204,
      headers,
      body: ''
    };
  }

  // Route based on HTTP method and path
  const path = event.path.replace(/\/api\/projects\/?/, '');
  const pathSegments = path.split('/');
  
  if (event.httpMethod === 'GET' && pathSegments[0] === 'challenge') {
    return withAuth(getProjectsByChallenge)(event, context);
  } else if (event.httpMethod === 'POST' && pathSegments[0] === 'challenge') {
    return withAuth(createProject)(event, context);
  } else if (event.httpMethod === 'GET' && path) {
    return withAuth(getProjectById)(event, context);
  } else if (event.httpMethod === 'PUT' && path) {
    return withAuth(updateProject)(event, context);
  } else if (event.httpMethod === 'DELETE' && path) {
    return withAuth(deleteProject)(event, context);
  }

  // If no route matches
  return {
    statusCode: 404,
    headers,
    body: JSON.stringify({ error: 'Not found' })
  };
};

const getProjectsByChallenge = withAuth(async (event) => {
  try {
    const { db } = await connectToDatabase();
    const challengeId = event.path.split('/').pop();
    
    // Verify challenge belongs to user
    const challenge = await db.collection('challenges').findOne({
      id: challengeId,
      user_id: event.user.id
    });
    
    if (!challenge) {
      return {
        statusCode: 404,
        body: JSON.stringify({ error: 'Challenge not found' })
      };
    }
    
    // Get projects for challenge
    const projects = await db.collection('projects')
      .find({ challenge_id: challengeId })
      .sort({ created_at: -1 })
      .toArray();
    
    return {
      statusCode: 200,
      body: JSON.stringify(projects)
    };
  } catch (error) {
    console.error('Error getting projects:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to get projects' })
    };
  }
});

const createProject = withAuth(async (event) => {
  try {
    const { db } = await connectToDatabase();
    const challengeId = event.path.split('/').pop();
    const data = JSON.parse(event.body || '{}');
    
    // Verify challenge belongs to user
    const challenge = await db.collection('challenges').findOne({
      id: challengeId,
      user_id: event.user.id
    });
    
    if (!challenge) {
      return {
        statusCode: 404,
        body: JSON.stringify({ error: 'Challenge not found' })
      };
    }
    
    // Validate required fields
    if (!data.title) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: 'Title is required' })
      };
    }
    
    // Create project object
    const now = new Date();
    const project: Project = {
      id: uuidv4(),
      challenge_id: challengeId,
      user_id: event.user.id,
      title: data.title,
      description: data.description || '',
      repository_url: data.repository_url || '',
      demo_url: data.demo_url || '',
      tech_stack: data.tech_stack || [],
      status: data.status || 'not_started',
      progress_percentage: data.progress_percentage || 0,
      created_at: now,
      updated_at: now
    };
    
    // Insert into database
    await db.collection('projects').insertOne(project);
    
    return {
      statusCode: 200,
      body: JSON.stringify(project)
    };
  } catch (error) {
    console.error('Error creating project:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to create project' })
    };
  }
});

const getProjectById = withAuth(async (event) => {
  try {
    const { db } = await connectToDatabase();
    const projectId = event.path.split('/').pop();
    
    const project = await db.collection('projects').findOne({
      id: projectId,
      user_id: event.user.id
    });
    
    if (!project) {
      return {
        statusCode: 404,
        body: JSON.stringify({ error: 'Project not found' })
      };
    }
    
    return {
      statusCode: 200,
      body: JSON.stringify(project)
    };
  } catch (error) {
    console.error('Error getting project:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to get project' })
    };
  }
});

const updateProject = withAuth(async (event) => {
  try {
    const { db } = await connectToDatabase();
    const projectId = event.path.split('/').pop();
    const data = JSON.parse(event.body || '{}');
    
    // Find project
    const project = await db.collection('projects').findOne({
      id: projectId,
      user_id: event.user.id
    });
    
    if (!project) {
      return {
        statusCode: 404,
        body: JSON.stringify({ error: 'Project not found' })
      };
    }
    
    // Update fields
    const updateData: Partial<Project> = {
      title: data.title || project.title,
      description: data.description || project.description,
      repository_url: data.repository_url !== undefined ? data.repository_url : project.repository_url,
      demo_url: data.demo_url !== undefined ? data.demo_url : project.demo_url,
      tech_stack: data.tech_stack || project.tech_stack,
      status: data.status || project.status,
      progress_percentage: data.progress_percentage !== undefined ? data.progress_percentage : project.progress_percentage,
      updated_at: new Date()
    };
    
    // Update in database
    await db.collection('projects').updateOne(
      { id: projectId },
      { $set: updateData }
    );
    
    // Return updated project
    const updatedProject = await db.collection('projects').findOne({ id: projectId });
    
    return {
      statusCode: 200,
      body: JSON.stringify(updatedProject)
    };
  } catch (error) {
    console.error('Error updating project:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to update project' })
    };
  }
});

const deleteProject = withAuth(async (event) => {
  try {
    const { db } = await connectToDatabase();
    const projectId = event.path.split('/').pop();
    
    // Find project
    const project = await db.collection('projects').findOne({
      id: projectId,
      user_id: event.user.id
    });
    
    if (!project) {
      return {
        statusCode: 404,
        body: JSON.stringify({ error: 'Project not found' })
      };
    }
    
    // Delete project
    await db.collection('projects').deleteOne({ id: projectId });
    
    return {
      statusCode: 200,
      body: JSON.stringify({ message: 'Project deleted successfully' })
    };
  } catch (error) {
    console.error('Error deleting project:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to delete project' })
    };
  }
});