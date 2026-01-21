"""常量定义模块.

定义项目中使用的各种常量，避免魔法数字。
"""

# ==================== SKILL.md 行数限制 ====================

# SKILL.md 推荐最大行数
SKILL_MD_RECOMMENDED_MAX_LINES: int = 150

# SKILL.md 良好最大行数
SKILL_MD_GOOD_MAX_LINES: int = 200

# SKILL.md 及格最大行数
SKILL_MD_ACCEPTABLE_MAX_LINES: int = 350

# SKILL.md 不及格行数阈值
SKILL_MD_POOR_THRESHOLD_LINES: int = 500

# 引用文件推荐行数范围
REFERENCE_FILE_MIN_LINES: int = 200
REFERENCE_FILE_MAX_LINES: int = 300

# 引用文件过长阈值
REFERENCE_FILE_LONG_THRESHOLD: int = 400

# 引用文件最大数量
REFERENCE_FILE_MAX_COUNT: int = 5

# ==================== Token 效率阈值 ====================

# 优秀首次加载 tokens
EXCELLENT_TOKENS: int = 1000

# 良好首次加载 tokens
GOOD_TOKENS: int = 2000

# 及格首次加载 tokens
ACCEPTABLE_TOKENS: int = 3500

# 不及格首次加载 tokens
POOR_TOKENS: int = 5000

# 内容密度百分比阈值
CONTENT_DENSITY_EXCELLENT: float = 0.70  # 70%
CONTENT_DENSITY_GOOD: float = 0.50  # 50%
CONTENT_DENSITY_ACCEPTABLE: float = 0.30  # 30%

# ==================== 代码大小阈值 ====================

# 代码总行数较多阈值（用于生成建议）
CODE_SIZE_MANY_LINES_THRESHOLD: int = 1000

# 代码总行数过多阈值（用于重构建议）
CODE_SIZE_LARGE_THRESHOLD: int = 2000

# 代码总行数非常大阈值
CODE_SIZE_VERY_LARGE_THRESHOLD: int = 5000

# ==================== 复杂度阈值 ====================

# 圈复杂度低阈值
CYCLOMATIC_COMPLEXITY_LOW: int = 5

# 圈复杂度中等阈值
CYCLOMATIC_COMPLEXITY_MEDIUM: int = 15

# 圈复杂度高阈值
CYCLOMATIC_COMPLEXITY_HIGH: int = 25

# 可维护性指数低阈值
MAINTAINABILITY_INDEX_LOW: int = 50

# 可维护性指数良好阈值
MAINTAINABILITY_INDEX_GOOD: int = 70

# ==================== 可维护性指数计算常量 ====================#

# MI = max(0, 171 - 0.23*avg_complexity - 16.2*total_complexity/1000)
MI_BASE_CONSTANT: float = 171.0
MI_AVG_COMPLEXITY_COEFFICIENT: float = 0.23
MI_TOTAL_COMPLEXITY_COEFFICIENT: float = 16.2
MI_COMPLEXITY_SCALE: float = 1000.0

# ==================== 质量评分权重 ====================

NAMING_WEIGHT: float = 0.15
DESCRIPTION_WEIGHT: float = 0.25
STRUCTURE_WEIGHT: float = 0.30
CONTENT_WEIGHT: float = 0.20
TOKEN_EFFICIENCY_WEIGHT: float = 0.10

# ==================== 质量分数 ====================

# SKILL.md 行数评分
SKILL_MD_SCORE_EXCELLENT: int = 30
SKILL_MD_SCORE_GOOD: int = 25
SKILL_MD_SCORE_ACCEPTABLE: int = 15
SKILL_MD_SCORE_MINIMAL: int = 10

# 文档评分
DOCUMENTATION_SCORE_EXCELLENT: int = 30
DOCUMENTATION_SCORE_GOOD: int = 25
DOCUMENTATION_SCORE_ACCEPTABLE: int = 15
DOCUMENTATION_SCORE_MINIMAL: int = 10

# 测试覆盖率评分
TEST_COVERAGE_SCORE_EXCELLENT: int = 30
TEST_COVERAGE_SCORE_GOOD: int = 25
TEST_COVERAGE_SCORE_ACCEPTABLE: int = 15
TEST_COVERAGE_SCORE_MINIMAL: int = 5

# ==================== 文件大小限制 ====================

# 单个文件最大行数
SINGLE_FILE_MAX_LINES: int = 500

# ==================== 描述长度限制 ====================

# 描述最小字符数
DESCRIPTION_MIN_CHARS: int = 50

# 描述推荐字符数范围
DESCRIPTION_RECOMMENDED_MIN_CHARS: int = 150
DESCRIPTION_RECOMMENDED_MAX_CHARS: int = 300

# 描述最大字符数
DESCRIPTION_MAX_CHARS: int = 1024

# ==================== 技能名称限制 ====================

# 技能名称最小长度
SKILL_NAME_MIN_LENGTH: int = 3

# 技能名称最大长度
SKILL_NAME_MAX_LENGTH: int = 50

# ==================== 重构工作量估算 ====================

# 重构工作量估算（小时）
EFFORT_HIGH: int = 8
EFFORT_MEDIUM: int = 4
EFFORT_LOW: int = 1

__all__ = [
    # SKILL.md 行数限制
    "SKILL_MD_RECOMMENDED_MAX_LINES",
    "SKILL_MD_GOOD_MAX_LINES",
    "SKILL_MD_ACCEPTABLE_MAX_LINES",
    "SKILL_MD_POOR_THRESHOLD_LINES",
    "REFERENCE_FILE_MIN_LINES",
    "REFERENCE_FILE_MAX_LINES",
    "REFERENCE_FILE_LONG_THRESHOLD",
    "REFERENCE_FILE_MAX_COUNT",
    # Token 效率阈值
    "EXCELLENT_TOKENS",
    "GOOD_TOKENS",
    "ACCEPTABLE_TOKENS",
    "POOR_TOKENS",
    "CONTENT_DENSITY_EXCELLENT",
    "CONTENT_DENSITY_GOOD",
    "CONTENT_DENSITY_ACCEPTABLE",
    # 代码大小阈值
    "CODE_SIZE_LARGE_THRESHOLD",
    "CODE_SIZE_VERY_LARGE_THRESHOLD",
    # 复杂度阈值
    "CYCLOMATIC_COMPLEXITY_LOW",
    "CYCLOMATIC_COMPLEXITY_MEDIUM",
    "CYCLOMATIC_COMPLEXITY_HIGH",
    "MAINTAINABILITY_INDEX_LOW",
    "MAINTAINABILITY_INDEX_GOOD",
    # 可维护性指数计算常量
    "MI_BASE_CONSTANT",
    "MI_AVG_COMPLEXITY_COEFFICIENT",
    "MI_TOTAL_COMPLEXITY_COEFFICIENT",
    "MI_COMPLEXITY_SCALE",
    # 质量评分权重
    "NAMING_WEIGHT",
    "DESCRIPTION_WEIGHT",
    "STRUCTURE_WEIGHT",
    "CONTENT_WEIGHT",
    "TOKEN_EFFICIENCY_WEIGHT",
    # 质量分数
    "SKILL_MD_SCORE_EXCELLENT",
    "SKILL_MD_SCORE_GOOD",
    "SKILL_MD_SCORE_ACCEPTABLE",
    "SKILL_MD_SCORE_MINIMAL",
    "DOCUMENTATION_SCORE_EXCELLENT",
    "DOCUMENTATION_SCORE_GOOD",
    "DOCUMENTATION_SCORE_ACCEPTABLE",
    "DOCUMENTATION_SCORE_MINIMAL",
    "TEST_COVERAGE_SCORE_EXCELLENT",
    "TEST_COVERAGE_SCORE_GOOD",
    "TEST_COVERAGE_SCORE_ACCEPTABLE",
    "TEST_COVERAGE_SCORE_MINIMAL",
    # 文件大小限制
    "SINGLE_FILE_MAX_LINES",
    # 描述长度限制
    "DESCRIPTION_MIN_CHARS",
    "DESCRIPTION_RECOMMENDED_MIN_CHARS",
    "DESCRIPTION_RECOMMENDED_MAX_CHARS",
    "DESCRIPTION_MAX_CHARS",
    # 技能名称限制
    "SKILL_NAME_MIN_LENGTH",
    "SKILL_NAME_MAX_LENGTH",
    # 重构工作量估算
    "EFFORT_HIGH",
    "EFFORT_MEDIUM",
    "EFFORT_LOW",
]
