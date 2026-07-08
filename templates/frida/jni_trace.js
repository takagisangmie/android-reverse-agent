// JNI/native boundary trace template.
// Fill TARGET_CLASS and methods after jadx/static analysis.

Java.perform(function () {
  var TARGET_CLASS = "com.example.NativeLib";

  try {
    var Cls = Java.use(TARGET_CLASS);
    console.log("[jni_trace] Loaded " + TARGET_CLASS);

    // Example:
    // Cls.sign.implementation = function (input) {
    //   console.log("[native sign] input=" + input);
    //   var ret = this.sign(input);
    //   console.log("[native sign] ret=" + ret);
    //   return ret;
    // };
  } catch (e) {
    console.log("[jni_trace] failed: " + e);
  }
});
