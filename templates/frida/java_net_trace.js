// Java network trace template for CTF / authorized APK analysis.
// Goal: observe request construction and payload flow without modifying behavior.

Java.perform(function () {
  function safeToString(x) {
    try { return x ? x.toString() : "null"; } catch (e) { return "<toString failed>"; }
  }

  var URL = Java.use("java.net.URL");
  URL.openConnection.overload().implementation = function () {
    var ret = this.openConnection();
    console.log("[URL.openConnection] " + safeToString(this));
    return ret;
  };

  try {
    var HttpURLConnection = Java.use("java.net.HttpURLConnection");
    HttpURLConnection.setRequestMethod.implementation = function (method) {
      console.log("[HttpURLConnection.setRequestMethod] " + method);
      return this.setRequestMethod(method);
    };
  } catch (e) {
    console.log("[skip] HttpURLConnection hook failed: " + e);
  }
});
