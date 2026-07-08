# Pipeline 设计

## 总流程

```text
init_case
  ↓
apk_fingerprint
  ↓
unpack_static
  ↓
manifest_analyze
  ↓
capability_scan
  ↓
protocol_analyze
  ↓
field_location
  ↓
native_jni_analyze
  ↓
dynamic_trace_plan
  ↓
vmp_analysis_plan
  ↓
solver_plan
  ↓
report
```

## 任务状态

每个任务有五种状态：pending、running、success、failed、skipped。

失败不直接终止全局流程，而是生成 next_actions。

## 证据回填

每个工具适配器必须返回：

```json
{
  "artifacts": [],
  "evidence": [],
  "findings": [],
  "next_actions": []
}
```

这样后续可以平滑接 LangGraph、Pydantic AI 或 OpenAI Agents SDK。
