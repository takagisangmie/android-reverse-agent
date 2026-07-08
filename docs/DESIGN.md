# Android Reverse Agent 设计总纲

## 核心思想

Android Reverse Agent 不是让 LLM 单独猜题，而是构建一个证据驱动的 Android 逆向闭环。

```text
Observation 观察
→ Hypothesis 假设
→ Action 工具动作
→ Evidence 证据
→ Verification 验证
→ Report 结论
```

每个模块都必须输出结构化证据，避免“模型看起来分析得很对，但没有可复现依据”。

## 核心对象

### Case

一次 APK 分析任务，包含 apk_path、package_name、workdir、artifacts、evidence、findings 和 next_actions。

### Artifact

分析过程中的中间产物，例如 apktool 输出目录、jadx 输出目录、AndroidManifest.xml、native so、strings.txt、trace 日志、solver.py。

### Evidence

证据是整个系统的核心，字段包括 source、kind、location、summary、confidence、raw 和 tags。

### Finding

经过整理后的发现，例如上传设备指纹、sign 字段由 native 生成、JNI_OnLoad 注册 native 方法、发现 VMP dispatcher、发现算法痕迹。

### NextAction

下一步动作，例如 run_jadx、locate_field_source、trace_okhttp、inspect_jni_onload、emulate_native_method、build_solver。

## 分析主流程

```text
Sample Intake
→ Static Unpack
→ Capability Scan
→ Protocol Analysis
→ Field Source Location
→ Native/JNI Analysis
→ Dynamic Trace
→ VMP Analysis
→ Solver and Writeup
```

## 协议分析目标

协议分析不是只抓包，而是建立请求字段生成链路。最终需要回答：

- 使用什么协议：HTTP/HTTPS/WebSocket/TCP/UDP/gRPC/自定义二进制。
- 请求发送到哪里：endpoint、method、headers、content-type。
- payload 是什么格式：JSON、Form、Protobuf、MsgPack、加密 blob。
- 有哪些关键字段：sign、token、timestamp、nonce、deviceId、fingerprint、uid、session。
- 字段从哪里来：常量、SharedPreferences、Java 拼接、native 生成、服务端返回。
- 是否上传设备指纹：Android ID、IMEI、OAID、Build、fingerprint、brand、model、root/debug/emulator 检测结果。

## 关键字段定位

字段定位的本质是数据流反向追踪。

```text
网络字段
← 请求构造
← 参数对象
← 字符串拼接 / JSON put / map put
← 加密/签名方法
← 原始输入 / 设备信息 / native 返回值
```

## Native/JNI 分析

目标：

- 识别 System.loadLibrary / System.load。
- 识别 Java native 方法。
- 分析 JNI_OnLoad。
- 解析 RegisterNatives。
- 建立 Java native 方法到 so 函数地址映射。
- 判断 native 是否负责 sign/encrypt/check/flag/vmp。

## VMP 分析

VMP 分析不是一口气还原全部虚拟机，而是优先恢复和 flag/sign/encrypt 相关的关键路径。

步骤：

1. 找 dispatcher。
2. 找 opcode fetch。
3. 找 handler table。
4. 找 VM context。
5. trace opcode 序列。
6. 标记 handler 语义。
7. 还原关键路径。
8. 生成 solver。

## Agent 边界

LLM 适合做：总结反编译代码、判断字段生成链、生成 trace 脚本草案、生成 solver 草案、归纳 evidence、生成 writeup。

LLM 不应该单独决定：flag 是否正确、某字段一定来自某函数、某算法一定是什么、某路径一定可达。这些必须由工具或运行结果验证。
