
# Contributing to Path2Markdown

First off, thank you for considering contributing to Path2Markdown! We appreciate any help—whether it’s fixing a bug, adding a new feature, improving the documentation, or making the tool cross-platform.

Below you’ll find guidelines and best practices to make the contribution process smooth and effective.

## Table of Contents

- [Getting Started](#getting-started)
- [How to Contribute](#how-to-contribute)
- [Development Workflow](#development-workflow)
- [Coding Standards](#coding-standards)
- [Testing](#testing)
- [Documentation](#documentation)
- [Versioning and Releases](#versioning-and-releases)
- [Communication](#communication)

## Getting Started

1. **Fork the Repository**:  
   Click the "Fork" button on the top-right corner of the [main repository](https://github.com/YourUserName/Path2Markdown) page to create your own copy.

2. **Clone Your Fork**:  
   ```bash
   git clone https://github.com/elapen/Path2Markdown.git
   ```
   
3. **Set Up Your Environment**:  
   Ensure you have Python installed. We use `PySide6` and other dependencies as listed in `requirements.txt`.  
   ```bash
   cd Path2Markdown
   pip install -r requirements.txt
   ```

4. **Create a Branch**:  
   For each contribution (feature, fix, etc.), create a new branch.  
   ```bash
   git checkout -b feature/my-new-feature
   ```

## How to Contribute

- **Fix Bugs**: Check the [Issues](https://github.com/YourUserName/Path2Markdown/issues) tab for open bug reports. If you find a bug on your own, feel free to open a new issue before submitting a fix.
- **Add Features**: Have an idea for a new feature or improvement? Open an issue to discuss it. Once agreed upon, implement it in a feature branch and submit a PR.
- **Improve Documentation**: Clear, concise documentation helps everyone. If you notice outdated or missing info in the README, developer docs, or comments, please update it.
- **Platform Support**: We welcome contributions to support macOS, Linux, or other platforms. Feel free to open discussions and PRs related to this topic.
- **Refactoring and Cleanup**: Code quality matters. Feel free to submit PRs that improve code structure, readability, or performance.

## Development Workflow

1. **Sync with Upstream**:  
   Keep your fork in sync to avoid merge conflicts:  
   ```bash
   git fetch upstream
   git merge upstream/main
   ```

2. **Write Code & Tests**:  
   Implement your changes. Add or update tests where necessary (see [Testing](#testing)).

3. **Commit Guidelines**:  
   Commit messages should be clear and descriptive. For example:  
   - `fix: handle empty folder case in markdown generation`
   - `feat: add macOS support`
   - `docs: update README with installation steps`

4. **Push & Open a PR**:  
   Once done, push your branch and create a Pull Request (PR) to the `main` branch of the original repo.  
   ```bash
   git push origin feature/my-new-feature
   ```
   Then visit your fork on GitHub and click "Compare & pull request."

5. **Review Process**:  
   Maintainers and other contributors will review your PR. Please be responsive to feedback and make changes as requested.

## Coding Standards

- **Style**: Follow [PEP 8](https://peps.python.org/pep-0008/) Python style guidelines.
- **Naming**: Choose clear and descriptive variable/function/class names.
- **Structure**: Keep functions and classes small and focused.  
- **Comments**: Add docstrings and comments where clarity is needed.

We may use tools like `black` and `isort` for code formatting and imports ordering. Running these before committing helps maintain consistency.

## Testing

Tests help ensure we don’t break existing functionality when adding features or fixing bugs. We strongly encourage:

- **Automated Tests**: Use `pytest` or similar frameworks.
- **Test Coverage**: Increase coverage over time. Add tests for new code paths.
- **Run Tests Locally**: Before opening a PR, run tests to ensure everything passes:
  ```bash
  pytest
  ```

## Documentation

- **README**: If you add a new feature, update the README accordingly.
- **In-Code Docs**: Provide docstrings for new functions, classes, and modules.
- **CHANGELOG**: If you’re adding a significant feature or making a breaking change, update the `CHANGELOG.md`.

## Versioning and Releases

We follow semantic versioning (major.minor.patch). Maintainers will handle the release process, but significant contributions should be noted in the `CHANGELOG.md`.

## Communication

- **Issues**: For bugs, features, or questions.
- **Discussions**: For long-form discussions, feedback, or brainstorming.
- **Pull Requests**: For code contributions.

We aim to build a welcoming, inclusive community. Please be respectful and follow the [Code of Conduct](CODE_OF_CONDUCT.md) if one is provided.

---

Thank you again for your interest in improving Path2Markdown! Your contributions make the project better for everyone.
```