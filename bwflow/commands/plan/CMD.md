# bwflow:plan

分析需求，拆解为可执行的子任务，生成 PRD 文档。

---

## 目标

在进入实现之前，确保需求清晰、上下文完整。

## 执行步骤

1. **理解用户需求**：与用户确认需求背景、目标和约束
2. **调用 Research Agent**：搜索相关蓝图和规范
3. **生成 PRD 文档**：写入 `bwflow/tasks/{MM-DD-name}/prd.md`
4. **识别涉及的蓝图**：确定需要阅读的 `bwflow/blueprint/` 文件
5. **识别相关规范**：确定需要遵循的 `bwflow/spec/` 文件
6. **配置任务上下文**：填充 `context/blueprint.jsonl` 和 `context/implement.jsonl`
7. **更新 task.json**：设置 `status: planning`

## PRD 模板

```markdown
# {任务标题}

## 目标
{要解决什么问题}

## 需求
- {需求 1}
- {需求 2}

## 验收标准
- [ ] {标准 1}
- [ ] {标准 2}

## 技术约束
{任何技术决策或约束}

## 涉及模块
- bwflow/blueprint/{module}/
- bwflow/spec/{module}/
```

## 输出结果

- `prd.md` 文档
- `task.json` 更新
- `context/blueprint.jsonl` 蓝图引用
- `context/implement.jsonl` 实现上下文
