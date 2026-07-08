// OkHttp trace template for CTF / authorized APK analysis.
// Logs URL, method, headers and call stack where available.

Java.perform(function () {
  function logStack() {
    try {
      var Log = Java.use("android.util.Log");
      var Exception = Java.use("java.lang.Exception");
      console.log(Log.getStackTraceString(Exception.$new()));
    } catch (e) {}
  }

  try {
    var RequestBuilder = Java.use("okhttp3.Request$Builder");

    RequestBuilder.url.overload("java.lang.String").implementation = function (url) {
      console.log("[OkHttp Request.Builder.url] " + url);
      logStack();
      return this.url(url);
    };

    RequestBuilder.addHeader.implementation = function (name, value) {
      console.log("[OkHttp addHeader] " + name + ": " + value);
      return this.addHeader(name, value);
    };

    RequestBuilder.header.implementation = function (name, value) {
      console.log("[OkHttp header] " + name + ": " + value);
      return this.header(name, value);
    };
  } catch (e) {
    console.log("[skip] OkHttp3 Request.Builder hook failed: " + e);
  }
});
