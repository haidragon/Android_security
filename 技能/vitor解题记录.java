    public static String p1EncFn = "ckxalskuaewlkszdva";
    public static String p1Fn = "nsavlkureaasdqwecz";
    public static String p5EncFn = "cxnvhaekljlkjxxqkq";
    public static String rand2EncFn = "fwswzofqwkzhsgdxfr";
    public static String randEncFn = "zslzrfomygfttivyac";
//arg6 is a string
//arg5 
public static boolean cf(MainActivity arg5, String arg6) {
        try {
            fc.cfa(((Context)arg5), fc.p1EncFn);
            fc.cfa(((Context)arg5), fc.p5EncFn);
            fc.cfa(((Context)arg5), fc.randEncFn);
            fc.cfa(((Context)arg5), fc.rand2EncFn);
            //在 arg5的4个文件读取并写入
            if((arg6.startsWith("OOO{")) && (arg6.endsWith("}"))) {
                if(arg6.length() != 45) {
                }
                //arg5, ,arg6
                //fc.dp1(((Context)arg5), new File(arg5.getFilesDir(), fc.p1EncFn), fc.g0(arg6.substring(4, 44)))
                //arg5，arg6
                else if(!fc.cf(((Context)arg5), fc.dp1(((Context)arg5), new File(arg5.getFilesDir(), fc.p1EncFn), fc.g0(arg6.substring(4, 44))), arg6)) {
                    return 0;
                }
                else {
                    File v1 = new File(arg5.getFilesDir(), "bam.html");
                    WebView v5 = arg5.mWebView;
                    v5.loadUrl("file:///" + v1.getAbsolutePath() + "?flag=" + Uri.encode(arg6));
                    return fc.mValid;
                }
            }

            return 0;
        }
        catch(Exception ) {
            return 0;
        }
    }

    private static File cfa(Context arg4, String arg5) throws Exception {
        InputStream v0 = arg4.getAssets().open(arg5);//arg5 is filename 
        //v0 inoput Stream
        //arg4.获取程序默认数据库路径
        //打开了四个
        File v1 = new File(arg4.getFilesDir().getAbsolutePath(), arg5);
        // v0 , v4k,s
        FileOutputStream v4 = new FileOutputStream(v1);
        byte[] v5 = new byte[1024];
        while(true) {
            int v2 = v0.read(v5);
            if(v2 == -1) {
                break;
            }

            ((OutputStream)v4).write(v5, 0, v2);
        }

        v0.close();
        ((OutputStream)v4).close();
        return v1;
    }

    private static boolean cf(Context arg6, File arg7, String arg8) {
        boolean v7;
        File v0 = new File(arg6.getFilesDir().getAbsolutePath());
                              //DexClassLoader(String dexPath, String optimizedDirectory, String libraryPath, ClassLoader parent)
                              //arg7 = fc.dp1(((Context)arg5), new File(arg5.getFilesDir(), fc.p1EncFn), fc.g0(arg6.substring(4, 44)))
        DexClassLoader v1 = new DexClassLoader(arg7.getAbsolutePath(), v0.getAbsolutePath(), v0.getAbsolutePath(), ClassLoader.getSystemClassLoader());
        try {
            Class v0_1 = v1.loadClass("ooo.p1.P1");
            //反射机制之 获取方法然后invoke 执行实例
            v7 = v0_1.getDeclaredMethod("cf", Context.class, String.class).invoke(v0_1, arg6, arg8).booleanValue();
            return v7;

        }
        catch(Exception ) {
            return v7;
        }
    }

    //把flag传进来
    //4-44 = 40
    public static byte[] g0(String arg7) {
        int v0 = 4;
        byte[] v1 = new byte[v0];
        byte[] v7 = arg7.getBytes();
        int v3;
        for(v3 = 0; v3 < v0; ++v3) {
            v1[v3] = 0;
        }
        //v1 = [0,0,0,0]
        for(v3 = 0; v3 < 10; ++v3) {
            int v4;
            for(v4 = 0; v4 < v0; ++v4) {
                v1[v4] = ((byte)(v1[v4] ^ v7[v3 * 4 + v4]));
            }
        }

        return v1;
    }
//fc.dp1(((Context)arg5), new File(arg5.getFilesDir(), fc.p1EncFn), fc.g0(arg6.substring(4, 44)))
//arg5,new File(arg5.getFilesDir(), fc.p1EncFn), fc.g0(arg6.substring(4, 44)
    private static File dp1(Context arg3, File arg4, byte[] arg5) throws Exception {
        //这是一个加密模式
        arg5 = fc.hash(arg5); //得到v1的hash
        byte[] v4 = Files.readAllBytes(arg4.toPath());
        try {

//fc.initVector = new byte[]{19, 55, 19, 55, 19, 55, 19, 55, 19, 55, 19, 55, 19, 55, 19, 55};
//it's v    
            //
            IvParameterSpec v0 = new IvParameterSpec(fc.initVector);
            //两个参数 第一个为私钥字节数组，第二个为加密方式 
            SecretKeySpec v1 = new SecretKeySpec(arg5, "AES");
            //实例化加密类，参数为加密方式，要写全
            Cipher v5 = Cipher.getInstance("AES/CBC/PKCS5PADDING");
            //初始化，此方法可以采用三种方式，按服务器要求来添加。
            //v0 采用此代码中的IVParameterSpec
            v5.init(2, ((Key)v1), ((AlgorithmParameterSpec)v0));
            //v4 is 需要加密的内容
            v4 = v5.doFinal(v4);
            File v5_1 = new File(arg3.getFilesDir(), fc.p1Fn);
            FileOutputStream v3 = new FileOutputStream(v5_1);
            ((OutputStream)v3).write(v4, 0, v4.length);
            ((OutputStream)v3).flush();
            ((OutputStream)v3).close();
            return v5_1;
        }
        catch(Exception ) {
            return null;
        }
    }

第一步 先解密
思路：
从fc.p1Fn读取，进行解密
解密完之后得到

此处我需要得到
byte flag 的 hash 

