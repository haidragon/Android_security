# 漏洞信息来源

## 漏洞信息来源

* RSS、相关博文 【RSS订阅】TODO 推送吧

## 漏洞研究风向标

* 华米星OVG、Android安全公告

* TODO:

## 安全会议

* BlackHat

> https://www.blackhat.com
> USA是主会场，议题质量和数量也是最高的，议题类型覆盖面也很广，除此之外还有欧洲和亚洲等分会场，质量相对次一些。
> 这次BlackHat USA的议题也陆续公开了：https://www.blackhat.com/us-19/briefings/schedule/index.html

* OffensiveCon

> https://www.offensivecon.org/
> OffensiveCon是从2018年才开始举办的，但议题质量一直保持不错，演讲者中包括Project Zero、Google syzkaller作者、Pwn2Own与Hack2Win获奖者等等。
> 会后，一般是由演讲者选择是否公开ppt，多数人是在Twitter上公开的，官网上我没找到资源（https://github.com/riusksk/SecConArchive/tree/master/OffensiveCon2019），所以之前收集的ppt都是从twitter上扒下来的。

* HITB (Hack In The Box)

> https://conference.hitb.org/
> 这几天HITB刚在荷兰阿姆斯特丹举办完，议题PPT也一并公开(https://conference.hitb.org/hitbsecconf2019ams/materials/)。
> 如果要说国内外安全会议中，哪个公开PPT最快的，一定是HITB，他们一般是现场演讲完，就直接扔官网下载。然后过一段时间，也同样发布演讲视频。
> 他们有时会同时搞两个演讲会场，一个是收费的主会场，议题质量高一些，一个是免费的，叫CommSec，用来提携新人，议题质量相对比较次，每个议题分享时间也比较短，最多半小时。
> 之前去新加坡参加过一次HITB，人数不多，场地也不大，但可以感受到与国内安全会议的区别：更注重技术交流，而非搞关系。
> 2018年开始，HITB也开始与京东合作，在北京举办分会场，没去过，不作评价，但国际会议本土化，总会产生一些差异的。

* InfiltrateCon

> https://infiltratecon.com
>从2011年开始举办的，已经走过8个年头。
>看了今年的议题，还是有干货的，但只有4个议题ppt在twitter上公开。
>以前，会后都会在官网上公开PPT和视频，但目前官方还没公开。
>今年的议题涉及Chrome RCE、iOS与Android提权、Pwn TEE、浏览器JS Fuzzing等等，只能坐等官方公开PPT了。

* Chaos Communication Congress(C3)

> https://www.ccc.de/
> 德国混淆黑客大会，常叫C3会议，常在C3前面加上第几届，比如今年第35届，所以叫35C3，历史非常悠久。
> 以前大多是聚焦在无线电安全，所以一些什么2G\3G\4G短信、电话窃听经常出自该会议。熟悉无线电安全的同学，应该都听过。2018年也有一些不错的软件安全相关的议题，这些在之前写的文章《推荐今年C3黑客大会上的几个议题》介绍过了。
> 除了大会议题，不得不提下他们的CTF，非常具有实战价值，比如2018年的题目，直接拿pwn2own漏洞当比赛，从safari代码执行到提权，还有VisualBox沙盒逃逸题目，需要利用到0Dday，出题者是ProjectZero的人，早就将其卖给ZDI，刷了不少VBox漏洞。这些CTF题目在网上都有相应的WriteUp可供学习。
> 这些议题只有演讲视频公开，没有PPT，官方会放在https://media/ccc.de，可在线或下载观看。
> 都是在每年的12月份举办，2019的还有半年呢……

* CanSecWest

> https://cansecwest.com
> CanSecWest都是与Pwn2Own一块出现的，以前议题PPT都是放在https://www.slideshare.net/上分享，但从2018年开始又不搞了。
> 每年议题不多，但质量还是可以的，不过感觉这两年的质量略有下降。
> 今年3月的议题也没看到有下载，也是混Twitter找ppt的，只看了《vs com.apple.security.sandbox》这个议题，今年我感兴趣的议题没几个，大家根据自己喜好选择吧。
> 如果你各个议题PPT，也欢迎分享下。

* MOSEC 移动安全技术峰会

> http://mosec.org
> MOSEC是从2015年开始举办的，由盘古与韩国POC联合举办，聚集移动安全领域，包括Android、iOS、IoT以及无线电等领域。虽然起步晚，但议题干货满满的，应该是目前国内最好的安全会议了。
> 今年的议题也已经陆续公开了，包括iOS越狱、Android提权、LTE、基带、卫星系统等等。
> 官网是不公开大会的议题PPT，由演讲者选择，所以想学习的同学，可能还是得去参会。

* POC

> http://powerofcommunity.net/
> POC(PowerOfCommunity)起始于2006年，在韩国举办的。单从议题质量看，确实不错，大多漏洞研究领域的前沿技术，但它经常是"二手货"，也就是在其它安全会议讲过后，但去韩国观光旅游顺便讲下。
> 还有个意思的现象就是，每年的议题超过一半是中国人讲的。
> 所以，你推荐也对，你不推荐也没错。
> 不过，有个好处就是，POC议题PPT都是提供下载的。有时在其它会议找不到PPT时，到POC官网翻下，偶有小惊喜。
> 另外还有个会议叫ZeroNights，同一举办方，更多是面向老外的。

## 研究者团队、社区

* Dianne Hackborn
	Google资深大牛
	> https://www.jianshu.com/p/07b87084337f
	> 关于Android四大组件深刻解读
* Twttier （ ）TODO:

* 漏洞赏金计划、私有市场 每个国家都有
    * TODO:
    Hackone
        https://github.com/B3nac/Android-Reports-and-Resources
