"""回退场景集成测试.

测试真实异常场景下的回退机制行为：
- collect_requirements 在高级 API 不可用时的回退
- brainstorm 模式的回退行为
- progressive 模式的回退行为
- 完整性检查的回退行为
"""

from unittest.mock import AsyncMock, MagicMock, Mock

import pytest

from skill_creator_mcp.server import (
    _check_requirement_completeness,
    _generate_brainstorm_question,
    _generate_progressive_question,
    collect_requirements,
)

# ============================================================================
# collect_requirements 回退场景测试
# ============================================================================


@pytest.mark.asyncio
async def test_collect_requirements_with_elicit_unsupported():
    """测试 elicitation 不可用时返回友好错误提示."""
    mock_ctx = MagicMock()

    # Mock elicitation 不支持
    mock_ctx.sample = AsyncMock(side_effect=Exception("Client does not support sampling"))
    mock_ctx.elicit = AsyncMock(side_effect=AttributeError("Method not found"))
    mock_ctx.get_state = AsyncMock(return_value=None)
    mock_ctx.set_state = AsyncMock()
    mock_ctx.session_id = "test-session"

    result = await collect_requirements(
        mock_ctx,
        action="start",
        mode="basic",
        use_elicit=True,
    )

    # 应该返回错误，提示使用传统模式
    assert result["success"] is False
    assert result["error"] == "elicit_mode_not_supported"
    assert "fallback_mode" in result
    assert result["fallback_mode"] == "traditional"
    assert "traditional_usage" in result
    assert "step_1" in result["traditional_usage"]


@pytest.mark.asyncio
async def test_collect_requirements_fallback_to_traditional_mode():
    """测试回退到传统模式后的正常工作流程."""
    mock_ctx = MagicMock()

    # Mock 高级 API 不可用
    mock_ctx.sample = AsyncMock(side_effect=Exception("Client does not support sampling"))
    mock_ctx.elicit = AsyncMock(side_effect=AttributeError("Method not found"))
    mock_ctx.get_state = AsyncMock(return_value=None)
    mock_ctx.set_state = AsyncMock()
    mock_ctx.session_id = "test-session"

    # 步骤 1: 开始收集（不使用 elicit）
    result = await collect_requirements(
        mock_ctx,
        action="start",
        mode="basic",
        use_elicit=False,
    )

    assert result["success"] is True
    assert "session_id" in result
    assert "current_step" in result
    assert result["current_step"]["key"] == "skill_name"

    # 步骤 2: 回答第一个问题
    session_id = result["session_id"]
    result = await collect_requirements(
        mock_ctx,
        action="next",
        session_id=session_id,
        user_input="test-skill",
    )

    assert result["success"] is True
    assert result["answers"]["skill_name"] == "test-skill"


@pytest.mark.asyncio
async def test_collect_requirements_brainstorm_fallback():
    """测试 brainstorm 模式在 LLM 不可用时的回退."""
    mock_ctx = MagicMock()

    # Mock LLM 不可用
    mock_ctx.sample = AsyncMock(side_effect=Exception("Client does not support sampling"))
    mock_ctx.get_state = AsyncMock(return_value=None)
    mock_ctx.set_state = AsyncMock()
    mock_ctx.session_id = "test-session"

    result = await collect_requirements(
        mock_ctx,
        action="start",
        mode="brainstorm",
    )

    assert result["success"] is True
    assert "question" in result
    # 应该返回预定义的 fallback 问题
    assert "is_dynamic_mode" in result
    assert result["is_dynamic_mode"] is True


@pytest.mark.asyncio
async def test_collect_requirements_progressive_fallback():
    """测试 progressive 模式在 LLM 不可用时的回退."""
    mock_ctx = MagicMock()

    # Mock LLM 不可用
    mock_ctx.sample = AsyncMock(side_effect=Exception("Client does not support sampling"))
    mock_ctx.get_state = AsyncMock(return_value=None)
    mock_ctx.set_state = AsyncMock()
    mock_ctx.session_id = "test-session"

    result = await collect_requirements(
        mock_ctx,
        action="start",
        mode="progressive",
    )

    assert result["success"] is True
    assert "question" in result
    assert "is_dynamic_mode" in result
    assert result["is_dynamic_mode"] is True


# ============================================================================
# ============================================================================
# 端到端回退流程测试
# ============================================================================


@pytest.mark.asyncio
async def test_e2e_fallback_workflow_basic():
    """测试 basic 模式完整流程（无 LLM）."""
    mock_ctx = MagicMock()

    # 使用可变状态来模拟会话存储
    session_storage = {}

    async def mock_get_state(key):
        return session_storage.get(key)

    async def mock_set_state(key, value):
        session_storage[key] = value

    # Mock 高级 API 不可用
    mock_ctx.sample = AsyncMock(side_effect=Exception("Client does not support sampling"))
    mock_ctx.get_state = mock_get_state
    mock_ctx.set_state = mock_set_state
    mock_ctx.session_id = "test-session"

    # 完整的 5 步收集流程（答案长度符合验证要求）
    answers = {
        "skill_name": "pdf-helper",
        "skill_function": "解析 PDF 文件，提取文本和图片内容",
        "use_cases": "文档分析和数据提取，用于内容归档和自动化处理",
        "template_type": "tool-based",
        "additional_features": "支持 OCR 文字识别",
    }

    # 步骤 1: 开始
    result = await collect_requirements(mock_ctx, action="start", mode="basic")
    session_id = result["session_id"]

    # 步骤 2-5: 逐个回答
    for key, value in answers.items():
        result = await collect_requirements(
            mock_ctx,
            action="next",
            session_id=session_id,
            user_input=value,
        )
        assert result["success"] is True, f"Failed for key={key}, value={value}"

    # 完成收集
    result = await collect_requirements(
        mock_ctx,
        action="complete",
        session_id=session_id,
    )

    assert result["completed"] is True


@pytest.mark.asyncio
async def test_e2e_fallback_workflow_complete():
    """测试 complete 模式完整流程（无 LLM）."""
    mock_ctx = MagicMock()

    # Mock 高级 API 不可用
    mock_ctx.sample = AsyncMock(side_effect=Exception("Client does not support sampling"))
    mock_ctx.get_state = AsyncMock(return_value=None)
    mock_ctx.set_state = AsyncMock()
    mock_ctx.session_id = "test-session"

    # 开始 complete 模式
    result = await collect_requirements(mock_ctx, action="start", mode="complete")

    # 验证有 10 个步骤
    assert result["total_steps"] == 10


@pytest.mark.asyncio
async def test_e2e_fallback_with_session_recovery():
    """测试会话中断恢复（回退模式）."""
    mock_ctx = MagicMock()

    # Mock 高级 API 不可用
    mock_ctx.sample = AsyncMock(side_effect=Exception("Client does not support sampling"))
    mock_ctx.get_state = AsyncMock(return_value=None)
    mock_ctx.set_state = AsyncMock()
    mock_ctx.session_id = "test-session"

    # 开始会话
    result = await collect_requirements(mock_ctx, action="start", mode="basic")
    session_id = result["session_id"]

    # 回答第一个问题
    await collect_requirements(
        mock_ctx,
        action="next",
        session_id=session_id,
        user_input="test-skill",
    )

    # 模拟中断：查询状态
    state_data = {
        "current_step_index": 1,
        "answers": {"skill_name": "test-skill"},
        "started_at": "2026-01-23T10:00:00Z",
        "completed": False,
        "mode": "basic",
        "total_steps": 5,
    }
    mock_ctx.get_state = AsyncMock(return_value=state_data)

    # 恢复会话
    result = await collect_requirements(
        mock_ctx,
        action="status",
        session_id=session_id,
    )

    assert result["success"] is True
    assert result["step_index"] == 1
    assert result["answers"]["skill_name"] == "test-skill"


# ============================================================================
# ============================================================================
# 回退函数直接测试
# ============================================================================


@pytest.mark.asyncio
async def test_check_requirement_completeness_fallback():
    """测试完整性检查的回退行为."""
    mock_ctx = MagicMock()

    # Mock LLM 不可用
    mock_ctx.sample = AsyncMock(side_effect=Exception("Client does not support sampling"))

    answers = {
        "skill_name": "test-skill",
        "skill_function": "测试功能",
    }

    result = await _check_requirement_completeness(mock_ctx, answers)

    # 应该回退到简单检查
    assert "is_complete" in result
    assert result["is_complete"] is False  # 缺少 use_cases 和 template_type
    assert "missing_info" in result
    assert len(result["missing_info"]) == 2


@pytest.mark.asyncio
async def test_generate_brainstorm_question_fallback():
    """测试 brainstorm 问题生成的回退行为."""
    mock_ctx = MagicMock()

    # Mock LLM 不可用
    mock_ctx.sample = AsyncMock(side_effect=Exception("Client does not support sampling"))

    result = await _generate_brainstorm_question(
        mock_ctx,
        answers={},
        conversation_history=None,
    )

    # 应该返回预定义问题
    assert result["success"] is True
    assert "question" in result
    assert result["is_dynamic"] is False
    assert result["source"] == "fallback"


@pytest.mark.asyncio
async def test_generate_progressive_question_fallback():
    """测试 progressive 问题生成的回退行为（异常情况，统一格式）."""
    mock_ctx = MagicMock()

    # Mock LLM 不可用
    mock_ctx.sample = AsyncMock(side_effect=Exception("Client does not support sampling"))

    result = await _generate_progressive_question(
        mock_ctx,
        answers={},
    )

    # 异常时现在返回 success:True（与 brainstorm 保持一致）
    assert result["success"] is True
    assert "error" in result  # 保留错误信息供调试
    assert "next_question" in result
    assert result["is_dynamic"] is False
    assert result["source"] == "fallback"
    assert "question_key" in result


# ============================================================================
# ============================================================================
# 边界情况测试
# ============================================================================


@pytest.mark.asyncio
async def test_fallback_with_empty_answers():
    """测试空答案时的回退行为."""
    mock_ctx = MagicMock()

    mock_ctx.sample = AsyncMock(side_effect=Exception("Client does not support sampling"))

    result = await _check_requirement_completeness(mock_ctx, {})

    assert result["is_complete"] is False
    assert len(result["missing_info"]) == 4


@pytest.mark.asyncio
async def test_fallback_with_all_answers():
    """测试所有答案都存在时的回退行为."""
    mock_ctx = MagicMock()

    mock_ctx.sample = AsyncMock(side_effect=Exception("Client does not support sampling"))

    answers = {
        "skill_name": "test-skill",
        "skill_function": "测试功能",
        "use_cases": "测试场景",
        "template_type": "tool-based",
    }

    result = await _check_requirement_completeness(mock_ctx, answers)

    assert result["is_complete"] is True
    assert len(result["missing_info"]) == 0


@pytest.mark.asyncio
async def test_brainstorm_fallback_progression():
    """测试 brainstorm 回退问题随着答案增加而变化."""
    mock_ctx = MagicMock()

    mock_ctx.sample = AsyncMock(side_effect=Exception("Client does not support sampling"))

    # 第一次：没有答案
    result1 = await _generate_brainstorm_question(
        mock_ctx,
        answers={},
        conversation_history=None,
    )

    # 第二次：有一个答案
    result2 = await _generate_brainstorm_question(
        mock_ctx,
        answers={"skill_name": "test"},
        conversation_history=None,
    )

    # 应该返回不同的预定义问题
    assert result1["question"] != result2["question"]


@pytest.mark.asyncio
async def test_progressive_fallback_smart_questions():
    """测试 progressive 回退问题智能选择（JSON 解析失败情况）."""
    mock_ctx = MagicMock()

    # 模拟 JSON 解析失败但 LLM 返回了文本
    mock_sample_result = Mock()
    mock_sample_result.text = "Some non-JSON text"
    mock_ctx.sample = AsyncMock(return_value=mock_sample_result)

    # 没有答案时应该问 skill_name
    result1 = await _generate_progressive_question(mock_ctx, {})
    # JSON 解析失败后使用基础问题列表
    assert "next_question" in result1
    assert "question_key" in result1
    # 第一个问题应该是 skill_name
    assert result1["question_key"] == "skill_name"

    # 有 skill_name 时应该问 skill_function
    result2 = await _generate_progressive_question(mock_ctx, {"skill_name": "test"})
    assert result2["question_key"] == "skill_function"
