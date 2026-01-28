Skill Creator MCP Server Documentation
========================================

Welcome to the documentation for Skill Creator MCP Server.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

   api/index

Overview
========

Skill Creator MCP Server is a Model Context Protocol (MCP) server that provides tools for developing, validating, and optimizing Agent-Skills.

Features
--------

**Skill Lifecycle (4)**:

* **init_skill** - Initialize new Agent-Skill projects
* **validate_skill** - Validate skill structure and content
* **analyze_skill** - Analyze code quality and complexity
* **refactor_skill** - Generate refactoring suggestions

**Packaging (2)**:

* **package_skill** - Package skills for distribution
* **package_agent_skill** - Standard Agent-Skill packaging

**Requirement Collection (7)**:

* **create_requirement_session** - Create requirement collection session
* **get_requirement_session** - Get session state
* **update_requirement_answer** - Update answer
* **get_static_question** - Get static question
* **generate_dynamic_question** - Generate dynamic question
* **validate_answer_format** - Validate answer format
* **check_requirement_completeness** - Check completeness

**Batch Operations (2)**:

* **batch_validate_skills** - Batch validate multiple skills
* **batch_analyze_skills** - Batch analyze multiple skills

**Health Check (3)**:

* **health_check** - Complete health check
* **quick_status** - Quick status summary
* **is_healthy** - Quick health check

Installation
------------

.. code-block:: bash

   pip install skill-creator-mcp

Quick Start
-----------

.. code-block:: python

   from skill_creator_mcp import mcp

   # Use with Claude Code
   # Configure in ~/.config/Claude/claude_desktop_config.json

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
