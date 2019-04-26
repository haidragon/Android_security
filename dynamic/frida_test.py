import frida
import sys
device = frida.get_usb_device()
pid = device.spawn(["com.android.mediacenter"])
session = device.attach(pid)
device.resume(pid)
scr = """
Interceptor.attach(Module.findExportByName("libapeplayer.so" ,"aSetdatasource_0"), {
    onEnter: function(args) {
        send("called!");
    },
    onLeave:function(retval){   
    }
});
"""
def on_message(message ,data):
    print(message)
script = session.create_script(scr)
script.on("message" , on_message)
script.load()
sys.stdin.read()

#"libapeplayer.so" , "jni_onload"