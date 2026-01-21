# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [0.1.0] - 2026-01-21

### Added
- **MCP Server (skill-creator-mcp)**: Initial release
  - `init_skill` tool - Initialize new Agent-Skill projects
  - `validate_skill` tool - Validate skill structure and content
  - `analyze_skill` tool - Analyze code quality and complexity
  - `refactor_skill` tool - Generate refactoring suggestions
  - `package_skill` tool - Package skills for distribution
  - 3 MCP Resources: templates, best practices, validation rules
  - 3 MCP Prompts: create-skill, validate-skill, refactor-skill
  - Support for STDIO and HTTP/SSE transport

- **Agent-Skill (skill-creator)**: Initial release
  - Progressive disclosure three-layer architecture
  - SKILL.md entry point (94 lines)
  - Comprehensive documentation in references/

- **Testing**: 262 tests with 96% coverage

- **Documentation**: MCP Integration, Best Practices, Validation, Architecture Audit

- **DevTools**: Docker, CI/CD, pre-commit hooks, ruff, mypy, bandit

### Performance
- All tool operations < 1 second

### Security
- No high-severity vulnerabilities

---

## [Unreleased]

### Planned
- MCP Inspector guide
- Performance benchmarks
