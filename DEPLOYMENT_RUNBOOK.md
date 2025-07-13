# Deployment Runbook - 100 Days Challenge

**Document Type:** Runbook  
**Service/Component:** 100 Days Challenge Tracker  
**Version:** 1.0  
**Last Updated:** 2023-07-15  
**Owner:** Development Team  
**Reviewers:** DevOps, QA  

## Service Overview

### Purpose
The 100 Days Challenge Tracker is a full-stack application that allows users to create and track 100-day coding challenges, manage projects within challenges, and visualize progress through analytics dashboards.

### Business Impact
**High Impact:** Complete service outage prevents users from tracking their progress, creating new challenges, or accessing their data.  
**Medium Impact:** Slow API responses or intermittent errors degrade user experience but core functionality remains available.  
**Low Impact:** Minor UI issues or non-critical feature unavailability that doesn't affect core challenge tracking.  

### Service Level Objectives (SLOs)
| Metric | Target | Measurement |
|--------|--------|-------------|
| Availability | 99.9% | Netlify uptime monitoring |
| Response Time | < 300ms p95 | API latency in Netlify Functions |
| Error Rate | < 0.5% | Function error logs |
| Throughput | 100 req/min | Request metrics |

## System Architecture

### Application Structure
```
Frontend (React/TypeScript)
├── UI Components: React components with TailwindCSS
├── State Management: React Context API
└── API Client: Fetch API with custom hooks

Backend (Netlify Functions/TypeScript)
├── API Gateway: Netlify Functions
├── Core Logic: TypeScript business logic
└── Database Layer: MongoDB connection utilities

Infrastructure
├── Data Storage: MongoDB Atlas
├── Hosting: Netlify
└── CI/CD: GitHub Actions
```

### Key Dependencies
| Dependency | Type | Impact if Down | Contact |
|------------|------|----------------|---------|
| MongoDB Atlas | Critical | Data unavailable | MongoDB Support |
| Netlify | Critical | Service unavailable | Netlify Support |
| GitHub | Important | Deployment pipeline broken | GitHub Support |
| Auth Provider | Critical | Users cannot login | Auth Provider Support |

## Monitoring & Alerting

### Key Metrics
| Metric | Dashboard Link | Normal Range | Alert Threshold |
|--------|----------------|--------------|-----------------|
| Function Invocations | Netlify Functions | 0-1000/hr | >2000/hr |
| Function Duration | Netlify Functions | 50-200ms | >500ms |
| Function Errors | Netlify Functions | 0-5/day | >20/day |
| MongoDB Connections | MongoDB Atlas | 5-50 | >100 |

### Alert Channels
- **Critical Alerts**: Email to team + SMS to on-call
- **Warning Alerts**: Email to team
- **Info Alerts**: Slack channel #100days-alerts

### Dashboards
- **Netlify Overview**: https://app.netlify.com/sites/100days-challenge/overview
- **Function Metrics**: https://app.netlify.com/sites/100days-challenge/functions
- **MongoDB Atlas**: https://cloud.mongodb.com/v2/projects
- **Error Tracking**: Netlify Function logs

## Common Operational Tasks

### Health Checks

#### Basic Health Check
```bash
# Check API health
curl -s https://100days-challenge.netlify.app/.netlify/functions/api/health | jq

# Expected response:
{
  "status": "healthy",
  "timestamp": "2023-07-15T10:30:00Z",
  "environment": "production",
  "database": "connected"
}
```

#### Detailed Health Check
```bash
# Check MongoDB connection
curl -s https://100days-challenge.netlify.app/.netlify/functions/api/health/detailed | jq

# Check frontend loading
curl -s -I https://100days-challenge.netlify.app/

# Verify authentication flow
# (Use browser to test login flow)
```

### Service Restart

#### Netlify Functions Restart
```bash
# Redeploy functions to restart them
netlify deploy --prod --functions ./backend/dist/functions

# Or trigger a new deployment from Netlify UI
# Go to https://app.netlify.com/sites/100days-challenge/deploys
# Click "Trigger deploy" > "Deploy site"
```

#### Emergency Restart
```bash
# Clear Netlify cache and redeploy
netlify deploy --prod --functions ./backend/dist/functions --clear

# If issues persist, contact Netlify support
```

### Scaling Operations

#### Function Scaling
Netlify Functions automatically scale based on demand. No manual intervention required.

#### Database Scaling
```bash
# MongoDB Atlas scaling is done through the UI
# 1. Log in to MongoDB Atlas
# 2. Select your cluster
# 3. Click "..." > "Edit Configuration"
# 4. Adjust cluster tier as needed
```

### Configuration Updates

#### Environment Variables
```bash
# Update via Netlify UI
# 1. Go to https://app.netlify.com/sites/100days-challenge/settings/env
# 2. Add or edit environment variables
# 3. Trigger a new deployment to apply changes

# Or use Netlify CLI
netlify env:set VARIABLE_NAME "new value"
netlify deploy --prod
```

#### Frontend Configuration
```bash
# Update frontend environment variables
# 1. Edit frontend/.env
# 2. Commit and push changes
# 3. Trigger a new deployment
```

## Incident Response Procedures

### Severity Levels

#### P0 - Critical (Service Down)
**Response Time:** Immediate (< 15 minutes)
1. **Verify the issue** using health checks
2. **Check Netlify status** at https://www.netlifystatus.com/
3. **Check MongoDB Atlas status** at https://status.mongodb.com/
4. **Review recent deployments** in Netlify dashboard
5. **Rollback to last working version** if recent deployment caused the issue
6. **Contact Netlify support** if issue persists
7. **Update status page** and notify users

#### P1 - High (Degraded Performance)
**Response Time:** < 1 hour
1. **Investigate function metrics** in Netlify dashboard
2. **Check MongoDB performance** in Atlas dashboard
3. **Review error logs** for patterns
4. **Identify bottlenecks** in API or database
5. **Apply fixes** as needed (optimize queries, etc.)
6. **Monitor closely** for improvement

#### P2 - Medium (Minor Issues)
**Response Time:** < 24 hours
1. **Document the issue** in tracking system
2. **Investigate root cause**
3. **Develop fix** and test in staging
4. **Deploy fix** during low-traffic period

### Escalation Matrix
| Level | Contact | When to Escalate |
|-------|---------|------------------|
| L1 | Development Team | All issues |
| L2 | Tech Lead | 30 min for P0, 4 hrs for P1 |
| L3 | Project Manager | 1 hr for P0, 8 hrs for P1 |
| L4 | External Support | If infrastructure issue persists >2 hrs |

## Troubleshooting Guide

### API Errors

#### Check Function Logs
```bash
# View function logs in Netlify UI
# Go to https://app.netlify.com/sites/100days-challenge/functions
# Click on the function name to view logs

# Or use Netlify CLI
netlify functions:invoke api/health --no-identity

# Check for common errors
netlify functions:logs | grep "Error"
```

#### Common Issues
| Symptom | Likely Cause | Solution |
|---------|--------------|----------|
| 500 Internal Server Error | MongoDB connection issue | Check MongoDB Atlas status and connection string |
| 401 Unauthorized | Authentication issue | Verify auth provider and tokens |
| 404 Not Found | Incorrect API path | Check API routes and client requests |
| Timeout | Long-running function | Optimize database queries or function code |

### Database Issues

#### Investigation Steps
```bash
# Check MongoDB Atlas status
# Go to https://cloud.mongodb.com/v2/projects
# Select your project and cluster

# Review connection statistics
# Check "Metrics" tab in MongoDB Atlas

# Test connection from local environment
mongosh "mongodb+srv://cluster0.example.mongodb.net/100days" --username <username>
```

#### Common Causes
- **Connection limits**: Increase connection pool in MongoDB Atlas
- **Slow queries**: Add indexes for frequently queried fields
- **Network issues**: Check Netlify to MongoDB connectivity
- **Authentication**: Verify database credentials in environment variables

### Frontend Issues

#### Diagnosis
```bash
# Check browser console for errors
# Open browser developer tools (F12) > Console

# Verify API responses
# Open browser developer tools (F12) > Network

# Test with different browsers
# Try Chrome, Firefox, Safari, and Edge
```

#### Resolution
1. **Clear browser cache**: Hard refresh (Ctrl+F5)
2. **Update frontend code**: Fix any JavaScript errors
3. **Check API compatibility**: Ensure frontend and API versions match
4. **Redeploy frontend**: Trigger a new deployment

## Maintenance Procedures

### Deployment Process

#### Pre-Deployment Checklist
- [ ] All tests passing in CI/CD
- [ ] Database migrations tested in staging
- [ ] Frontend builds without errors
- [ ] Backend functions compile successfully
- [ ] Environment variables configured correctly

#### Deployment Steps
```bash
# 1. Build the application
npm run build

# 2. Test the build locally
npm run start:local

# 3. Deploy to staging
netlify deploy

# 4. Test in staging environment
# Run manual tests on staging URL

# 5. Deploy to production
netlify deploy --prod

# 6. Verify deployment
curl -s https://100days-challenge.netlify.app/.netlify/functions/api/health | jq
```

#### Post-Deployment Verification
- [ ] Health check returns "healthy"
- [ ] Login flow works correctly
- [ ] Challenge creation works
- [ ] Project creation works
- [ ] Dashboard loads with correct data

### Database Maintenance

#### Backup Procedures
```bash
# MongoDB Atlas automatic backups
# 1. Log in to MongoDB Atlas
# 2. Go to "Backup" section
# 3. Configure backup schedule (daily recommended)
# 4. Set retention period (30 days recommended)

# Manual backup
# Use MongoDB Atlas UI to create on-demand backup
```

#### Index Maintenance
```bash
# Check index usage in MongoDB Atlas
# 1. Go to "Performance Advisor"
# 2. Review recommended indexes

# Create new indexes as needed
db.challenges.createIndex({ "user_id": 1, "created_at": -1 })
db.projects.createIndex({ "challenge_id": 1 })
```

### Security Updates

#### Dependency Updates
```bash
# Check for vulnerabilities
npm audit

# Update dependencies
npm update

# Update with breaking changes
npm install package@latest

# After updates, test thoroughly before deploying
```

## Disaster Recovery

### Backup Strategy
- **Database**: MongoDB Atlas continuous backups
- **Code**: GitHub repository
- **Configuration**: Environment variables backed up securely
- **Deployment**: Netlify deployment history

### Recovery Procedures

#### Database Recovery
```bash
# Restore from MongoDB Atlas backup
# 1. Log in to MongoDB Atlas
# 2. Go to "Backup" section
# 3. Select point-in-time or snapshot backup
# 4. Click "Restore"
# 5. Select target cluster
# 6. Confirm restoration
```

#### Complete Service Recovery
```bash
# 1. Restore database from backup if needed
# (Follow Database Recovery steps above)

# 2. Redeploy application
git clone https://github.com/yourusername/100dayschallenge.git
cd 100dayschallenge
npm install
npm run build
netlify deploy --prod

# 3. Verify recovery
curl -s https://100days-challenge.netlify.app/.netlify/functions/api/health | jq
```

### RTO/RPO Targets
- **Recovery Time Objective (RTO)**: 2 hours
- **Recovery Point Objective (RPO)**: 24 hours
- **Mean Time to Recovery (MTTR)**: 1 hour

## Contacts & Resources

### Key Contacts
| Role | Contact | Responsibility |
|------|---------|----------------|
| Tech Lead | tech.lead@example.com | Technical decisions |
| DevOps | devops@example.com | Infrastructure issues |
| Database Admin | dba@example.com | MongoDB issues |
| Support | support@example.com | User-facing issues |

### Important Links
- **GitHub Repository**: https://github.com/yourusername/100dayschallenge
- **Netlify Dashboard**: https://app.netlify.com/sites/100days-challenge
- **MongoDB Atlas**: https://cloud.mongodb.com/v2/projects
- **Documentation**: https://github.com/yourusername/100dayschallenge/wiki
- **Issue Tracker**: https://github.com/yourusername/100dayschallenge/issues

### Emergency Contacts
- **Netlify Support**: https://www.netlify.com/support/
- **MongoDB Support**: https://support.mongodb.com/
- **Auth Provider Support**: [Auth provider support URL]

## Change Log

| Date | Version | Change Description | Author |
|------|---------|-------------------|--------|
| 2023-07-15 | 1.0 | Initial runbook creation | Development Team |

---

**Last Reviewed:** 2023-07-15  
**Next Review Due:** 2024-01-15