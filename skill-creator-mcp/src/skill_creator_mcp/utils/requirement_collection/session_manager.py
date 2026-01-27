"""会话状态管理模块.

提供 SessionStateManager 类，集中管理会话状态的加载、保存和更新操作。
"""

from datetime import datetime
from datetime import timezone as tz
from typing import Any

from fastmcp import Context


class SessionStateManager:
    """会话状态管理器.

    集中管理会话状态的加载、保存和更新操作。
    """

    def __init__(self, ctx: Context, session_id: str, state_prefix: str = "requirement_"):
        """初始化会话状态管理器.

        Args:
            ctx: MCP 上下文
            session_id: 会话ID
            state_prefix: 状态键前缀，默认为 "requirement_"
        """
        self.ctx = ctx
        self.session_id = session_id
        self.state_prefix = state_prefix
        self._state: Any | None = None
        self._state_key = f"{state_prefix}{session_id}"

    async def load(self) -> Any:
        """加载会话状态.

        Returns:
            会话状态对象，如果不存在则返回 None
        """
        if self._state is None:
            state_data = await self.ctx.get_state(self._state_key)
            if state_data:
                from ...models.skill_config import SessionState

                self._state = SessionState.model_validate(state_data)
        return self._state

    async def save(self) -> None:
        """保存会话状态."""
        if self._state:
            await self.ctx.set_state(  # type: ignore[func-returns-value]
                self._state_key, self._state.model_dump()
            )

    async def create(
        self,
        mode: str,
        total_steps: int,
        current_step_index: int = 0,
    ) -> Any:
        """创建新的会话状态.

        Args:
            mode: 收集模式
            total_steps: 总步骤数
            current_step_index: 当前步骤索引

        Returns:
            新创建的会话状态对象
        """
        from ...models.skill_config import SessionState

        self._state = SessionState(
            current_step_index=current_step_index,
            answers={},
            started_at=datetime.now(tz.utc).isoformat(),
            completed=False,
            mode=mode,  # type: ignore[arg-type]
            total_steps=total_steps,
        )
        await self.save()
        return self._state

    async def get_or_create(
        self,
        mode: str,
        total_steps: int,
        current_step_index: int = 0,
    ) -> Any:
        """获取或创建会话状态.

        Args:
            mode: 收集模式
            total_steps: 总步骤数
            current_step_index: 当前步骤索引

        Returns:
            会话状态对象
        """
        state = await self.load()
        if state is None:
            state = await self.create(mode, total_steps, current_step_index)
        return state

    async def update(self, **updates: Any) -> None:
        """更新会话状态字段.

        Args:
            **updates: 要更新的字段和值
        """
        state = await self.load()
        if state:
            for key, value in updates.items():
                if hasattr(state, key):
                    setattr(state, key, value)
            await self.save()

    @property
    def state(self) -> Any | None:
        """获取当前会话状态（不触发加载）."""
        return self._state

    @property
    def key(self) -> str:
        """获取状态键."""
        return self._state_key
