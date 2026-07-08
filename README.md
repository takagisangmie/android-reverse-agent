# Android Reverse Agent

Android Reverse Agent 是一个面向 **CTF Android Reverse / 授权 APK 安全分析** 的证据驱动逆向工作流骨架。

它不是一个“多 Agent 聊天玩具”，而是一个可扩展的 Reverse Pipeline：

```text
APK 输入
→ 样本建档
→ 静态拆解
→ 协议分析
→ 关键字段定位
→ Java / Native 关联
→ Trace / 动态验证
→ VMP / 算法分析
→ Solver / 复现脚本
→ Writeup 输出
```

## 设计目标

1. **真实 APK 化 CTF 题目分析**
   - Manifest、组件、入口 Activity、ContentProvider、Service、Receiver。
   - Java/Kotlin 逻辑、JNI、RegisterNatives、native so。
   - 网络协议、请求字段、设备指纹、签名字段、加密参数。
   - VMP、字符串加密、反调试、环境检测、反 Hook。

2. **证据驱动**
   - 每个判断都要留下 evidence。
   - 每个关键字段都要能反向定位到 Java 方法、native 方法、trace 点或 solver。
   - 每个推测都要有验证任务，不让 LLM 凭感觉乱跑。

3. **工具可替换**
   - jadx / apktool / aapt2 / baksmali
   - IDA MCP / Ghidra Headless / r2pipe
   - Frida / objection / adb
   - unidbg / Qiling / angr / Z3
   - mitmproxy / tcpdump / Wireshark

4. **适合逐步落地**
   - 先跑静态分析和报告。
   - 再接 jadx/apktool 自动输出。
   - 再接 trace、unidbg、IDA MCP。
   - 最后接 LLM Agent 编排。

## 快速开始

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

pip install -e .

ara init-case samples/demo.apk
ara analyze samples/demo.apk --out cases
ara show-plan cases/<case_id>/case.json
```

当前是地基版本：CLI、数据模型、目录结构、playbooks、trace 模板和设计文档已经搭好；外部工具适配器先以可扩展 stub 形式存在。

## 项目结构

```text
android-reverse-agent/
├── README.md
├── pyproject.toml
├── docs/
├── src/ara/
├── templates/
└── tests/
```

## 推荐使用方式

### 第一阶段：静态报告

目标是快速知道：

- APK 包名、入口、权限。
- 是否有 native so。
- 是否有网络库、加密库、设备指纹相关 API。
- 是否有明显 CTF flag / key / token / sign / nonce / device / fingerprint 字段。
- 哪些 Java 方法值得优先看。

### 第二阶段：协议分析

目标是回答：

- 协议是什么：HTTP/HTTPS/WebSocket/TCP/UDP/gRPC/自定义二进制。
- 请求传输了什么：JSON/Form/Protobuf/MsgPack/加密 blob。
- 关键字段是什么：token/sign/timestamp/nonce/deviceId/fingerprint/uid/session。
- 字段从哪里来：常量、SharedPreferences、Java 拼接、native 生成、服务端返回。
- 是否上传设备指纹：Android ID、IMEI、OAID、Build、fingerprint、brand、model、root/debug/emulator 检测结果。

### 第三阶段：关键字段定位

目标是建立链路：

```text
网络字段
→ 请求构造方法
→ 参数来源
→ Java 计算方法
→ native 方法
→ 加密算法 / VMP / solver
```

### 第四阶段：native / JNI

目标是定位：

- System.loadLibrary 调用链。
- JNI_OnLoad 做了什么。
- RegisterNatives 注册表。
- Java native 方法和 so 函数的映射。
- native 层是否做签名、加密、环境检测、字符串解密、VMP dispatch。

### 第五阶段：VMP / 算法分析

目标是识别：

- dispatcher。
- handler table。
- opcode fetch/decode。
- VM context。
- stack/register/memory model。
- 输入约束、状态转移、关键比较点。
- 是否可以 trace opcode 序列并还原伪代码。

## 安全边界

本项目用于 CTF、授权 APK、教学研究和自有应用分析。不要用于未授权绕过、盗号、恶意 Hook、数据窃取、绕过真实应用风控或商业保护。
