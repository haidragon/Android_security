# 别人家的 fuzz 思路
1. hourglass fuzz
TODO 去看
[HITB]hook 住一个函数，然后添加一个大循环去变异,特别是你发现，某一个函数的 fuzz 过程不饱和，而且与上下文联系也不大，并且通过代码审计已经确定哪些东西是可控的。
ref https://conference.hitb.org/hitbsecconf2019ams/materials/