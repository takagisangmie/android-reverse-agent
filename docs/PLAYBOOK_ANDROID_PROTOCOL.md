# Playbook: Android 协议分析

## 目标问题

1. APK 使用什么协议？
2. 请求发送到哪里？
3. payload 是什么格式？
4. 是否加密？
5. 是否有签名字段？
6. 是否上传设备指纹？
7. 关键字段从哪里来？

## 静态入口

### 网络库特征

```text
OkHttpClient
Request.Builder
Retrofit
HttpURLConnection
URLConnection
WebSocket
Socket
DatagramSocket
grpc
io.grpc
```

### payload 格式

```text
JSONObject
JSONArray
Gson
Moshi
Jackson
protobuf
MessageLite
toByteArray
parseFrom
Base64
application/json
application/x-www-form-urlencoded
application/octet-stream
```

### 关键字段

```text
sign
signature
token
nonce
timestamp
ts
device
deviceId
android_id
fingerprint
oaid
imei
imsi
model
brand
sdk
version
uid
session
key
iv
cipher
```

## 动态 trace 点

优先级：

1. OkHttp Interceptor / RealCall
2. RequestBody.writeTo
3. HttpURLConnection.getOutputStream
4. WebSocket send
5. javax.crypto.Cipher.doFinal
6. MessageDigest.digest
7. Mac.doFinal
8. Base64.encodeToString
9. native sign/encrypt 方法
