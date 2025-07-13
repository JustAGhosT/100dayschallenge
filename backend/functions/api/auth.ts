import { Handler } from '@netlify/functions';
import { v4 as uuidv4 } from 'uuid';
import { connectToDatabase } from '../../utils/db';
import { User, Session } from '../../types';

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
  const path = event.path.replace(/\/api\/auth\/?/, '');
  
  if (event.httpMethod === 'POST' && path === 'login') {
    return handleLogin(event);
  } else if (event.httpMethod === 'POST' && path === 'logout') {
    return handleLogout(event);
  } else if (event.httpMethod === 'GET' && path === 'user') {
    return getCurrentUser(event);
  }

  // If no route matches
  return {
    statusCode: 404,
    headers,
    body: JSON.stringify({ error: 'Not found' })
  };
};

const handleLogin = async (event: any) => {
  try {
    const { db } = await connectToDatabase();
    const data = JSON.parse(event.body || '{}');
    
    // In a real app, you would validate credentials here
    // For this example, we'll just check if the user exists by email
    if (!data.email) {
      return {
        statusCode: 400,
        body: JSON.stringify({ error: 'Email is required' })
      };
    }
    
    // Find or create user
    let user = await db.collection('users').findOne({ email: data.email });
    
    if (!user) {
      // Create new user
      const now = new Date();
      const newUser: User = {
        id: uuidv4(),
        email: data.email,
        name: data.name || data.email.split('@')[0],
        picture: data.picture || '',
        created_at: now
      };
      
      await db.collection('users').insertOne(newUser);
      user = newUser;
    }
    
    // Create session
    const now = new Date();
    const expiresAt = new Date(now.getTime() + 7 * 24 * 60 * 60 * 1000); // 7 days
    
    const session: Session = {
      id: uuidv4(),
      user_id: user.id,
      session_token: uuidv4(),
      expires_at: expiresAt,
      created_at: now
    };
    
    await db.collection('sessions').insertOne(session);
    
    return {
      statusCode: 200,
      body: JSON.stringify({
        user: {
          id: user.id,
          email: user.email,
          name: user.name,
          picture: user.picture
        },
        session_token: session.session_token,
        expires_at: session.expires_at
      })
    };
  } catch (error) {
    console.error('Error during login:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to login' })
    };
  }
};

const handleLogout = async (event: any) => {
  try {
    const { db } = await connectToDatabase();
    const authHeader = event.headers.authorization || '';
    
    if (!authHeader.startsWith('Bearer ')) {
      return {
        statusCode: 401,
        body: JSON.stringify({ error: 'Unauthorized' })
      };
    }
    
    const token = authHeader.split(' ')[1];
    
    // Delete session
    await db.collection('sessions').deleteOne({ session_token: token });
    
    return {
      statusCode: 200,
      body: JSON.stringify({ message: 'Logged out successfully' })
    };
  } catch (error) {
    console.error('Error during logout:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to logout' })
    };
  }
};

const getCurrentUser = async (event: any) => {
  try {
    const { db } = await connectToDatabase();
    const authHeader = event.headers.authorization || '';
    
    if (!authHeader.startsWith('Bearer ')) {
      return {
        statusCode: 401,
        body: JSON.stringify({ error: 'Unauthorized' })
      };
    }
    
    const token = authHeader.split(' ')[1];
    
    // Find session
    const session = await db.collection('sessions').findOne({ session_token: token });
    if (!session) {
      return {
        statusCode: 401,
        body: JSON.stringify({ error: 'Invalid token' })
      };
    }
    
    // Check if session is expired
    if (new Date(session.expires_at) < new Date()) {
      return {
        statusCode: 401,
        body: JSON.stringify({ error: 'Token expired' })
      };
    }
    
    // Find user
    const user = await db.collection('users').findOne({ id: session.user_id });
    if (!user) {
      return {
        statusCode: 404,
        body: JSON.stringify({ error: 'User not found' })
      };
    }
    
    return {
      statusCode: 200,
      body: JSON.stringify({
        id: user.id,
        email: user.email,
        name: user.name,
        picture: user.picture
      })
    };
  } catch (error) {
    console.error('Error getting current user:', error);
    return {
      statusCode: 500,
      body: JSON.stringify({ error: 'Failed to get user' })
    };
  }
};