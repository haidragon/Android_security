Interceptor.attach(Module.findExportByName("libapeplayer.so" , "jni_onload"),{
	onEnter: function(args){
		console.log("called!")
	},
	onLeave:function(retval){

	}
});