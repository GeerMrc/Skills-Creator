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

### Changed
- **Branch Strategy**: Updated to reflect simplified main + feature/* structure
  - Removed outdated `develop` branch references
  - Updated audit report Git workflow score from 70/100 to 95/100

### Fixed
- **Documentation**: Fixed broken reference in `best-practices.md`
  - Replaced invalid `file-processing.md` with actual `validation.md`
- **Code Quality**: Fixed Ruff linting issues
  - Removed unused imports (`validate_skill_name`, `validate_template_type`) from server.py
  - Fixed 20 long lines (E501) across multiple files
  - All code checks now passing (ruff, mypy, pytest)
- **Type Hints**: Improved `# type: ignore` usage with explanatory comments
  - Added comments explaining why each type ignore is necessary
  - Verified all 6 instances are legitimate (not 120 as originally reported)
  - Issues caused by FastMCP API limitations, Literal type inference, and tarfile stubs

### Improved
- **Project Organization**: Comprehensive cleanup and optimization
  - Added core project documentation (ARCHITECTURE_AUDIT_REPORT_v2.md, CLAUDE.md, ISSUES.md, ROADMAP.md)
  - Archived old audit report versions to `.claude/archive/`
  - Moved outdated `architecture-audit-report.md` from references/ to archive/
  - Organized plan files with proper naming conventions (feat-*, fix-*, audit-*, etc.)
  - Created archive index (README.md) with 10+ archived plans

- **Test Coverage**: Increased from 94% to 98%
  - Added `tests/test_main.py` for `__main__.py` and `http.py` entry points
  - Added `tests/test_logging_config.py` for logging configuration
  - Total: 297 tests passing

- **Documentation**: Added Phase 1 Audit Reports
  - `report-mcp-server-development.md` - MCP Server development summary
  - `report-agent-skill-development.md` - Agent-Skill development summary
  - `report-audit-2026-01-22.md` - Complete audit work report

- **SKILL.md Updates**: Added missing references
  - Added `validation-guide.md` link (等级划分、常见问题、自动化验证示例)
  - Added `http://skills/schema/templates` resource (所有可用模板列表)

- **Cross-Validation**: Comprehensive verification completed
  - Verified all MCP tools, resources, and prompts are documented
  - Confirmed SKILL.md matches server.py implementation
  - Audited technical debt and found discrepancies (6 type ignores, not 120; 0 bare excepts)
  - Validated all document reference links

### Verified
- **Test Coverage**: 98% (297 tests passing)
- **Cross-references**: All documentation links validated
- **Code Quality**: All quality checks passing (ruff, mypy, pytest)
- **MCP Consistency**: All tools (5), resources (4), and prompts (3) documented

### Documented Decisions
- **References File Size**: Keeping current sizes (content quality > size limits)
  - mcp-integration.md: 281 lines ✅
  - validation.md: 322 lines (11% over, acceptable)
  - validation-guide.md: 332 lines (11% over, acceptable)
  - best-practices.md: 405 lines (35% over, but content is excellent)

### Planned
- MCP Inspector guide
- Performance benchmarks
