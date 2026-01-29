#!/usr/bin/env bash
# 文档一致性验证脚本
# 用于验证文档中的工具数量、测试数量与实际代码一致

set -euo pipefail

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 项目根目录
PROJECT_ROOT="/models/claude-glm/Skills-Creator"
MCP_SERVER_DIR="${PROJECT_ROOT}/skill-creator-mcp"

echo "===================================="
echo "文档一致性验证脚本"
echo "===================================="
echo ""

# 1. 统计实际 MCP 工具数量
echo "[1/5] 统计实际 MCP 工具数量..."
cd "${MCP_SERVER_DIR}"
# 只统计独立的 @mcp.tool() 行（排除注释和空格）
ACTUAL_TOOL_COUNT=$(grep -E "^[[:space:]]*@mcp\.tool\(\)" src/skill_creator_mcp/server.py | wc -l | xargs)
echo "实际 MCP 工具数量: ${ACTUAL_TOOL_COUNT}"

# 2. 统计实际测试用例数量
echo ""
echo "[2/5] 统计实际测试用例数量..."
ACTUAL_TEST_COUNT=$(uv run pytest --collect-only -q 2>/dev/null | grep -E "test session starts|tests collected" | tail -1 | grep -oE "[0-9]+ tests collected" | grep -oE "^[0-9]+" || echo "未知")
if [ "$ACTUAL_TEST_COUNT" = "未知" ]; then
    ACTUAL_TEST_COUNT=$(uv run pytest --collect-only 2>/dev/null | grep -oE "^[0-9]+ test" | grep -oE "^[0-9]+" || echo "未知")
fi
echo "实际测试用例数量: ${ACTUAL_TEST_COUNT}"

# 3. 检查 CLAUDE.md 中的数量声明
echo ""
echo "[3/5] 检查 CLAUDE.md 中的数量声明..."
cd "${PROJECT_ROOT}"
CLAUDE_TOOL_COUNT=$(grep -oE "[0-9]+ Tools" CLAUDE.md | head -1 | grep -oE "[0-9]+" || echo "未找到")
CLAUDE_TEST_COUNT=$(grep -oE "[0-9]+个测试" CLAUDE.md | head -1 | grep -oE "[0-9]+" || echo "未找到")
echo "CLAUDE.md 工具数量: ${CLAUDE_TOOL_COUNT}"
echo "CLAUDE.md 测试数量: ${CLAUDE_TEST_COUNT}"

# 4. 检查 README.md 中的数量声明
echo ""
echo "[4/5] 检查 README.md 中的数量声明..."
cd "${MCP_SERVER_DIR}"
README_TEST_COUNT=$(grep "tests-" README.md | grep -oE "tests-[0-9]+%20passed" | head -1 | sed 's/tests-//;s/%20passed//' | head -1 || echo "未找到")
echo "README.md 测试数量: ${README_TEST_COUNT}"

# 5. 生成验证报告
echo ""
echo "[5/5] 生成验证报告..."
echo ""
echo "===================================="
echo "验证报告"
echo "===================================="
echo ""

ERRORS=0

# 检查工具数量
if [ "$CLAUDE_TOOL_COUNT" != "未找到" ]; then
    if [ "$CLAUDE_TOOL_COUNT" = "$ACTUAL_TOOL_COUNT" ]; then
        echo -e "${GREEN}✓ 工具数量一致: ${ACTUAL_TOOL_COUNT}${NC}"
    else
        echo -e "${RED}✗ 工具数量不一致: CLAUDE.md 声称 ${CLAUDE_TOOL_COUNT}, 实际 ${ACTUAL_TOOL_COUNT}${NC}"
        ((ERRORS++))
    fi
else
    echo -e "${YELLOW}⚠ CLAUDE.md 中未找到工具数量声明${NC}"
fi

# 检查测试数量
echo ""
if [ "$CLAUDE_TEST_COUNT" != "未找到" ] && [ "$README_TEST_COUNT" != "未找到" ]; then
    if [ "$CLAUDE_TEST_COUNT" = "$ACTUAL_TEST_COUNT" ] && [ "$README_TEST_COUNT" = "$ACTUAL_TEST_COUNT" ]; then
        echo -e "${GREEN}✓ 测试数量一致: ${ACTUAL_TEST_COUNT}${NC}"
    else
        if [ "$CLAUDE_TEST_COUNT" != "$ACTUAL_TEST_COUNT" ]; then
            echo -e "${RED}✗ CLAUDE.md 测试数量不一致: 声称 ${CLAUDE_TEST_COUNT}, 实际 ${ACTUAL_TEST_COUNT}${NC}"
            ((ERRORS++))
        fi
        if [ "$README_TEST_COUNT" != "$ACTUAL_TEST_COUNT" ]; then
            echo -e "${RED}✗ README.md 测试数量不一致: 声称 ${README_TEST_COUNT}, 实际 ${ACTUAL_TEST_COUNT}${NC}"
            ((ERRORS++))
        fi
    fi
else
    echo -e "${YELLOW}⚠ 文档中未找到测试数量声明${NC}"
fi

echo ""
echo "===================================="
if [ $ERRORS -eq 0 ]; then
    echo -e "${GREEN}✓ 所有检查通过！${NC}"
    exit 0
else
    echo -e "${RED}✗ 发现 ${ERRORS} 个不一致项${NC}"
    exit 1
fi
