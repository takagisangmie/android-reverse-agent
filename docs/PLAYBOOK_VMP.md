# Playbook: VMP 算法分析

## 目标

VMP 分析不是一口气还原全部虚拟机，而是优先恢复和 flag / sign / encrypt 相关的关键路径。

## 识别特征

- 大 switch 或间接跳转。
- handler table。
- opcode bytecode 数组。
- VM context 结构体。
- while 循环 dispatch。
- 大量小 handler。
- 栈/寄存器数组读写。
- 常量池或加密字符串表。
- 控制流平坦化和状态变量。

## 分析步骤

1. 找 dispatcher。
2. 找 opcode fetch 和 pc update。
3. 找 handler table。
4. 找 VM context。
5. trace opcode 序列。
6. 标记 handler 语义。
7. 还原关键路径。
8. 生成 solver。

## handler 语义标注

```json
{
  "opcode": "0x13",
  "handler": "0x7abc",
  "semantic": "xor_reg_imm",
  "reads": ["r1", "imm"],
  "writes": ["r1"],
  "confidence": 0.7
}
```

## 证据要求

VMP 结论必须同时包含：dispatcher 地址、opcode 序列样本、handler table 证据、VM context 猜测依据、至少一个 handler 的可验证语义。
