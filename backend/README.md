# 100 Days Challenge Backend

This is the backend API for the 100 Days Challenge Tracker application, built with TypeScript and deployed on Netlify Functions.

## Tech Stack

- TypeScript
- Netlify Functions
- MongoDB

## Getting Started

1. Install dependencies:

```bash
npm install
```

2. Create a `.env` file with the following variables:

```
MONGODB_URI=your_mongodb_connection_string
DB_NAME=100days
```

3. Run the development server:

```bash
npm run dev
```

## API Endpoints

### Authentication

- `POST /api/auth/login` - Login or register a user
- `POST /api/auth/logout` - Logout a user
- `GET /api/auth/user` - Get current user

### Challenges

- `GET /api/challenges` - Get all challenges for the current user
- `POST /api/challenges` - Create a new challenge
- `GET /api/challenges/:id` - Get a specific challenge
- `PUT /api/challenges/:id` - Update a challenge
- `DELETE /api/challenges/:id` - Delete a challenge

### Projects

- `GET /api/projects/challenge/:challengeId` - Get all projects for a challenge
- `POST /api/projects/challenge/:challengeId` - Create a new project for a challenge
- `GET /api/projects/:id` - Get a specific project
- `PUT /api/projects/:id` - Update a project
- `DELETE /api/projects/:id` - Delete a project

### Dashboard

- `GET /api/dashboard` - Get dashboard data for the current user

### Health Check

- `GET /api/health` - Check API health

## Deployment

This backend is designed to be deployed on Netlify. To deploy:

1. Push your code to a Git repository
2. Connect the repository to Netlify
3. Set the build command to `npm run build`
4. Set the publish directory to `public`
5. Add environment variables in the Netlify dashboard

## Development

- `npm run build` - Build the project
- `npm run dev` - Run the development server
- `npm test` - Run tests