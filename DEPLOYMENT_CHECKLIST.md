# Deployment Checklist

Use this checklist to ensure your 100 Days Challenge application is ready for deployment.

## Prerequisites

- [ ] MongoDB Atlas account created (for production database)
- [ ] Netlify account created
- [ ] GitHub repository created

## Local Development Setup

- [ ] All dependencies installed (`npm install` at root)
- [ ] Backend environment variables set in `backend/.env`
- [ ] Frontend environment variables set in `frontend/.env`
- [ ] Local development server runs without errors (`npm run dev`)
- [ ] API endpoints work locally
- [ ] Frontend connects to local API successfully

## Testing

- [ ] Backend tests pass (`npm run test:backend`)
- [ ] Frontend tests pass (`npm run test:frontend`)
- [ ] Integration tests pass (`npm run test`)

## Pre-Deployment

- [ ] Update MongoDB connection string in `backend/.env` to production database
- [ ] Set `NODE_ENV=production` in `backend/.env`
- [ ] Ensure all API endpoints are properly secured
- [ ] Check for any hardcoded development URLs
- [ ] Run build process to verify it completes without errors (`npm run build`)

## Netlify Setup

- [ ] Connect GitHub repository to Netlify
- [ ] Configure build settings:
  - [ ] Base directory: `/`
  - [ ] Build command: `npm run build`
  - [ ] Publish directory: `frontend/dist`
  - [ ] Functions directory: `backend/dist/functions`
- [ ] Add environment variables in Netlify dashboard:
  - [ ] `MONGODB_URI` - MongoDB Atlas connection string
  - [ ] `DB_NAME` - Production database name
  - [ ] `NODE_ENV` - Set to `production`
  - [ ] Any other required environment variables

## Post-Deployment

- [ ] Verify frontend loads correctly
- [ ] Test authentication flow
- [ ] Create a test challenge
- [ ] Create a test project
- [ ] Verify dashboard analytics
- [ ] Check mobile responsiveness

## Performance & Monitoring

- [ ] Enable Netlify Analytics
- [ ] Set up MongoDB Atlas monitoring
- [ ] Configure error logging
- [ ] Set up uptime monitoring

## Security

- [ ] Enable HTTPS (automatic with Netlify)
- [ ] Check for exposed API keys or secrets
- [ ] Verify authentication is working properly
- [ ] Ensure proper CORS configuration

## Backup & Recovery

- [ ] Configure MongoDB Atlas backups
- [ ] Document recovery procedures
- [ ] Test restore process