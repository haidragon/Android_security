# Android8.0 硬件抽象层
## 硬件抽象层
ref:https://source.android.com/devices/architecture/hal-types

始于Linux内核开源协议和第三方厂商隐私安全的矛盾，为了绕过之一矛盾，Google构建了HAL，通过他在遵守Linux协议，同时保护第三方厂商的利益。
	'''
	Camera HAL
	Audio HAL
	Graphics HAL
	Other HALs
	'''
* 绑定式 HAL
	以HAL接口定义语言（HIDL）表示的HAL。这些HAL取代了早期Android版本中使用的传统HAL和旧版HAL。在绑定式HAL中，Android框架和HAL之间通过Binder进程间调用进行通信。所有在推出时即搭载了Android8.0或更高版本的设备都必须只支持绑定式HAL。
* 直通式 HAL
	以HIDL封装的传统HAL或旧版HAL。这些HAL封装了现有的HAL，可在绑定模式和SamProcess模式下使用。升级到Android8.0的设备可以使用直通式HAL

	
## Project Treble

Android 8.0 推出了Project Treble，最大的变化之一是 HAL binderized

ref:https://source.android.com/devices/architecture/treble

Treble 适用于 搭载Android8.0及后续版本的所有新设备。

利用新的供应商接口，Project Treble将供应商实现与Android操作系统框架分离开来。
Android 7.x 及更早版本中没有正式的供应商接口，因此设备制造商必须更新大量 Android 代码才能将设备更新到新版 Android 系统。

Treble 提供了一个稳定的新供应商接口，供设备制造商访问Android代码中特定于硬件的部分，这样一来，设备制造商只需更新 Android 操作系统框架，即可跳过芯片制造商直接提供新的 Android 版本。