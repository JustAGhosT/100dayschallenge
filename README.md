# 100 Days Challenge Tracker

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![Netlify Status](https://api.netlify.com/api/v1/badges/project-status/deploy-status)](https://app.netlify.com/sites/100days-challenge/deploys)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.1-blue)](https://www.typescriptlang.org/)
[![React](https://img.shields.io/badge/React-18-61dafb)](https://reactjs.org/)

A full-stack application for tracking 100-day coding challenges, built with React, TypeScript, and Netlify Functions. Create challenges, track daily projects, and visualize your progress.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Quick Start](#quick-start)
- [Installation](#installation)
- [Usage](#usage)
- [Configuration](#configuration)
- [API Reference](#api-reference)
- [Development](#development)
- [Testing](#testing)
- [Deployment](#deployment)
- [Contributing](#contributing)
- [Troubleshooting](#troubleshooting)
- [License](#license)

## Overview

### What it does
The 100 Days Challenge Tracker helps developers commit to and track their progress through 100-day coding challenges. It provides tools to create challenges, log daily projects, and visualize progress through an analytics dashboard.

### Why it matters
Consistent daily practice is key to mastering programming skills. This application helps developers maintain their commitment by providing structure, accountability, and motivation through progress tracking and visualization.

### Key capabilities
- **Challenge Management**: Create and manage multiple 100-day challenges with custom goals and rules
- **Project Tracking**: Log daily coding projects with details, repository links, and progress tracking
- **Progress Analytics**: Visualize your progress with charts and statistics
- **Portfolio Building**: Showcase your completed projects as a portfolio

## Features

### Core Features
- ✅ **User Authentication**: Secure login and registration system
- ✅ **Challenge Creation**: Create custom challenges with specific goals and rules
- ✅ **Project Management**: Add, update, and track daily coding projects
- ✅ **Progress Dashboard**: Visual representation of your challenge progress
- ✅ **Repository Integration**: Link to your GitHub repositories

### Advanced Features
- 🚀 **Tech Stack Analytics**: Track which technologies you're using most frequently
- 🚀 **URL Monitoring**: Automatic checking of repository and demo links
- 🚀 **Responsive Design**: Works on desktop, tablet, and mobile devices

### Roadmap
- 🔄 **Social Sharing**: Share your progress on social media (Q3 2023)
- 📋 **Community Challenges**: Join challenges with other developers (Q4 2023)
- 📋 **GitHub Integration**: Automatic project creation from commits (Q1 2024)

## Quick Start

### Prerequisites
- Node.js 16+
- npm or yarn
- MongoDB (local or Atlas)

### 30-Second Setup
```bash
# Clone the repository
git clone https://github.com/yourusername/100dayschallenge.git
cd 100dayschallenge

# Install dependencies
npm install

# Configure environment
cp backend/.env.example backend/.env
cp frontend/.env.development frontend/.env

# Start the development server
npm run dev
```

### Verify Installation
```bash
# Check API health
curl http://localhost:8888/.netlify/functions/api/health

# Open frontend in browser
open http://localhost:3000
```

## Installation

### Development Environment
```bash
# Clone and setup
git clone https://github.com/yourusername/100dayschallenge.git
cd 100dayschallenge
npm install

# Setup MongoDB
# Option 1: Local MongoDB
# Start MongoDB locally on port 27017

# Option 2: MongoDB Atlas
# Create a cluster and add connection string to backend/.env
```

### Production Deployment
```bash
# Using Netlify CLI
netlify login
netlify deploy --prod

# Manual deployment
npm run build
netlify deploy --prod --dir=frontend/dist --functions=backend/dist/functions
```

## Usage

### Creating a Challenge
1. Log in to your account
2. Navigate to the Challenges page
3. Click "Create Challenge"
4. Fill in the challenge details:
   - Title
   - Description
   - Duration (default: 100 days)
   - Goals
   - Rules
5. Click "Create" to start your challenge

### Adding a Project
1. Navigate to your active challenge
2. Click "Add Project"
3. Fill in the project details:
   - Title
   - Description
   - Repository URL (optional)
   - Demo URL (optional)
   - Technologies used
   - Status (Not Started, In Progress, Completed)
4. Click "Save" to add your project

### Tracking Progress
1. Navigate to the Dashboard
2. View your overall progress
3. Check statistics on:
   - Completed days
   - Technologies used
   - Consistency streak
   - Project completion rate

## Configuration

### Environment Variables
| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017` | Yes |
| `DB_NAME` | Database name | `100days` | Yes |
| `NODE_ENV` | Environment | `development` | No |
| `VITE_BACKEND_URL` | Backend API URL | `http://localhost:8888/.netlify/functions` | Yes |

### Frontend Configuration
Create a `.env` file in the frontend directory:
```
VITE_BACKEND_URL=/.netlify/functions
VITE_APP_TITLE=100 Days Challenge Tracker
```

### Backend Configuration
Create a `.env` file in the backend directory:
```
MONGODB_URI=mongodb://localhost:27017
DB_NAME=100days
NODE_ENV=development
```

## API Reference

### Core Endpoints

#### Authentication
- `POST /api/auth/login` - Login or register a user
- `POST /api/auth/logout` - Logout a user
- `GET /api/auth/user` - Get current user

#### Challenges
- `GET /api/challenges` - Get all challenges for the current user
- `POST /api/challenges` - Create a new challenge
- `GET /api/challenges/:id` - Get a specific challenge
- `PUT /api/challenges/:id` - Update a challenge
- `DELETE /api/challenges/:id` - Delete a challenge

#### Projects
- `GET /api/projects/challenge/:challengeId` - Get all projects for a challenge
- `POST /api/projects/challenge/:challengeId` - Create a new project for a challenge
- `GET /api/projects/:id` - Get a specific project
- `PUT /api/projects/:id` - Update a project
- `DELETE /api/projects/:id` - Delete a project

#### Dashboard
- `GET /api/dashboard` - Get dashboard data for the current user

For complete API documentation, see [API Docs](./docs/api.md).

## Development

### Setup Development Environment
```bash
# Install development dependencies
npm install

# Start development server
npm run dev

# Run frontend only
npm run dev:frontend

# Run backend only
npm run dev:backend
```

### Project Structure
```
100dayschallenge/
├── frontend/             # React TypeScript frontend
│   ├── src/             # Source code
│   │   ├── components/  # React components
│   │   ├── contexts/    # React contexts
│   │   ├── hooks/       # Custom hooks
│   │   ├── lib/         # Utilities
│   │   └── types/       # TypeScript types
│   ├── public/          # Static assets
│   └── index.html       # HTML template
├── backend/             # Netlify Functions backend
│   ├── functions/       # API endpoints
│   ├── types/           # TypeScript types
│   └── utils/           # Utilities
├── tests/               # Test files
│   ├── backend_test.py  # Backend tests
│   ├── frontend_test.py # Frontend tests
│   └── integration_test.py # Integration tests
└── docs/                # Documentation
```

### Code Standards
- **Language**: TypeScript
- **Frontend**: React, Vite, TailwindCSS
- **Backend**: TypeScript, Netlify Functions
- **Database**: MongoDB
- **Testing**: Jest, React Testing Library, Python unittest

## Testing

### Running Tests
```bash
# All tests
npm test

# Backend tests
npm run test:backend

# Frontend tests
npm run test:frontend

# Integration tests
npm run test:integration
```

### Test Structure
```
tests/
├── backend_test.py      # Backend API tests
├── frontend_test.py     # Frontend UI tests
├── integration_test.py  # End-to-end tests
└── run_tests.py         # Test runner
```

## Deployment

### Netlify Deployment
1. Push your code to GitHub
2. Connect your repository to Netlify
3. Configure build settings:
   - Base directory: `/`
   - Build command: `npm run build`
   - Publish directory: `frontend/dist`
   - Functions directory: `backend/dist/functions`
4. Add environment variables in Netlify dashboard
5. Deploy

### Monitoring
- **Health Checks**: `/.netlify/functions/api/health` endpoint
- **Function Logs**: Available in Netlify dashboard
- **Analytics**: Netlify Analytics

## Contributing

We welcome contributions! Please follow these steps:

### Development Workflow
1. Fork the repository
2. Create a feature branch: `git checkout -b feature/your-feature`
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass: `npm test`
6. Submit a pull request

### Issues and Discussions
- 🐛 **Bug Reports**: [GitHub Issues](https://github.com/yourusername/100dayschallenge/issues)
- 💡 **Feature Requests**: [GitHub Discussions](https://github.com/yourusername/100dayschallenge/discussions)

## Troubleshooting

### Common Issues

#### MongoDB Connection Failed
```bash
# Check MongoDB is running
mongosh

# Verify connection string in backend/.env
cat backend/.env
```

#### API Errors
```bash
# Check API health
curl http://localhost:8888/.netlify/functions/api/health

# Check Netlify Function logs
netlify functions:logs
```

#### Frontend Build Issues
```bash
# Clear node_modules and reinstall
rm -rf frontend/node_modules
npm install

# Check for TypeScript errors
cd frontend && npm run tsc
```

### Getting Help
- 📖 **Documentation**: [Full Documentation](./docs/)
- 💬 **GitHub Discussions**: [Ask questions](https://github.com/yourusername/100dayschallenge/discussions)

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

**Built with ❤️ by [Your Name/Team]**

*Last updated: July 2023*