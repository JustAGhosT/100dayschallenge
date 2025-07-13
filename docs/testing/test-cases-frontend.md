# Frontend Test Cases - 100 Days Challenge Tracker

## Component Tests

### Authentication Components

#### TC-F-001: Login Form Validation

**Description**: Verify that the login form properly validates user input.

**Preconditions**:
- Login form is rendered

**Test Steps**:
1. Attempt to submit the form without entering email
2. Enter invalid email format and submit
3. Enter valid email but no password and submit
4. Enter valid email and password and submit

**Expected Results**:
1. Form shows error message for required email
2. Form shows error message for invalid email format
3. Form shows error message for required password
4. Form submits successfully

**Test Data**:
- Invalid email: "notanemail"
- Valid email: "test@example.com"
- Valid password: "password123"

---

#### TC-F-002: Registration Form Validation

**Description**: Verify that the registration form properly validates user input.

**Preconditions**:
- Registration form is rendered

**Test Steps**:
1. Attempt to submit the form without entering name
2. Attempt to submit the form without entering email
3. Enter invalid email format and submit
4. Enter valid details and submit

**Expected Results**:
1. Form shows error message for required name
2. Form shows error message for required email
3. Form shows error message for invalid email format
4. Form submits successfully

**Test Data**:
- Valid name: "Test User"
- Invalid email: "notanemail"
- Valid email: "test@example.com"

---

### Challenge Components

#### TC-F-003: Challenge Card Rendering

**Description**: Verify that challenge cards render correctly with all required information.

**Preconditions**:
- User is logged in
- User has at least one challenge

**Test Steps**:
1. Navigate to challenges page
2. Observe challenge card elements

**Expected Results**:
1. Challenge card displays:
   - Challenge title
   - Description
   - Progress indicator
   - Start and end dates
   - Number of projects

**Test Data**:
- Challenge with title, description, dates, and projects

---

#### TC-F-004: Challenge Form Validation

**Description**: Verify that the challenge creation form properly validates user input.

**Preconditions**:
- User is logged in
- Challenge creation form is rendered

**Test Steps**:
1. Attempt to submit the form without entering title
2. Enter title but no description and submit
3. Enter negative number for duration and submit
4. Enter valid details and submit

**Expected Results**:
1. Form shows error message for required title
2. Form submits successfully (description is optional)
3. Form shows error message for invalid duration
4. Form submits successfully

**Test Data**:
- Valid title: "100 Days of Coding"
- Valid description: "Coding every day for 100 days"
- Invalid duration: -10
- Valid duration: 100

---

### Project Components

#### TC-F-005: Project Card Rendering

**Description**: Verify that project cards render correctly with all required information.

**Preconditions**:
- User is logged in
- User has at least one project

**Test Steps**:
1. Navigate to a challenge with projects
2. Observe project card elements

**Expected Results**:
1. Project card displays:
   - Project title
   - Description
   - Status indicator
   - Technology tags
   - Repository and demo links (if provided)

**Test Data**:
- Project with title, description, status, and tech stack

---

#### TC-F-006: Project Form Validation

**Description**: Verify that the project creation form properly validates user input.

**Preconditions**:
- User is logged in
- Project creation form is rendered

**Test Steps**:
1. Attempt to submit the form without entering title
2. Enter invalid URL for repository and submit
3. Enter invalid URL for demo and submit
4. Enter valid details and submit

**Expected Results**:
1. Form shows error message for required title
2. Form shows error message for invalid repository URL
3. Form shows error message for invalid demo URL
4. Form submits successfully

**Test Data**:
- Valid title: "Portfolio Website"
- Invalid URL: "notaurl"
- Valid URL: "https://github.com/username/repo"

---

### Dashboard Components

#### TC-F-007: Progress Chart Rendering

**Description**: Verify that the progress chart renders correctly with accurate data.

**Preconditions**:
- User is logged in
- User has at least one active challenge

**Test Steps**:
1. Navigate to dashboard
2. Observe progress chart

**Expected Results**:
1. Progress chart displays:
   - Correct number of days completed
   - Correct percentage of completion
   - Visual representation of progress

**Test Data**:
- Challenge with known progress data

---

#### TC-F-008: Tech Stack Distribution Visualization

**Description**: Verify that the tech stack distribution chart renders correctly.

**Preconditions**:
- User is logged in
- User has projects with technology tags

**Test Steps**:
1. Navigate to dashboard
2. Observe tech stack distribution chart

**Expected Results**:
1. Tech stack chart displays:
   - All used technologies
   - Correct distribution percentages
   - Color-coded visualization

**Test Data**:
- Projects with various technology tags

---

## Hook Tests

#### TC-F-009: useChallenge Hook - Challenge Fetching

**Description**: Verify that the useChallenge hook correctly fetches challenge data.

**Preconditions**:
- Mock API response for challenges

**Test Steps**:
1. Render a test component using the useChallenge hook
2. Call the fetchChallenges method
3. Verify the returned data

**Expected Results**:
1. Hook returns the correct challenge data
2. Loading state is managed correctly
3. Error state is handled properly

**Test Data**:
- Mock challenge data array

---

#### TC-F-010: useAuth Hook - Authentication State

**Description**: Verify that the useAuth hook correctly manages authentication state.

**Preconditions**:
- Mock authentication API responses

**Test Steps**:
1. Render a test component using the useAuth hook
2. Call the login method with valid credentials
3. Verify authentication state
4. Call the logout method
5. Verify authentication state

**Expected Results**:
1. After login, isAuthenticated is true and user data is available
2. After logout, isAuthenticated is false and user data is cleared

**Test Data**:
- Valid credentials: { email: "test@example.com", password: "password123" }
- Mock user data

---

## Form Submission Tests

#### TC-F-011: Challenge Creation Form Submission

**Description**: Verify that the challenge creation form correctly submits data to the API.

**Preconditions**:
- User is logged in
- Mock API endpoint for challenge creation

**Test Steps**:
1. Render the challenge creation form
2. Fill in valid challenge data
3. Submit the form
4. Verify API call and response handling

**Expected Results**:
1. Form data is correctly formatted for API
2. Success message is displayed on successful submission
3. User is redirected to the challenge page

**Test Data**:
- Valid challenge data

---

#### TC-F-012: Project Creation Form Submission

**Description**: Verify that the project creation form correctly submits data to the API.

**Preconditions**:
- User is logged in
- User has at least one challenge
- Mock API endpoint for project creation

**Test Steps**:
1. Render the project creation form
2. Fill in valid project data
3. Submit the form
4. Verify API call and response handling

**Expected Results**:
1. Form data is correctly formatted for API
2. Success message is displayed on successful submission
3. Project is added to the challenge

**Test Data**:
- Valid project data

---

## Responsive Design Tests

#### TC-F-013: Mobile Responsiveness - Dashboard

**Description**: Verify that the dashboard is properly responsive on mobile devices.

**Preconditions**:
- User is logged in

**Test Steps**:
1. Set viewport to mobile size (375x667)
2. Navigate to dashboard
3. Verify layout and component rendering

**Expected Results**:
1. All dashboard components are visible and properly sized
2. Navigation is accessible via mobile menu
3. Charts and statistics are readable

**Test Data**:
- N/A

---

#### TC-F-014: Tablet Responsiveness - Challenge Detail

**Description**: Verify that the challenge detail page is properly responsive on tablet devices.

**Preconditions**:
- User is logged in
- User has at least one challenge

**Test Steps**:
1. Set viewport to tablet size (768x1024)
2. Navigate to challenge detail page
3. Verify layout and component rendering

**Expected Results**:
1. Challenge details are properly displayed
2. Project list is properly formatted
3. All actions are accessible

**Test Data**:
- Existing challenge with projects