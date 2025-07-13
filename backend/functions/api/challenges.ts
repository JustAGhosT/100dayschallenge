import { Handler } from '@netlify/functions';
import { v4 as uuidv4 } from 'uuid';
import { connectToDatabase } from '../../utils/db';
import { withAuth } from '../../utils/auth';
import { Challenge } from '../../types';

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
  const path = event.path.replace(/\/api\/challenges\/?/, '');
  
  if (event.httpMethod === 'GET' && !path) {
    return withAuth(getAllChallenges)(event, context);
  } else if (event.httpMethod === 'POST' && !path) {
    return withAuth(createChallenge)(event, context);
  } else if (event.httpMethod === 'GET' && path) {
    return withAuth(getChallengeById)(event, context);
  } else if (event.httpMethod === 'PUT' && path) {
    return withAuth(updateChallenge)(event, context);
  } else if (event.httpMethod === 'DELETE' && path) {
    return withAuth(deleteChallenge)(event, context);
  }

  // If no route matches
  return {
    statusCode: 404,
    headers,
    body: JSON.stringify({ error: 'Not found' })
  };
};

const getAllChallenges = withAuth(async (event) => {
  try {
    const { db } = await connectToDatabase();
    const challenges = await db.collection('challenges')
      .find({ user_id: event.user.id })
      .sort({ created_at: -1 })
      .toArray();
    
    return {
      statusCode: 200,
      body: JSON.stringify(challenges)
    };
  } catch (error) {
    console.error('Error getting challenges:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to get challenges' })
    };
  }
});

const createChallenge = withAuth(async (event) => {
  try {
    const { db } = await connectToDatabase();
    const data = JSON.parse(event.body || '{}');
    
    // Validate required fields
    if (!data.title || !data.duration_days) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: 'Title and duration_days are required' })
      };
    }
    
    // Create challenge object
    const now = new Date();
    const challenge: Challenge = {
      id: uuidv4(),
      user_id: event.user.id,
      title: data.title,
      description: data.description || '',
      goals: data.goals || [],
      rules: data.rules || [],
      duration_days: data.duration_days,
      start_date: data.start_date ? new Date(data.start_date) : now,
      end_date: new Date(now.getTime() + data.duration_days * 24 * 60 * 60 * 1000),
      created_at: now,
      updated_at: now
    };
    
    // Insert into database
    await db.collection('challenges').insertOne(challenge);
    
    return {
      statusCode: 200,
      body: JSON.stringify(challenge)
    };
  } catch (error) {
    console.error('Error creating challenge:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to create challenge' })
    };
  }
});

const getChallengeById = withAuth(async (event) => {
  try {
    const { db } = await connectToDatabase();
    const challengeId = event.path.split('/').pop();
    
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
    
    return {
      statusCode: 200,
      body: JSON.stringify(challenge)
    };
  } catch (error) {
    console.error('Error getting challenge:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to get challenge' })
    };
  }
});

const updateChallenge = withAuth(async (event) => {
  try {
    const { db } = await connectToDatabase();
    const challengeId = event.path.split('/').pop();
    const data = JSON.parse(event.body || '{}');
    
    // Find challenge
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
    
    // Update fields
    const updateData: Partial<Challenge> = {
      title: data.title || challenge.title,
      description: data.description || challenge.description,
      goals: data.goals || challenge.goals,
      rules: data.rules || challenge.rules,
      duration_days: data.duration_days || challenge.duration_days,
      updated_at: new Date()
    };
    
    // Recalculate end date if duration changed
    if (data.duration_days && data.duration_days !== challenge.duration_days) {
      updateData.end_date = new Date(
        challenge.start_date.getTime() + data.duration_days * 24 * 60 * 60 * 1000
      );
    }
    
    // Update in database
    await db.collection('challenges').updateOne(
      { id: challengeId },
      { $set: updateData }
    );
    
    // Return updated challenge
    const updatedChallenge = await db.collection('challenges').findOne({ id: challengeId });
    
    return {
      statusCode: 200,
      body: JSON.stringify(updatedChallenge)
    };
  } catch (error) {
    console.error('Error updating challenge:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to update challenge' })
    };
  }
});

const deleteChallenge = withAuth(async (event) => {
  try {
    const { db } = await connectToDatabase();
    const challengeId = event.path.split('/').pop();
    
    // Find challenge
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
    
    // Delete challenge
    await db.collection('challenges').deleteOne({ id: challengeId });
    
    // Delete associated projects
    await db.collection('projects').deleteMany({ challenge_id: challengeId });
    
    return {
      statusCode: 200,
      body: JSON.stringify({ message: 'Challenge deleted successfully' })
    };
  } catch (error) {
    console.error('Error deleting challenge:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to delete challenge' })
    };
  }
});