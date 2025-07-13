import { MongoClient, Db } from 'mongodb';

let cachedDb: Db | null = null;
let cachedClient: MongoClient | null = null;

export async function connectToDatabase(): Promise<{ db: Db; client: MongoClient }> {
  // If we already have a connection, use it
  if (cachedDb && cachedClient) {
    return { db: cachedDb, client: cachedClient };
  }

  // Get connection string from environment variables
  const uri = process.env.MONGODB_URI || 'mongodb://localhost:27017';
  const dbName = process.env.DB_NAME || '100days';

  // Connect to MongoDB
  const client = new MongoClient(uri);
  await client.connect();
  const db = client.db(dbName);

  // Cache the connection
  cachedDb = db;
  cachedClient = client;

  return { db, client };
}