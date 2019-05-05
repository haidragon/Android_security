Java.perform(function () {

    var FileClazz = Java.use("java.io.File");
    var class_exception = Java.use("java.lang.Exception");
    var class_log = Java.use("android.util.Log");
    var ape_claz = Java.use("com.huawei.extendedplayer.ape.APEPlayer")
    var PATTERN = "";

    function backtrace(){
        var my_exception_obj = class_exception.$new();
        trace = class_log.getStackTraceString(my_exception_obj);  
        console.log(trace);
    }

    ape_claz.seekTo.implementation = function( a0 ){
        // a0 is long type value
        console.log("seekTo hooked, time is " + a0.toString())
        return this.seekTo(a0)
        // return this.seekTo(-1)
    }

    ape_claz._setDataSource.implementation = function( a0 ){
        // a0 is tring
        console.log("ape_claz.setDataSource hooked")
        return this.setDataSource(a0)
    }

});

