# Contributing to 100 Days Challenge Tracker

Thank you for considering contributing to the 100 Days Challenge Tracker! This document provides guidelines and instructions for contributing to the project.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [How Can I Contribute?](#how-can-i-contribute)
- [Development Setup](#development-setup)
- [Pull Request Process](#pull-request-process)
- [Coding Standards](#coding-standards)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)
- [Community](#community)

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code. Please report unacceptable behavior to [conduct@100dayschallenge.com](mailto:conduct@100dayschallenge.com).

## How Can I Contribute?

### Reporting Bugs

- **Ensure the bug was not already reported** by searching on GitHub under [Issues](https://github.com/yourusername/100dayschallenge/issues).
- If you're unable to find an open issue addressing the problem, [open a new one](https://github.com/yourusername/100dayschallenge/issues/new). Include a **title and clear description**, as much relevant information as possible, and a **code sample** or an **executable test case** demonstrating the expected behavior that is not occurring.

### Suggesting Enhancements

- **Check if the enhancement has already been suggested** by searching on GitHub under [Issues](https://github.com/yourusername/100dayschallenge/issues).
- If it hasn't, [create a new issue](https://github.com/yourusername/100dayschallenge/issues/new) with a clear title and description of the suggested enhancement.
- Include any relevant details about how the enhancement would work and why it would be beneficial.

### Your First Code Contribution

- Look for issues labeled `good first issue` or `help wanted` to find good starting points.
- Fork the repository and create a branch for your changes.
- Make your changes and submit a pull request.

## Development Setup

### Prerequisites

- Node.js 16+
- npm or yarn
- MongoDB (local or Atlas)

### Local Development Environment

1. Fork the repository
2. Clone your fork:
   ```bash
   git clone https://github.com/yourusername/100dayschallenge.git
   cd 100dayschallenge
   ```

3. Install dependencies:
   ```bash
   npm install
   ```

4. Set up environment variables:
   ```bash
   cp backend/.env.example backend/.env
   cp frontend/.env.development frontend/.env
   ```

5. Start the development server:
   ```bash
   npm run dev
   ```

6. Visit `http://localhost:3000` to see the application running.

## Pull Request Process

1. **Create a branch** for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and commit them with clear, descriptive commit messages:
   ```bash
   git commit -m "Add feature: description of changes"
   ```

3. **Run tests** to ensure your changes don't break existing functionality:
   ```bash
   npm test
   ```

4. **Update documentation** if necessary.

5. **Push your branch** to your fork:
   ```bash
   git push origin feature/your-feature-name
   ```

6. **Submit a pull request** to the main repository.

7. **Address review comments** if any are provided.

## Coding Standards

### General Guidelines

- Follow the existing code style and patterns.
- Write clear, readable, and maintainable code.
- Keep functions small and focused on a single task.
- Use meaningful variable and function names.

### Frontend (React/TypeScript)

- Follow the [React Hooks guidelines](https://reactjs.org/docs/hooks-rules.html).
- Use functional components with hooks instead of class components.
- Use TypeScript interfaces for props and state.
- Follow the component structure in the project.

### Backend (TypeScript/Netlify Functions)

- Follow RESTful API design principles.
- Use TypeScript for type safety.
- Handle errors properly and provide meaningful error messages.
- Follow the existing folder structure.

## Testing Guidelines

### Writing Tests

- Write tests for all new features and bug fixes.
- Aim for high test coverage, especially for critical paths.
- Follow the existing test patterns in the project.

### Running Tests

```bash
# Run all tests
npm test

# Run frontend tests
npm run test:frontend

# Run backend tests
npm run test:backend

# Run integration tests
npm run test:integration
```

## Documentation

- Update documentation for any changes to features, APIs, or configuration.
- Document new features thoroughly.
- Keep the README and other documentation up to date.

## Community

- Join our [Discord server](https://discord.gg/100dayschallenge) for discussions.
- Participate in [GitHub Discussions](https://github.com/yourusername/100dayschallenge/discussions).
- Follow our [Twitter account](https://twitter.com/100dayschallenge) for updates.

---

Thank you for contributing to the 100 Days Challenge Tracker! Your efforts help make this project better for everyone.