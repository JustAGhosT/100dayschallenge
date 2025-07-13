#!/usr/bin/env node
const { execSync } = require('child_process');
const fs = require('fs');
const path = require('path');

// Colors for console output
const colors = {
  reset: '\x1b[0m',
  bright: '\x1b[1m',
  green: '\x1b[32m',
  cyan: '\x1b[36m',
  yellow: '\x1b[33m',
  red: '\x1b[31m'
};

console.log(`${colors.bright}${colors.cyan}=== 100 Days Challenge Deployment Script ===${colors.reset}\n`);

try {
  // Step 1: Build backend
  console.log(`${colors.yellow}Building backend...${colors.reset}`);
  execSync('cd backend && npm run build', { stdio: 'inherit' });
  console.log(`${colors.green}✓ Backend built successfully${colors.reset}\n`);

  // Step 2: Build frontend
  console.log(`${colors.yellow}Building frontend...${colors.reset}`);
  execSync('cd frontend && npm run build', { stdio: 'inherit' });
  console.log(`${colors.green}✓ Frontend built successfully${colors.reset}\n`);

  // Step 3: Copy backend functions to deployment directory
  console.log(`${colors.yellow}Preparing functions for deployment...${colors.reset}`);
  
  // Ensure the netlify/functions directory exists
  const functionsDir = path.join(__dirname, '.netlify', 'functions');
  if (!fs.existsSync(functionsDir)) {
    fs.mkdirSync(functionsDir, { recursive: true });
  }
  
  // Copy backend functions
  execSync('cp -r backend/dist/functions/* .netlify/functions/', { stdio: 'inherit' });
  console.log(`${colors.green}✓ Functions prepared for deployment${colors.reset}\n`);

  // Step 4: Run tests
  console.log(`${colors.yellow}Running tests...${colors.reset}`);
  execSync('npm test', { stdio: 'inherit' });
  console.log(`${colors.green}✓ Tests passed${colors.reset}\n`);

  console.log(`${colors.bright}${colors.green}Deployment preparation complete!${colors.reset}`);
  console.log(`${colors.cyan}You can now deploy using: netlify deploy${colors.reset}`);

} catch (error) {
  console.error(`${colors.red}Deployment preparation failed:${colors.reset}`, error);
  process.exit(1);
}