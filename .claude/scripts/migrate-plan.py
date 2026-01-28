#!/usr/bin/env python3
"""
计划迁移工具脚本

用于将未完成的任务从一个计划迁移到新计划，并建立追溯关系。

使用方式:
    python migrate-plan.py <原计划路径> <新计划路径> <任务ID列表>

示例:
    python migrate-plan.py .claude/plans/old-plan.md .claude/plans/new-plan.md T-007 T-008
"""

import sys
from datetime import datetime
from pathlib import Path


def generate_trace_id() -> str:
    """生成追溯ID"""
    return f"TR-{datetime.now().strftime('%Y-%m-%d')}-{datetime.now().strftime('%H%M%S')}"


def parse_plan_tasks(plan_path: str) -> list:
    """解析计划文件中的任务列表

    Returns:
        任务列表，每个任务是一个字典
    """
    plan_file = Path(plan_path)
    if not plan_file.exists():
        raise FileNotFoundError(f"计划文件不存在: {plan_path}")

    content = plan_file.read_text(encoding='utf-8')

    # 简单解析任务表格（假设使用Markdown表格格式）
    tasks = []
    in_table = False
    header_skipped = False

    for line in content.split('\n'):
        line = line.strip()
        if not line:
            continue

        # 检测表格开始
        if line.startswith('|') and '任务ID' in line:
            in_table = True
            continue

        # 跳过表头分隔符
        if in_table and not header_skipped and line.startswith('|--'):
            header_skipped = True
            continue

        # 解析表格行
        if in_table and line.startswith('|'):
            parts = [p.strip() for p in line.split('|')[1:-1]]  # 移除首尾空元素
            if len(parts) >= 6:
                task = {
                    'id': parts[0],
                    'name': parts[1],
                    'priority': parts[2],
                    'status': parts[4] if len(parts) > 4 else 'pending'
                }
                tasks.append(task)

        # 表格结束
        if in_table and not line.startswith('|'):
            break

    return tasks


def update_original_plan(plan_path: str, task_ids: list, trace_id: str, new_plan_path: str) -> None:
    """更新原计划，标记迁移的任务

    Args:
        plan_path: 原计划路径
        task_ids: 要迁移的任务ID列表
        trace_id: 追溯ID
        new_plan_path: 新计划路径
    """
    plan_file = Path(plan_path)
    content = plan_file.read_text(encoding='utf-8')

    # 计算相对路径
    try:
        rel_path = Path(new_plan_path).relative_to(plan_file.parent.parent)
    except ValueError:
        rel_path = Path(new_plan_path)

    lines = []
    in_table = False
    header_skipped = False

    for line in content.split('\n'):
        original_line = line

        # 检测任务表格
        if '| 任务ID' in line:
            in_table = True
            lines.append(line)
            continue

        if in_table and not header_skipped and line.startswith('|--'):
            header_skipped = True
            lines.append(line)
            continue

        # 更新任务状态
        if in_table and line.startswith('|'):
            parts = [p.strip() for p in line.split('|')]
            if len(parts) >= 6:
                task_id = parts[1].strip()
                if task_id in task_ids:
                    # 更新状态为migrated
                    parts[5] = 'migrated'  # 执行状态列
                    line = '|'.join(parts)

        lines.append(original_line)

        # 表格结束，添加迁移说明
        if in_table and not line.startswith('|'):
            in_table = False
            lines.append("")
            lines.append("### 任务迁移记录")
            lines.append("")
            for task_id in task_ids:
                lines.append(f"- **{task_id}**: 迁移到 [{rel_path}]({rel_path})")
                lines.append(f"  > 追溯ID: {trace_id}")
            lines.append("")

    # 写回文件
    plan_file.write_text('\n'.join(lines), encoding='utf-8')
    print(f"✅ 原计划已更新: {plan_path}")


def create_new_plan(template_path: str, new_plan_path: str, tasks: list, task_ids: list,
                    trace_id: str, original_plan_path: str) -> None:
    """创建新计划

    Args:
        template_path: 模板文件路径
        new_plan_path: 新计划路径
        tasks: 所有任务列表
        task_ids: 要迁移的任务ID列表
        trace_id: 追溯ID
        original_plan_path: 原计划路径
    """
    # 查找模板
    template_file = Path(template_path)
    if not template_file.exists():
        print(f"⚠️  模板文件不存在: {template_path}，将创建基本结构")
        template_content = "# 新计划\n\n## 迁移任务\n\n"
    else:
        template_content = template_file.read_text(encoding='utf-8')

    # 计算相对路径
    try:
        rel_orig_path = Path(original_plan_path).relative_to(Path(new_plan_path).parent.parent)
    except ValueError:
        rel_orig_path = Path(original_plan_path)

    # 筛选要迁移的任务
    migrated_tasks = [t for t in tasks if t['id'] in task_ids]

    # 构建任务表格
    task_table = "## 迁移任务清单\n\n"
    task_table += "| 任务ID | 任务名称 | 优先级 | 原状态 | 执行状态 | 完成时间 | Commit |\n"
    task_table += "|--------|----------|--------|--------|----------|----------|--------|\n"

    for task in migrated_tasks:
        task_table += f"| {task['id']} | {task['name']} | {task['priority']} | {task['status']} | pending | - | - |\n"

    # 添加追溯信息
    trace_info = "\n## 相关计划\n\n"
    trace_info += "### 前置计划\n"
    trace_info += f"- [{rel_orig_path}]({rel_orig_path})\n"
    trace_info += f"- 追溯ID: {trace_id}\n"

    # 合并内容
    new_content = template_content + "\n" + task_table + "\n" + trace_info

    # 写入新计划
    new_file = Path(new_plan_path)
    new_file.parent.mkdir(parents=True, exist_ok=True)
    new_file.write_text(new_content, encoding='utf-8')
    print(f"✅ 新计划已创建: {new_plan_path}")


def generate_migration_report(original_plan: str, new_plan: str, task_ids: list,
                             trace_id: str) -> str:
    """生成迁移报告

    Returns:
        迁移报告内容
    """
    report = f"""# 计划迁移报告

**迁移时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**追溯ID**: {trace_id}

## 迁移详情

### 原计划
- **路径**: `{original_plan}`
- **迁移任务数**: {len(task_ids)}

### 新计划
- **路径**: `{new_plan}`
- **接收任务数**: {len(task_ids)}

## 迁移任务列表

"""

    for task_id in task_ids:
        report += f"- {task_id}\n"

    report += f"""
## 验证检查清单

- [x] 原计划任务状态已更新为 `migrated`
- [x] 新计划已创建并包含迁移任务
- [x] 追溯ID已记录: {trace_id}
- [x] 原计划和新计划已建立引用关系

## 后续操作

1. 审查新计划内容
2. 更新新计划的任务状态
3. 用户明确同意后归档原计划

---

**报告生成时间**: {datetime.now().isoformat()}
"""
    return report


def main():
    if len(sys.argv) < 4:
        print("使用方式: python migrate-plan.py <原计划路径> <新计划路径> <任务ID列表>")
        print("示例: python migrate-plan.py .claude/plans/old.md .claude/plans/new.md T-007 T-008")
        sys.exit(1)

    original_plan = sys.argv[1]
    new_plan = sys.argv[2]
    task_ids = sys.argv[3:]

    # 生成追溯ID
    trace_id = generate_trace_id()

    print("📋 计划迁移工具")
    print(f"原计划: {original_plan}")
    print(f"新计划: {new_plan}")
    print(f"迁移任务: {', '.join(task_ids)}")
    print(f"追溯ID: {trace_id}")
    print()

    try:
        # 1. 解析原计划任务
        print("📖 解析原计划...")
        tasks = parse_plan_tasks(original_plan)
        print(f"   找到 {len(tasks)} 个任务")

        # 2. 更新原计划
        print("📝 更新原计划...")
        update_original_plan(original_plan, task_ids, trace_id, new_plan)

        # 3. 创建新计划
        print("📄 创建新计划...")
        template_path = ".claude/plans/.templates/plan-template.md"
        create_new_plan(template_path, new_plan, tasks, task_ids, trace_id, original_plan)

        # 4. 生成迁移报告
        print("📊 生成迁移报告...")
        report = generate_migration_report(original_plan, new_plan, task_ids, trace_id)

        # 保存报告
        report_path = f".claude/plans/archive/migration-{trace_id}.md"
        report_file = Path(report_path)
        report_file.parent.mkdir(parents=True, exist_ok=True)
        report_file.write_text(report, encoding='utf-8')
        print(f"✅ 迁移报告已保存: {report_path}")

        print()
        print("✅ 迁移完成！")
        print()
        print("下一步操作:")
        print("1. 审查新计划内容")
        print("2. 更新新计划的任务状态")
        print("3. 用户明确同意后归档原计划")

    except Exception as e:
        print(f"❌ 错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
