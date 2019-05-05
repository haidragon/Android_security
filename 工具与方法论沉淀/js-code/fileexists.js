
String.prototype.endWith=function(str){
    if(str==null||str==""||this.length==0||str.length>this.length)  return false;
    if(this.substring(this.length-str.length)==str) return true;
    else return false;
    return true;
}

Java.perform(function () {
    var FileClazz = Java.use("java.io.File");
    var class_exception = Java.use("java.lang.Exception");
    var class_log = Java.use("android.util.Log");

    FileClazz.exists.implementation = function () {
        var path = this.getAbsolutePath();
        console.log("[*] " + path);
        if ( path.endWith(".jar")){
            var my_exception_obj = class_exception.$new();
            trace = class_log.getStackTraceString(my_exception_obj);  
            console.log(trace);
        }
        return this.exists() ;
    };
});