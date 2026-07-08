# Playbook: Native / JNI 分析

## 目标

1. 找 native so。
2. 找 Java native 方法。
3. 找 System.loadLibrary。
4. 找 JNI_OnLoad。
5. 找 RegisterNatives。
6. 建立 Java 方法到 native 函数的映射。
7. 判断 native 是否负责 sign/encrypt/check/flag/vmp。

## 静态关键词

Java 层：

```text
native
System.loadLibrary
System.load
JNI
sign
encrypt
decrypt
check
verify
flag
```

Native 层：

```text
JNI_OnLoad
RegisterNatives
Java_
GetStringUTFChars
NewStringUTF
FindClass
GetMethodID
CallObjectMethod
```

## RegisterNatives 结构

```c
typedef struct {
    const char* name;
    const char* signature;
    void* fnPtr;
} JNINativeMethod;
```

输出应包含 java_class、java_method、signature、native_address、native_name、source。

## JNI_OnLoad 检查点

- 是否检测包名/签名。
- 是否检测调试器。
- 是否检测 emulator/root/frida。
- 是否初始化字符串解密表。
- 是否初始化 VM handler table。
- 是否注册 native 方法。
- 是否解密 dex/so。
- 是否创建线程做检测。
