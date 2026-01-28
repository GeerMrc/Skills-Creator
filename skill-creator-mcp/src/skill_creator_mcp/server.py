"""Skill Creator MCP Server.

这是一个基于 FastMCP SDK 开发的 MCP Server，用于创建、验证、
分析和重构 Agent-Skills。
"""

from typing import Any

from fastmcp import Context, FastMCP

from .prompts import (
    get_create_skill_prompt,
    get_refactor_skill_prompt,
    get_validate_skill_prompt,
)
from .resources import (
    get_best_practices,
    get_template_content,
    get_validation_rules,
    list_templates,
)

# 新工具模块导入（Phase 2.2 重构）
from .tools.batch_tools import (
    batch_analyze_skills_tool as batch_analyze_skills_tool_impl,
)
from .tools.batch_tools import (
    batch_validate_skills_tool as batch_validate_skills_tool_impl,
)
from .tools.health_check import (
    get_quick_status,
    health_check,
    is_healthy,
)
from .tools.package_tools import (
    package_agent_skill as package_agent_skill_impl,
)
from .tools.package_tools import (
    package_skill as package_skill_impl,
)
from .tools.requirement_question_tools import (
    generate_dynamic_question,
    get_static_question,
)

# 新的原子化需求收集工具（架构重构）
from .tools.requirement_session_tools import (
    create_requirement_session,
    get_requirement_session,
    update_requirement_answer,
)
from .tools.requirement_validation_tools import (
    check_requirement_completeness,
    validate_answer_format,
)
from .tools.skill_tools import (
    analyze_skill,
    init_skill,
    refactor_skill,
    validate_skill,
)
from .tools.test_tools import (
    check_client_capabilities as check_client_capabilities_impl,
)
from .tools.test_tools import (
    test_conversation_loop as test_conversation_loop_impl,
)
from .tools.test_tools import (
    test_llm_sampling as test_llm_sampling_impl,
)
from .tools.test_tools import (
    test_requirement_completeness as test_requirement_completeness_impl,
)
from .tools.test_tools import (
    test_user_elicitation as test_user_elicitation_impl,
)

# 创建 MCP Server
mcp = FastMCP(
    name="skill-creator",
    instructions="""
    Skill Creator MCP Server - Agent-Skills 开发工具

    这个服务器提供创建、验证、分析、重构和打包 Agent-Skills 的工具。

    ## 可用工具

    ### init_skill
    初始化新的 Agent-Skill。

    参数：
    - name (str): 技能名称（小写字母、数字、连字符，1-64字符）
    - template (str): 模板类型（minimal/tool-based/workflow-based/analyzer-based）
    - output_dir (str): 输出目录路径
    - with_scripts (bool): 是否包含示例脚本
    - with_examples (bool): 是否包含使用示例

    ### validate_skill
    验证 Agent-Skill 的结构和内容。

    参数：
    - skill_path (str): 技能目录路径
    - check_structure (bool): 是否检查目录结构（默认 True）
    - check_content (bool): 是否检查内容格式（默认 True）

    ### analyze_skill
    分析 Agent-Skill 的代码质量、复杂度和结构。

    参数：
    - skill_path (str): 技能目录路径
    - analyze_structure (bool): 是否分析代码结构（默认 True）
    - analyze_complexity (bool): 是否分析代码复杂度（默认 True）
    - analyze_quality (bool): 是否分析代码质量（默认 True）

    ### refactor_skill
    生成 Agent-Skill 的重构建议。

    参数：
    - skill_path (str): 技能目录路径
    - focus (list[str]): 重点关注领域（可选，如 structure、documentation、testing）
    - analyze_structure (bool): 是否分析代码结构（默认 True）
    - analyze_complexity (bool): 是否分析代码复杂度（默认 True）
    - analyze_quality (bool): 是否分析代码质量（默认 True）

    ### package_skill
    打包 Agent-Skill 为分发格式。

    参数：
    - skill_path (str): 技能目录路径
    - output_dir (str): 输出目录路径（默认：当前目录）
    - format (str): 打包格式（zip/tar.gz/tar.bz2，默认：zip）
    - include_tests (bool): 是否包含测试文件（默认：True）
    - validate_before_package (bool): 打包前是否验证（默认：True）

    ### package_agent_skill
    打包 Agent-Skill 为标准分发格式（推荐使用）。

    与 package_skill 的区别：
    - 使用更严格的排除模式
    - 支持版本号参数，生成标准化包名
    - 默认不包含测试文件
    - 确保符合 Agent-Skill 规范

    参数：
    - skill_path (str): Agent-Skill 目录路径
    - output_dir (str): 输出目录路径（默认：当前目录）
    - version (str): 版本号（可选，格式如 "0.3.1"）
    - format (str): 打包格式（zip/tar.gz/tar.bz2，默认：zip）
    - include_tests (bool): 是否包含测试文件（默认：False）
    - validate_before_package (bool): 打包前是否验证（默认：True）
    """
)

# ==================== 注册工具模块 ====================
# Phase 2.2 重构：从独立工具模块注册 MCP 工具


# 技能工具（skill_tools.py）
# 直接使用 @mcp.tool() 装饰器注册工具
mcp.add_tool(init_skill)
mcp.add_tool(validate_skill)
mcp.add_tool(analyze_skill)
mcp.add_tool(refactor_skill)


# 打包工具（package_tools.py）
# 函数签名：async def func(ctx, mcp, ...) -> dict
@mcp.tool()
async def package_skill(
    ctx: Context,
    skill_path: str,
    output_dir: str | None = None,
    format: str = "zip",
    include_tests: bool = True,
    validate_before_package: bool = True,
) -> dict[str, Any]:
    """
    打包 Agent-Skill 为分发格式.

    创建包含技能文件的压缩包，支持 zip、tar.gz 和 tar.bz2 格式。

    Args:
        ctx: MCP 上下文
        skill_path: 技能目录路径
        output_dir: 输出目录路径（可选，优先级：参数 > 环境变量 SKILL_CREATOR_OUTPUT_DIR > 默认值）
        format: 打包格式（zip/tar.gz/tar.bz2）
        include_tests: 是否包含测试文件
        validate_before_package: 打包前是否验证

    Returns:
        包含打包结果的字典
    """
    return await package_skill_impl(ctx, mcp, skill_path, output_dir, format, include_tests, validate_before_package)


@mcp.tool()
async def package_agent_skill(
    ctx: Context,
    skill_path: str,
    output_dir: str | None = None,
    version: str | None = None,
    format: str = "zip",
    include_tests: bool = False,
    validate_before_package: bool = True,
) -> dict[str, Any]:
    """
    打包 Agent-Skill 为标准分发格式.

    这是专门用于打包标准 Agent-Skill 的函数。
    与 package_skill 的区别：
    - 使用更严格的排除模式
    - 支持版本号参数，生成标准化包名
    - 默认不包含测试文件
    - 确保符合 Agent-Skill 规范

    Args:
        ctx: MCP 上下文
        skill_path: Agent-Skill 目录路径
        output_dir: 输出目录路径（可选，优先级：参数 > 环境变量 SKILL_CREATOR_OUTPUT_DIR > 默认值）
        version: 版本号（可选，格式如 "0.3.1"）
        format: 打包格式（zip/tar.gz/tar.bz2）
        include_tests: 是否包含测试文件（默认 False）
        validate_before_package: 打包前是否验证

    Returns:
        包含打包结果的字典
    """
    return await package_agent_skill_impl(ctx, mcp, skill_path, output_dir, version, format, include_tests, validate_before_package)


# ==================== 需求收集原子工具 ====================
# 架构重构：将 collect_requirements 拆分为原子操作工具
# 符合 ADR 001: MCP Server 只提供原子操作，不包含工作流逻辑
# 工作流编排由 Agent-Skill 负责


@mcp.tool()
async def create_requirement_session_tool(
    ctx: Context,
    mode: str = "basic",
    total_steps: int | None = None,
) -> dict[str, Any]:
    """创建新的需求收集会话.

    这是一个原子操作工具，只负责创建会话状态。
    工作流编排由 Agent-Skill 负责。

    Args:
        ctx: MCP 上下文
        mode: 收集模式（basic/complete/brainstorm/progressive）
        total_steps: 总步骤数（可选，默认根据模式自动计算）

    Returns:
        包含会话信息的字典
    """
    return await create_requirement_session(ctx, mode, total_steps)


@mcp.tool()
async def get_requirement_session_tool(
    ctx: Context,
    session_id: str,
) -> dict[str, Any]:
    """获取需求收集会话状态.

    这是一个原子操作工具，只负责读取会话状态。

    Args:
        ctx: MCP 上下文
        session_id: 会话ID

    Returns:
        包含会话状态的字典
    """
    return await get_requirement_session(ctx, session_id)


@mcp.tool()
async def update_requirement_answer_tool(
    ctx: Context,
    session_id: str,
    question_key: str,
    answer: str,
) -> dict[str, Any]:
    """更新需求收集会话中的答案.

    这是一个原子操作工具，只负责更新单个答案。
    不包含验证逻辑，验证由专门的工具处理。

    Args:
        ctx: MCP 上下文
        session_id: 会话ID
        question_key: 问题键（如 skill_name, skill_function）
        answer: 用户答案

    Returns:
        包含更新结果的字典
    """
    return await update_requirement_answer(ctx, session_id, question_key, answer)


@mcp.tool()
async def get_static_question_tool(
    ctx: Context,
    mode: str,
    step_index: int,
) -> dict[str, Any]:
    """获取静态问题（用于 basic/complete 模式）.

    这是一个原子操作工具，只负责获取预定义的问题。
    不包含循环逻辑，循环由 Agent-Skill 编排。

    Args:
        ctx: MCP 上下文
        mode: 收集模式（basic/complete）
        step_index: 步骤索引（从0开始）

    Returns:
        包含问题信息的字典
    """
    return await get_static_question(ctx, mode, step_index)


@mcp.tool()
async def generate_dynamic_question_tool(
    ctx: Context,
    mode: str,
    answers: dict[str, str],
    conversation_history: list[dict] | None = None,
    prompt_template: str | None = None,
) -> dict[str, Any]:
    """生成动态问题（用于 brainstorm/progressive 模式）.

    这是一个原子操作工具，使用 LLM 生成下一个问题。
    不包含循环逻辑，循环由 Agent-Skill 编排。

    Args:
        ctx: MCP 上下文
        mode: 收集模式（brainstorm/progressive）
        answers: 已收集的答案
        conversation_history: 对话历史（用于 brainstorm 模式）
        prompt_template: 自定义Prompt模板（可选，用于特殊场景）。
                        Prompt模板应由Agent-Skill提供，符合ADR 001架构原则。

    Returns:
        包含生成问题的字典
    """
    return await generate_dynamic_question(ctx, mode, answers, conversation_history, prompt_template)


@mcp.tool()
async def validate_answer_format_tool(
    ctx: Context,
    answer: str,
    validation: dict[str, Any],
) -> dict[str, Any]:
    """验证答案格式.

    这是一个原子操作工具，只负责验证单个答案。
    不包含重试逻辑，重试由 Agent-Skill 编排。

    Args:
        ctx: MCP 上下文
        answer: 用户输入的答案
        validation: 验证规则字典

    Returns:
        包含验证结果的字典
    """
    return await validate_answer_format(ctx, answer, validation)


@mcp.tool()
async def check_requirement_completeness_tool(
    ctx: Context,
    answers: dict[str, str],
    prompt_template: str | None = None,
) -> dict[str, Any]:
    """检查需求完整性（使用 LLM）.

    这是一个原子操作工具，只负责完整性检查。
    不包含补充收集逻辑，补充由 Agent-Skill 编排。

    Args:
        ctx: MCP 上下文
        answers: 已收集的答案
        prompt_template: 自定义Prompt模板（可选，用于特殊场景）。
                        Prompt模板应由Agent-Skill提供，符合ADR 001架构原则。

    Returns:
        包含完整性检查结果的字典
    """
    return await check_requirement_completeness(ctx, answers, prompt_template)


# 测试工具（test_tools.py）
@mcp.tool()
async def check_client_capabilities(ctx: Context) -> dict[str, Any]:
    """检测 MCP 客户端的能力支持情况.

    检测客户端是否支持高级 MCP 功能，如 sampling 和 elicitation。

    Returns:
        包含客户端能力检测结果的字典
    """
    return await check_client_capabilities_impl(ctx, mcp)


@mcp.tool()
async def test_llm_sampling(ctx: Context, prompt: str) -> dict[str, Any]:
    """测试 LLM Sampling 能力.

    验证 MCP Server 可以通过 ctx.sample() 调用客户端 LLM。

    Args:
        ctx: MCP 上下文
        prompt: 要发送给 LLM 的提示文本

    Returns:
        包含测试结果的字典，包括 LLM 响应文本和历史记录
    """
    return await test_llm_sampling_impl(ctx, mcp, prompt)


@mcp.tool()
async def test_user_elicitation(
    ctx: Context, prompt: str = "请提供技能名称（小写字母、数字、连字符）"
) -> dict[str, Any]:
    """测试用户征询 (User Elicitation) 能力.

    验证可以通过 ctx.elicit() 请求用户输入结构化数据。

    Args:
        ctx: MCP 上下文
        prompt: 向用户显示的提示文本

    Returns:
        包含测试结果的字典
    """
    return await test_user_elicitation_impl(ctx, mcp, prompt)


@mcp.tool()
async def test_conversation_loop(ctx: Context, user_input: str) -> dict[str, Any]:
    """测试对话循环和状态管理能力.

    验证可以在对话循环中使用 session state 保存历史，
    并且 LLM 可以利用对话历史生成更连贯的响应。

    Args:
        ctx: MCP 上下文
        user_input: 用户输入的文本

    Returns:
        包含测试结果的字典，包括 LLM 响应和会话状态
    """
    return await test_conversation_loop_impl(ctx, mcp, user_input)


@mcp.tool()
async def test_requirement_completeness(ctx: Context, requirement: str) -> dict[str, Any]:
    """测试需求完整性判断能力.

    验证 LLM 能够判断需求是否完整，并识别缺失的关键信息。

    Args:
        ctx: MCP 上下文
        requirement: 技能创建需求描述

    Returns:
        包含测试结果的字典，包括完整性分析和缺失信息列表
    """
    return await test_requirement_completeness_impl(ctx, mcp, requirement)


# 批量操作工具（batch_tools.py）
@mcp.tool()
async def batch_validate_skills_tool(
    ctx: Context,
    skill_paths: list[str],
    check_structure: bool = True,
    check_content: bool = True,
    concurrent_limit: int = 5,
) -> dict[str, Any]:
    """批量验证多个Agent-Skill.

    并发验证多个技能的结构和内容，提高验证效率。

    Args:
        ctx: MCP 上下文
        skill_paths: 技能目录路径列表
        check_structure: 是否检查目录结构（默认 True）
        check_content: 是否检查内容格式（默认 True）
        concurrent_limit: 并发限制（默认 5）

    Returns:
        包含批量验证结果的字典，包括每个技能的验证结果和汇总信息
    """
    return await batch_validate_skills_tool_impl(ctx, mcp, skill_paths, check_structure, check_content, concurrent_limit)


@mcp.tool()
async def batch_analyze_skills_tool(
    ctx: Context,
    skill_paths: list[str],
    analyze_structure: bool = True,
    analyze_complexity: bool = True,
    analyze_quality: bool = True,
    concurrent_limit: int = 5,
) -> dict[str, Any]:
    """批量分析多个Agent-Skill.

    并发分析多个技能的代码质量、复杂度和结构。

    Args:
        ctx: MCP 上下文
        skill_paths: 技能目录路径列表
        analyze_structure: 是否分析代码结构（默认 True）
        analyze_complexity: 是否分析代码复杂度（默认 True）
        analyze_quality: 是否分析代码质量（默认 True）
        concurrent_limit: 并发限制（默认 5）

    Returns:
        包含批量分析结果的字典，包括每个技能的分析结果和汇总信息
    """
    return await batch_analyze_skills_tool_impl(ctx, mcp, skill_paths, analyze_structure, analyze_complexity, analyze_quality, concurrent_limit)


# ==================== 健康检查工具 ====================


@mcp.tool()
async def health_check_tool(ctx: Context) -> dict[str, Any]:
    """执行完整健康检查.

    返回系统健康状态、系统指标、缓存指标和性能指标。

    Args:
        ctx: MCP 上下文

    Returns:
        包含完整健康检查结果的字典
    """
    try:
        result = health_check()
        return {
            "success": True,
            **result.model_dump(),
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"健康检查出错: {e}",
            "error_type": "internal_error",
        }


@mcp.tool()
async def quick_status_tool(ctx: Context) -> dict[str, Any]:
    """获取快速状态摘要.

    返回简化的系统状态信息字符串。

    Args:
        ctx: MCP 上下文

    Returns:
        包含状态摘要字符串的字典
    """
    try:
        status = get_quick_status()
        return {
            "success": True,
            "status": status,
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"获取状态出错: {e}",
            "error_type": "internal_error",
        }


@mcp.tool()
async def is_healthy_tool(ctx: Context) -> dict[str, Any]:
    """快速检查系统是否健康.

    返回布尔值表示系统健康状态。

    Args:
        ctx: MCP 上下文

    Returns:
        包含健康状态布尔值的字典
    """
    try:
        healthy = is_healthy()
        return {
            "success": True,
            "healthy": healthy,
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"健康检查出错: {e}",
            "error_type": "internal_error",
        }


# ==================== MCP Resources ====================


@mcp.resource("http://skills/schema/templates")
def list_templates_resource() -> str:
    """列出所有可用的技能模板."""
    templates = list_templates()
    result = "# 技能模板列表\n\n"
    for t in templates:
        result += f"## {t['type']}\n"
        result += f"{t['description']}\n\n"
    return result


@mcp.resource("http://skills/schema/templates/{type}")
def get_template_resource(type: str) -> str:
    """获取指定类型的技能模板内容."""
    from .resources.templates import TemplateType

    # 验证模板类型
    valid_types = ["minimal", "tool-based", "workflow-based", "analyzer-based"]
    if type not in valid_types:
        return f"# 错误\n\n未知的模板类型: {type}\n\n有效类型: {', '.join(valid_types)}"

    return get_template_content(TemplateType(type))  # type: ignore


@mcp.resource("http://skills/schema/best-practices")
def best_practices_resource() -> str:
    """获取 Agent-Skills 开发最佳实践."""
    return get_best_practices()


@mcp.resource("http://skills/schema/validation-rules")
def validation_rules_resource() -> str:
    """获取 Agent-Skills 验证规则."""
    return get_validation_rules()


# ==================== MCP Prompts ====================


@mcp.prompt("create-skill")
def create_skill_prompt(
    name: str,
    template: str = "minimal",
) -> str:
    """创建新技能的 Prompt 模板.

    Args:
        name: 技能名称
        template: 模板类型（默认：minimal）

    Returns:
        Prompt 模板内容
    """
    return get_create_skill_prompt(name, template)


@mcp.prompt("validate-skill")
def validate_skill_prompt(
    skill_path: str,
    template: str | None = None,
) -> str:
    """验证技能的 Prompt 模板.

    Args:
        skill_path: 技能目录路径
        template: 模板类型（可选）

    Returns:
        Prompt 模板内容
    """
    return get_validate_skill_prompt(skill_path, template)


@mcp.prompt("refactor-skill")
def refactor_skill_prompt(
    skill_path: str,
    focus: list[str] | None = None,
) -> str:
    """重构技能的 Prompt 模板.

    Args:
        skill_path: 技能目录路径
        focus: 重点关注领域（可选）

    Returns:
        Prompt 模板内容
    """
    return get_refactor_skill_prompt(skill_path, focus)


__all__ = ["mcp"]
