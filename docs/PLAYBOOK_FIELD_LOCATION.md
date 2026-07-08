# Playbook: 关键字段定位

## 核心思路

字段定位的本质是数据流反向追踪：

```text
网络字段
← 请求构造
← 参数对象
← 字符串拼接 / JSON put / map put
← 加密/签名方法
← 原始输入 / 设备信息 / native 返回值
```

## Java 层定位策略

### JSON 字段

搜索：

```text
put("field"
put(\"field\"
"field"
```

关注 JSONObject.put、Map.put、Gson model field、data class、builder.setXxx。

### Form 字段

关注 FormBody.Builder.add、HashMap.put、RequestParams、MultipartBody.Part。

### Header 字段

关注 addHeader、header、headers、Interceptor。

### Protobuf 字段

关注 Builder.setXxx、toByteArray、parseFrom、GeneratedMessageLite、fieldNumber。

## FieldTrace 输出

```text
field_name
request_location
builder_method
value_provider
crypto_method
native_dependency
runtime_trace
confidence
```

## 下一步动作

- 字段由 Java 明文拼接：生成复现脚本。
- 字段由 Java crypto 生成：trace Cipher/Mac/MessageDigest。
- 字段来自 native：进入 JNI 分析。
- 字段来自服务端：记录前置请求。
- 字段来自设备：进入 fingerprint 分析。
