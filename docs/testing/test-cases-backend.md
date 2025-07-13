# Backend Test Cases - 100 Days Challenge Tracker

## API Endpoint Tests

### Authentication Endpoints

#### TC-B-001: User Login - Valid Credentials

**Description**: Verify that users can successfully log in with valid credentials.

**Endpoint**: POST /api/auth/login

**Test Steps**:
1. Send POST request with valid email and name
2. Verify response status and structure

**Expected Results**:
1. Status code: 200
2. Response contains:
   - User object with id, email, name
   - Session token
   - Expiration date

**Test Data**:
```json
{
  "email": "test@example.com",
  "name": "Test User"
}
```

---

#### TC-B-002: User Login - Invalid Input

**Description**: Verify that login endpoint properly handles invalid input.

**Endpoint**: POST /api/auth/login

**Test Steps**:
1. Send POST request with missing email
2. Verify response status and error message

**Expected Results**:
1. Status code: 400
2. Response contains error message about required email

**Test Data**:
```json
{
  "name": "Test User"
}
```

---

#### TC-B-003: Get Current User

**Description**: Verify that authenticated users can retrieve their profile information.

**Endpoint**: GET /api/auth/user

**Test Steps**:
1. Send GET request with valid authentication token
2. Verify response status and user data

**Expected Results**:
1. Status code: 200
2. Response contains user object with id, email, name

**Test Data**:
- Valid authentication token in header

---

#### TC-B-004: Get Current User - Invalid Token

**Description**: Verify that the endpoint properly handles invalid authentication tokens.

**Endpoint**: GET /api/auth/user

**Test Steps**:
1. Send GET request with invalid authentication token
2. Verify response status and error message

**Expected Results**:
1. Status code: 401
2. Response contains error message about invalid token

**Test Data**:
- Invalid authentication token in header

---

### Challenge Endpoints

#### TC-B-005: Get All Challenges

**Description**: Verify that authenticated users can retrieve their challenges.

**Endpoint**: GET /api/challenges

**Test Steps**:
1. Send GET request with valid authentication token
2. Verify response status and challenge data

**Expected Results**:
1. Status code: 200
2. Response contains array of challenge objects
3. Each challenge has required fields (id, title, description, etc.)

**Test Data**:
- Valid authentication token in header

---

#### TC-B-006: Create Challenge - Valid Data

**Description**: Verify that users can create a new challenge with valid data.

**Endpoint**: POST /api/challenges

**Test Steps**:
1. Send POST request with valid challenge data
2. Verify response status and created challenge

**Expected Results**:
1. Status code: 200
2. Response contains created challenge with generated id
3. Challenge data matches input data

**Test Data**:
```json
{
  "title": "100 Days of Coding",
  "description": "Coding every day for 100 days",
  "goals": ["Improve skills", "Build portfolio"],
  "rules": ["Code daily", "Document progress"],
  "duration_days": 100
}
```

---

#### TC-B-007: Create Challenge - Invalid Data

**Description**: Verify that the endpoint properly validates challenge data.

**Endpoint**: POST /api/challenges

**Test Steps**:
1. Send POST request with missing title
2. Verify response status and error message

**Expected Results**:
1. Status code: 400
2. Response contains error message about required title

**Test Data**:
```json
{
  "description": "Coding every day for 100 days",
  "duration_days": 100
}
```

---

#### TC-B-008: Get Challenge by ID

**Description**: Verify that users can retrieve a specific challenge by ID.

**Endpoint**: GET /api/challenges/:id

**Test Steps**:
1. Send GET request with valid challenge ID
2. Verify response status and challenge data

**Expected Results**:
1. Status code: 200
2. Response contains challenge object with matching ID

**Test Data**:
- Valid challenge ID in URL
- Valid authentication token in header

---

#### TC-B-009: Get Challenge by ID - Not Found

**Description**: Verify that the endpoint properly handles requests for non-existent challenges.

**Endpoint**: GET /api/challenges/:id

**Test Steps**:
1. Send GET request with non-existent challenge ID
2. Verify response status and error message

**Expected Results**:
1. Status code: 404
2. Response contains error message about challenge not found

**Test Data**:
- Non-existent challenge ID in URL
- Valid authentication token in header

---

#### TC-B-010: Update Challenge

**Description**: Verify that users can update their challenges.

**Endpoint**: PUT /api/challenges/:id

**Test Steps**:
1. Send PUT request with updated challenge data
2. Verify response status and updated challenge

**Expected Results**:
1. Status code: 200
2. Response contains updated challenge
3. Challenge data reflects the updates

**Test Data**:
```json
{
  "title": "Updated Challenge Title",
  "description": "Updated description",
  "goals": ["Updated goal"],
  "rules": ["Updated rule"],
  "duration_days": 120
}
```

---

#### TC-B-011: Delete Challenge

**Description**: Verify that users can delete their challenges.

**Endpoint**: DELETE /api/challenges/:id

**Test Steps**:
1. Send DELETE request for an existing challenge
2. Verify response status and message
3. Attempt to retrieve the deleted challenge

**Expected Results**:
1. Status code: 200
2. Response contains success message
3. Subsequent GET request returns 404

**Test Data**:
- Valid challenge ID in URL
- Valid authentication token in header

---

### Project Endpoints

#### TC-B-012: Get Projects for Challenge

**Description**: Verify that users can retrieve projects for a specific challenge.

**Endpoint**: GET /api/projects/challenge/:challengeId

**Test Steps**:
1. Send GET request with valid challenge ID
2. Verify response status and project data

**Expected Results**:
1. Status code: 200
2. Response contains array of project objects
3. All projects belong to the specified challenge

**Test Data**:
- Valid challenge ID in URL
- Valid authentication token in header

---

#### TC-B-013: Create Project - Valid Data

**Description**: Verify that users can create a new project with valid data.

**Endpoint**: POST /api/projects/challenge/:challengeId

**Test Steps**:
1. Send POST request with valid project data
2. Verify response status and created project

**Expected Results**:
1. Status code: 200
2. Response contains created project with generated id
3. Project data matches input data

**Test Data**:
```json
{
  "title": "Portfolio Website",
  "description": "Personal portfolio website",
  "repository_url": "https://github.com/username/portfolio",
  "demo_url": "https://portfolio.example.com",
  "tech_stack": ["React", "TailwindCSS"],
  "status": "in_progress",
  "progress_percentage": 50
}
```

---

#### TC-B-014: Create Project - Invalid Data

**Description**: Verify that the endpoint properly validates project data.

**Endpoint**: POST /api/projects/challenge/:challengeId

**Test Steps**:
1. Send POST request with missing title
2. Verify response status and error message

**Expected Results**:
1. Status code: 400
2. Response contains error message about required title

**Test Data**:
```json
{
  "description": "Personal portfolio website",
  "status": "in_progress"
}
```

---

#### TC-B-015: Get Project by ID

**Description**: Verify that users can retrieve a specific project by ID.

**Endpoint**: GET /api/projects/:id

**Test Steps**:
1. Send GET request with valid project ID
2. Verify response status and project data

**Expected Results**:
1. Status code: 200
2. Response contains project object with matching ID

**Test Data**:
- Valid project ID in URL
- Valid authentication token in header

---

#### TC-B-016: Update Project

**Description**: Verify that users can update their projects.

**Endpoint**: PUT /api/projects/:id

**Test Steps**:
1. Send PUT request with updated project data
2. Verify response status and updated project

**Expected Results**:
1. Status code: 200
2. Response contains updated project
3. Project data reflects the updates

**Test Data**:
```json
{
  "title": "Updated Project Title",
  "status": "completed",
  "progress_percentage": 100
}
```

---

#### TC-B-017: Delete Project

**Description**: Verify that users can delete their projects.

**Endpoint**: DELETE /api/projects/:id

**Test Steps**:
1. Send DELETE request for an existing project
2. Verify response status and message
3. Attempt to retrieve the deleted project

**Expected Results**:
1. Status code: 200
2. Response contains success message
3. Subsequent GET request returns 404

**Test Data**:
- Valid project ID in URL
- Valid authentication token in header

---

### Dashboard Endpoint

#### TC-B-018: Get Dashboard Data

**Description**: Verify that users can retrieve their dashboard data.

**Endpoint**: GET /api/dashboard

**Test Steps**:
1. Send GET request with valid authentication token
2. Verify response status and dashboard data structure

**Expected Results**:
1. Status code: 200
2. Response contains:
   - User information
   - Challenge statistics
   - Project statistics
   - Tech stack distribution

**Test Data**:
- Valid authentication token in header

---

## Authentication Middleware Tests

#### TC-B-019: Authentication Middleware - Valid Token

**Description**: Verify that the authentication middleware correctly validates tokens.

**Test Steps**:
1. Create a mock request with valid authentication token
2. Pass request through authentication middleware
3. Verify that the request proceeds to the handler

**Expected Results**:
1. Middleware calls next() function
2. User data is attached to request object

**Test Data**:
- Valid authentication token

---

#### TC-B-020: Authentication Middleware - Missing Token

**Description**: Verify that the authentication middleware rejects requests without tokens.

**Test Steps**:
1. Create a mock request without authentication token
2. Pass request through authentication middleware
3. Verify that the middleware returns an error

**Expected Results**:
1. Middleware returns 401 status code
2. Error message indicates missing token

**Test Data**:
- Request without Authorization header

---

## Database Utility Tests

#### TC-B-021: Database Connection

**Description**: Verify that the database connection utility works correctly.

**Test Steps**:
1. Call the connectToDatabase function
2. Verify the returned database client and instance

**Expected Results**:
1. Function returns valid MongoDB client
2. Function returns valid database instance
3. Connection is cached for subsequent calls

**Test Data**:
- MongoDB connection string from environment variables

---

#### TC-B-022: Database Error Handling

**Description**: Verify that database errors are properly handled.

**Test Steps**:
1. Configure an invalid MongoDB connection string
2. Call the connectToDatabase function
3. Verify error handling

**Expected Results**:
1. Function throws an error with meaningful message
2. Error is properly logged

**Test Data**:
- Invalid MongoDB connection string