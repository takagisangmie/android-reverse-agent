// Crypto trace template for CTF / authorized APK analysis.
// Logs common Java crypto API usage. It observes parameters and return sizes.

Java.perform(function () {
  function bytesToHex(bytes) {
    if (!bytes) return "null";
    var out = [];
    for (var i = 0; i < bytes.length; i++) {
      var b = bytes[i];
      if (b < 0) b += 256;
      out.push(("0" + b.toString(16)).slice(-2));
    }
    return out.join("");
  }

  try {
    var MessageDigest = Java.use("java.security.MessageDigest");
    MessageDigest.digest.overload("[B").implementation = function (input) {
      console.log("[MessageDigest.digest] alg=" + this.getAlgorithm() + " input=" + bytesToHex(input));
      var ret = this.digest(input);
      console.log("[MessageDigest.digest] ret=" + bytesToHex(ret));
      return ret;
    };
  } catch (e) {
    console.log("[skip] MessageDigest hook failed: " + e);
  }

  try {
    var Mac = Java.use("javax.crypto.Mac");
    Mac.doFinal.overload("[B").implementation = function (input) {
      console.log("[Mac.doFinal] alg=" + this.getAlgorithm() + " input=" + bytesToHex(input));
      var ret = this.doFinal(input);
      console.log("[Mac.doFinal] ret=" + bytesToHex(ret));
      return ret;
    };
  } catch (e) {
    console.log("[skip] Mac hook failed: " + e);
  }

  try {
    var Cipher = Java.use("javax.crypto.Cipher");
    Cipher.doFinal.overload("[B").implementation = function (input) {
      console.log("[Cipher.doFinal] alg=" + this.getAlgorithm() + " input=" + bytesToHex(input));
      var ret = this.doFinal(input);
      console.log("[Cipher.doFinal] ret=" + bytesToHex(ret));
      return ret;
    };
  } catch (e) {
    console.log("[skip] Cipher hook failed: " + e);
  }
});
