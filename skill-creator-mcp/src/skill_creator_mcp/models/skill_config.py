"""技能配置数据模型."""

import re
from typing import Literal

from pydantic import BaseModel, Field, field_validator

# 模板类型字面量
SkillTemplateType = Literal["minimal", "tool-based", "workflow-based", "analyzer-based"]


class InitSkillInput(BaseModel):
    """初始化技能输入参数模型."""

    name: str = Field(
        ...,
        description="技能名称（小写字母、数字、连字符，1-64字符）",
        min_length=1,
        max_length=64,
    )
    template: SkillTemplateType = Field(
        default="minimal",
        description="技能模板类型",
    )
    output_dir: str = Field(
        default=".",
        description="输出目录路径",
    )
    with_scripts: bool = Field(
        default=False,
        description="是否包含示例脚本",
    )
    with_examples: bool = Field(
        default=False,
        description="是否包含使用示例",
    )

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        """验证技能名称符合规范.

        规范：
        - 只能包含小写字母、数字、连字符
        - 不能以连字符开头或结尾
        - 不能有连续的连字符

        Args:
            v: 技能名称

        Returns:
            验证通过的技能名称

        Raises:
            ValueError: 名称不符合规范时抛出
        """
        pattern = r'^[a-z0-9]([a-z0-9-]*[a-z0-9])?$'
        if not re.match(pattern, v):
            raise ValueError(
                f"技能名称 '{v}' 不符合规范。"
                "要求：小写字母、数字、连字符，不能以连字符开头或结尾"
            )
        return v


class SkillConfig(BaseModel):
    """技能配置模型."""

    name: str
    template: SkillTemplateType
    description: str | None = None
    author: str | None = None
    version: str = "0.1.0"
    allowed_tools: list[str] | None = None
    mcp_servers: list[str] | None = None
