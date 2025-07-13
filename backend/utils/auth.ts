import { Handler } from '@netlify/functions';
import { connectToDatabase } from './db';
import { Session, User } from '../types';

export interface AuthenticatedEvent {
  user: User;
  session: Session;
}

export const withAuth = (handler: (event: AuthenticatedEvent) => Promise<any>): Handler => {
  return async (event, context) => {
    // Allow OPTIONS requests for CORS
    if (event.httpMethod === 'OPTIONS') {
      return {
        statusCode: 204,
        headers: {
          'Access-Control-Allow-Origin': '*',
          'Access-Control-Allow-Headers': 'Content-Type, Authorization',
          'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS'
        },
        body: ''
      };
    }

    // Get authorization header
    const authHeader = event.headers.authorization || '';
    if (!authHeader.startsWith('Bearer ')) {
      return {
        statusCode: 401,
        body: JSON.stringify({ error: 'Unauthorized: Missing or invalid token' })
      };
    }

    const token = authHeader.split(' ')[1];
    
    try {
      // Connect to database
      const { db } = await connectToDatabase();
      
      // Find session
      const session = await db.collection('sessions').findOne({ session_token: token });
      if (!session) {
        return {
          statusCode: 401,
          body: JSON.stringify({ error: 'Unauthorized: Invalid token' })
        };
      }
      
      // Check if session is expired
      if (new Date(session.expires_at) < new Date()) {
        return {
          statusCode: 401,
          body: JSON.stringify({ error: 'Unauthorized: Token expired' })
        };
      }
      
      // Find user
      const user = await db.collection('users').findOne({ id: session.user_id });
      if (!user) {
        return {
          statusCode: 401,
          body: JSON.stringify({ error: 'Unauthorized: User not found' })
        };
      }
      
      // Call handler with authenticated user
      return await handler({ ...event, user, session });
    } catch (error) {
      console.error('Authentication error:', error);
      return {
        statusCode: 500,
        body: JSON.stringify({ error: 'Internal server error' })
      };
    }
  };
};