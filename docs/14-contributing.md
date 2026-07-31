# 🤝 Contributing Guide

> Guidelines for contributing to Smart Infrastructure Operations Dashboard (SIOD).

![Project](https://img.shields.io/badge/Project-SIOD-blue)
![Open Source](https://img.shields.io/badge/Open%20Source-Community-green)
![Contribution](https://img.shields.io/badge/Contribution-Welcome-purple)
![Status](https://img.shields.io/badge/Document-Contributing-orange)

---

# 📖 Overview

SIOD is designed as an open-source project.

Contributions are welcome from developers, infrastructure engineers, DevOps practitioners, researchers, and students.

Everyone can contribute through:

- Code.
- Documentation.
- Testing.
- Plugin development.
- Architecture discussion.
- Bug reports.

---

# 🎯 Contribution Goals

The contribution process aims to maintain:

- Code quality.
- Clear communication.
- Stable development.
- Collaborative environment.

---

# 🚀 Getting Started

Before contributing:

1. Read the documentation.
2. Understand project architecture.
3. Setup development environment.
4. Check existing issues.

---

# 📂 Development Structure

Main repository structure:

```
SIOD/

├── backend/

├── frontend/

├── agents/

├── plugins/

├── deployment/

├── docs/

└── tests/
```

---

# 🔀 Contribution Workflow

Standard workflow:

```
Fork Repository

        ↓

Create Branch

        ↓

Develop Feature

        ↓

Run Tests

        ↓

Create Pull Request

        ↓

Code Review

        ↓

Merge
```

---

# 🌱 Branch Naming

Recommended format:

```
feature/

bugfix/

documentation/

plugin/
```

Example:

```
feature/docker-plugin
```

---

# 📝 Commit Convention

Recommended:

```
type: description
```

Examples:

```
feat: add docker collector

fix: resolve api timeout

docs: update architecture guide

test: add api test
```

---

# 🧩 Plugin Contribution

Developers can contribute new plugins.

Examples:

```
plugins/

├── mikrotik/

├── proxmox/

├── aws/

├── mysql/
```

Requirements:

- Documentation.
- Configuration example.
- Test coverage.
- Security review.

---

# 🧪 Testing Requirement

Before submitting changes:

Run:

```
pytest
```

Verify:

- Application starts.
- API works.
- Existing features remain functional.

---

# 📚 Documentation Contribution

Documentation improvements are highly appreciated.

Examples:

- Installation guides.
- Architecture explanation.
- Tutorials.
- Troubleshooting guides.

---

# 🐛 Bug Reports

Bug reports should include:

Information:

```
Environment:

OS:

Version:

Steps to reproduce:

Expected behavior:

Actual behavior:
```

---

# 💡 Feature Requests

Feature requests should explain:

- Problem.
- Proposed solution.
- Expected benefit.
- Possible implementation.

---

# 🔐 Security Reports

Do not publicly report security vulnerabilities.

Security issues should be privately reported to maintain system safety.

---

# 📜 Code Style

Guidelines:

- Write readable code.
- Add comments where needed.
- Follow existing structure.
- Avoid unnecessary complexity.

---

# 🤖 AI Development Guidelines

For AI-related contributions:

Consider:

- Data privacy.
- Model limitations.
- Explainability.
- Human approval for automation.

---

# 🌍 Community Principles

Contributors should:

- Respect others.
- Share knowledge.
- Provide constructive feedback.
- Maintain professional communication.

---

# Conclusion

By contributing to SIOD, developers help build an open and extensible Infrastructure Operations Platform.

Together, SIOD can evolve from a monitoring project into a complete AI-assisted infrastructure management ecosystem.
