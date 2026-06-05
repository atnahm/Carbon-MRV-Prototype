# Contributing to Carbon MRV Platform

First off, thank you for considering contributing to the Carbon MRV Platform! It's people like you that make open-source platforms great.

## Code of Conduct

By participating in this project, you are expected to uphold standard professional conduct. Please be respectful to all contributors.

## How Can I Contribute?

### Reporting Bugs
If you find a bug in the source code or a mistake in the documentation, you can help us by submitting an issue to our GitHub Repository. Even better, you can submit a Pull Request with a fix.

### Suggesting Enhancements
If you have ideas to improve the platform, please submit an issue explaining the enhancement and its use cases. We welcome discussions on how to make the ML models more accurate or the architecture more scalable.

### Pull Requests
1. Fork the repository and create your branch from `main`.
2. If you've added code that should be tested, add tests to `backend/tests/` or frontend equivalents.
3. If you've changed APIs, update the documentation.
4. Ensure the test suite passes (`pytest backend/tests/`).
5. Ensure your code lints (`cd frontend && npm run lint`).
6. Issue that pull request!

## Local Setup
Please refer to the `README.md` for instructions on setting up the project locally using Docker Compose.

## Machine Learning Contributions
We are particularly interested in contributions that improve the `backend/ml_model.py`. If you introduce new features to the prediction model, ensure they support `partial_fit` for online learning so the platform can continuously improve from ground-truth data.
