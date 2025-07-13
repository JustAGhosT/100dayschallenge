# 100 Days Challenge Tracker API Documentation

This document provides detailed information about the 100 Days Challenge Tracker API endpoints, request/response formats, and authentication requirements.

## Base URL

- **Development**: `http://localhost:8888/.netlify/functions`
- **Production**: `https://100days-challenge.netlify.app/.netlify/functions`

## Authentication

Most API endpoints require authentication using a Bearer token.

**Headers:**
```
Authorization: Bearer <session_token>
```

## API Endpoints

### Health Check

#### GET /api/health

Check the health status of the API and its dependencies.

**Authentication Required:** No

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2023-07-15T10:30:00Z",
  "environment": "production",
  "database": "connected"
}
```

### Authentication

#### POST /api/auth/login

Login or register a user.

**Authentication Required:** No

**Request Body:**
```json
{
  "email": "user@example.com",
  "name": "User Name",
  "picture": "https://example.com/profile.jpg"
}
```

**Response:**
```json
{
  "user": {
    "id": "user-uuid",
    "email": "user@example.com",
    "name": "User Name",
    "picture": "https://example.com/profile.jpg"
  },
  "session_token": "session-token-uuid",
  "expires_at": "2023-07-22T10:30:00Z"
}
```

#### POST /api/auth/logout

Logout a user by invalidating their session token.

**Authentication Required:** Yes

**Response:**
```json
{
  "message": "Logged out successfully"
}
```

#### GET /api/auth/user

Get the current authenticated user's information.

**Authentication Required:** Yes

**Response:**
```json
{
  "id": "user-uuid",
  "email": "user@example.com",
  "name": "User Name",
  "picture": "https://example.com/profile.jpg"
}
```

### Challenges

#### GET /api/challenges

Get all challenges for the current user.

**Authentication Required:** Yes

**Response:**
```json
[
  {
    "id": "challenge-uuid",
    "user_id": "user-uuid",
    "title": "100 Days of Web Development",
    "description": "Building web applications every day for 100 days",
    "goals": ["Learn React", "Build portfolio", "Improve CSS skills"],
    "rules": ["Code minimum 1 hour daily", "Document progress"],
    "duration_days": 100,
    "start_date": "2023-07-01T00:00:00Z",
    "end_date": "2023-10-09T00:00:00Z",
    "created_at": "2023-07-01T10:30:00Z",
    "updated_at": "2023-07-01T10:30:00Z",
    "project_count": 5,
    "completed_project_count": 2
  }
]
```

#### POST /api/challenges

Create a new challenge.

**Authentication Required:** Yes

**Request Body:**
```json
{
  "title": "100 Days of Web Development",
  "description": "Building web applications every day for 100 days",
  "goals": ["Learn React", "Build portfolio", "Improve CSS skills"],
  "rules": ["Code minimum 1 hour daily", "Document progress"],
  "duration_days": 100,
  "start_date": "2023-07-01T00:00:00Z"
}
```

**Response:**
```json
{
  "id": "challenge-uuid",
  "user_id": "user-uuid",
  "title": "100 Days of Web Development",
  "description": "Building web applications every day for 100 days",
  "goals": ["Learn React", "Build portfolio", "Improve CSS skills"],
  "rules": ["Code minimum 1 hour daily", "Document progress"],
  "duration_days": 100,
  "start_date": "2023-07-01T00:00:00Z",
  "end_date": "2023-10-09T00:00:00Z",
  "created_at": "2023-07-01T10:30:00Z",
  "updated_at": "2023-07-01T10:30:00Z",
  "project_count": 0,
  "completed_project_count": 0
}
```

#### GET /api/challenges/:id

Get a specific challenge by ID.

**Authentication Required:** Yes

**Parameters:**
- `id`: Challenge UUID

**Response:**
```json
{
  "id": "challenge-uuid",
  "user_id": "user-uuid",
  "title": "100 Days of Web Development",
  "description": "Building web applications every day for 100 days",
  "goals": ["Learn React", "Build portfolio", "Improve CSS skills"],
  "rules": ["Code minimum 1 hour daily", "Document progress"],
  "duration_days": 100,
  "start_date": "2023-07-01T00:00:00Z",
  "end_date": "2023-10-09T00:00:00Z",
  "created_at": "2023-07-01T10:30:00Z",
  "updated_at": "2023-07-01T10:30:00Z",
  "project_count": 5,
  "completed_project_count": 2
}
```

#### PUT /api/challenges/:id

Update a challenge.

**Authentication Required:** Yes

**Parameters:**
- `id`: Challenge UUID

**Request Body:**
```json
{
  "title": "Updated Challenge Title",
  "description": "Updated description",
  "goals": ["Updated goal 1", "Updated goal 2"],
  "rules": ["Updated rule 1", "Updated rule 2"],
  "duration_days": 120
}
```

**Response:**
```json
{
  "id": "challenge-uuid",
  "user_id": "user-uuid",
  "title": "Updated Challenge Title",
  "description": "Updated description",
  "goals": ["Updated goal 1", "Updated goal 2"],
  "rules": ["Updated rule 1", "Updated rule 2"],
  "duration_days": 120,
  "start_date": "2023-07-01T00:00:00Z",
  "end_date": "2023-10-29T00:00:00Z",
  "created_at": "2023-07-01T10:30:00Z",
  "updated_at": "2023-07-15T14:45:00Z",
  "project_count": 5,
  "completed_project_count": 2
}
```

#### DELETE /api/challenges/:id

Delete a challenge.

**Authentication Required:** Yes

**Parameters:**
- `id`: Challenge UUID

**Response:**
```json
{
  "message": "Challenge deleted successfully"
}
```

### Projects

#### GET /api/projects/challenge/:challengeId

Get all projects for a challenge.

**Authentication Required:** Yes

**Parameters:**
- `challengeId`: Challenge UUID

**Response:**
```json
[
  {
    "id": "project-uuid",
    "challenge_id": "challenge-uuid",
    "user_id": "user-uuid",
    "title": "Personal Portfolio Website",
    "description": "A responsive portfolio website showcasing my projects",
    "repository_url": "https://github.com/username/portfolio",
    "demo_url": "https://portfolio-demo.example.com",
    "tech_stack": ["React", "Tailwind CSS", "Node.js"],
    "status": "in_progress",
    "progress_percentage": 60,
    "created_at": "2023-07-05T14:30:00Z",
    "updated_at": "2023-07-10T09:15:00Z",
    "url_status": {
      "repository": {
        "url": "https://github.com/username/portfolio",
        "status": "online",
        "last_checked": "2023-07-15T10:30:00Z"
      },
      "demo": {
        "url": "https://portfolio-demo.example.com",
        "status": "online",
        "last_checked": "2023-07-15T10:30:00Z"
      }
    },
    "last_url_check": "2023-07-15T10:30:00Z"
  }
]
```

#### POST /api/projects/challenge/:challengeId

Create a new project for a challenge.

**Authentication Required:** Yes

**Parameters:**
- `challengeId`: Challenge UUID

**Request Body:**
```json
{
  "title": "Personal Portfolio Website",
  "description": "A responsive portfolio website showcasing my projects",
  "repository_url": "https://github.com/username/portfolio",
  "demo_url": "https://portfolio-demo.example.com",
  "tech_stack": ["React", "Tailwind CSS", "Node.js"],
  "status": "in_progress",
  "progress_percentage": 60
}
```

**Response:**
```json
{
  "id": "project-uuid",
  "challenge_id": "challenge-uuid",
  "user_id": "user-uuid",
  "title": "Personal Portfolio Website",
  "description": "A responsive portfolio website showcasing my projects",
  "repository_url": "https://github.com/username/portfolio",
  "demo_url": "https://portfolio-demo.example.com",
  "tech_stack": ["React", "Tailwind CSS", "Node.js"],
  "status": "in_progress",
  "progress_percentage": 60,
  "created_at": "2023-07-15T14:30:00Z",
  "updated_at": "2023-07-15T14:30:00Z"
}
```

#### GET /api/projects/:id

Get a specific project by ID.

**Authentication Required:** Yes

**Parameters:**
- `id`: Project UUID

**Response:**
```json
{
  "id": "project-uuid",
  "challenge_id": "challenge-uuid",
  "user_id": "user-uuid",
  "title": "Personal Portfolio Website",
  "description": "A responsive portfolio website showcasing my projects",
  "repository_url": "https://github.com/username/portfolio",
  "demo_url": "https://portfolio-demo.example.com",
  "tech_stack": ["React", "Tailwind CSS", "Node.js"],
  "status": "in_progress",
  "progress_percentage": 60,
  "created_at": "2023-07-05T14:30:00Z",
  "updated_at": "2023-07-10T09:15:00Z",
  "url_status": {
    "repository": {
      "url": "https://github.com/username/portfolio",
      "status": "online",
      "last_checked": "2023-07-15T10:30:00Z"
    },
    "demo": {
      "url": "https://portfolio-demo.example.com",
      "status": "online",
      "last_checked": "2023-07-15T10:30:00Z"
    }
  },
  "last_url_check": "2023-07-15T10:30:00Z"
}
```

#### PUT /api/projects/:id

Update a project.

**Authentication Required:** Yes

**Parameters:**
- `id`: Project UUID

**Request Body:**
```json
{
  "title": "Updated Portfolio Website",
  "description": "Updated description",
  "repository_url": "https://github.com/username/updated-portfolio",
  "demo_url": "https://updated-portfolio.example.com",
  "tech_stack": ["React", "Tailwind CSS", "Node.js", "MongoDB"],
  "status": "completed",
  "progress_percentage": 100
}
```

**Response:**
```json
{
  "id": "project-uuid",
  "challenge_id": "challenge-uuid",
  "user_id": "user-uuid",
  "title": "Updated Portfolio Website",
  "description": "Updated description",
  "repository_url": "https://github.com/username/updated-portfolio",
  "demo_url": "https://updated-portfolio.example.com",
  "tech_stack": ["React", "Tailwind CSS", "Node.js", "MongoDB"],
  "status": "completed",
  "progress_percentage": 100,
  "created_at": "2023-07-05T14:30:00Z",
  "updated_at": "2023-07-15T15:00:00Z"
}
```

#### DELETE /api/projects/:id

Delete a project.

**Authentication Required:** Yes

**Parameters:**
- `id`: Project UUID

**Response:**
```json
{
  "message": "Project deleted successfully"
}
```

### Dashboard

#### GET /api/dashboard

Get dashboard data for the current user.

**Authentication Required:** Yes

**Response:**
```json
{
  "user": {
    "id": "user-uuid",
    "name": "User Name",
    "email": "user@example.com"
  },
  "stats": {
    "total_challenges": 3,
    "active_challenges": 2,
    "completed_challenges": 1,
    "total_projects": 25,
    "completed_projects": 15,
    "overall_progress": 60
  },
  "recent_challenges": [
    {
      "id": "challenge-uuid",
      "title": "100 Days of Web Development",
      "description": "Building web applications every day for 100 days",
      "start_date": "2023-07-01T00:00:00Z",
      "end_date": "2023-10-09T00:00:00Z",
      "project_count": 5,
      "completed_project_count": 2
    }
  ],
  "recent_projects": [
    {
      "id": "project-uuid",
      "challenge_id": "challenge-uuid",
      "title": "Personal Portfolio Website",
      "status": "in_progress",
      "progress_percentage": 60,
      "tech_stack": ["React", "Tailwind CSS", "Node.js"]
    }
  ],
  "tech_stack_distribution": {
    "React": 10,
    "JavaScript": 8,
    "TypeScript": 7,
    "Node.js": 5,
    "Tailwind CSS": 4,
    "MongoDB": 3
  }
}
```

## Error Responses

All API endpoints return standard error responses in the following format:

```json
{
  "error": "Error message describing what went wrong"
}
```

### Common Error Codes

| Status Code | Description |
|-------------|-------------|
| 400 | Bad Request - Invalid input data |
| 401 | Unauthorized - Authentication required or invalid token |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 500 | Internal Server Error - Something went wrong on the server |

## Rate Limiting

API requests are limited to 100 requests per minute per user. If you exceed this limit, you will receive a 429 Too Many Requests response.

## Versioning

The current API version is v1. All endpoints are prefixed with `/api`.

---

**API Documentation Version:** 1.0  
**Last Updated:** 2023-07-15