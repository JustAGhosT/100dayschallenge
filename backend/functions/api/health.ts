import { Handler } from '@netlify/functions';
import { connectToDatabase } from '../../utils/db';

export const handler: Handler = async (event, context) => {
  // Set CORS headers
  const headers = {
    'Access-Control-Allow-Origin': '*',
    'Access-Control-Allow-Headers': 'Content-Type',
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

  try {
    // Check database connection
    const { db } = await connectToDatabase();
    const dbStatus = await db.command({ ping: 1 });
    
    return {
      statusCode: 200,
      headers,
      body: JSON.stringify({
        status: 'healthy',
        timestamp: new Date().toISOString(),
        environment: process.env.NODE_ENV || 'development',
        database: dbStatus.ok === 1 ? 'connected' : 'error'
      })
    };
  } catch (error) {
    console.error('Health check error:', error);
    
    return {
      statusCode: 200,  // Still return 200 but with error details
      headers,
      body: JSON.stringify({
        status: 'unhealthy',
        timestamp: new Date().toISOString(),
        environment: process.env.NODE_ENV || 'development',
        database: 'error',
        error: error instanceof Error ? error.message : 'Unknown error'
      })
    };
  }
};