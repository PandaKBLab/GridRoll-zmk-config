# GridRoll

[English](README.md) · **简体中文** · [日本語](README.ja.md) · [Deutsch](README.de.md)

PandaKB GridRoll 分体键盘的 ZMK 固件：47 键、左侧旋钮、右侧 PAW3222 轨迹球、USB／蓝牙，支持 ZMK Studio 和 DYA Studio。

**右侧是连接电脑的主半边（Central）**，左侧无线连接右侧。键盘、蓝牙和 USB 产品名称均为 **GridRoll**。

本仓库只包含固件、构建工具和使用说明，不分发 PCB 工程、原理图、布线、网络表及内部电路文档。固件必需的 GPIO 定义保留在板级源码中。

## 下载与烧录

1. 打开 [Build GridRoll firmware](https://github.com/PandaKBLab/GridRoll-zmk-config/actions/workflows/build.yml)，选择成功运行。
2. 只下载一个 **GridRoll-firmware** ZIP，包内仅三个文件：**GridRoll-left.uf2**、**GridRoll-right.uf2** 和 **GridRoll-settings-reset.uf2**。
3. 分别进入两侧启动程序，将 GridRoll-left.uf2 复制到左侧，GridRoll-right.uf2 复制到右侧。设置清除版不能用作正常键盘固件。
4. 没有 GridRoll 启动程序的主控需要先按[首次烧录流程](docs/first-flash.md)安装；首次包需单独构建，不包含在本下载包中。

产物保留 30 天。编译通过属于软件验证，不代表实物测试通过。

## 蓝牙与 Studio

电脑只与**右侧的 GridRoll** 配对。搜不到时，选择未使用的蓝牙槽，或清除当前槽并在电脑端删除旧配对后重试。普通更新会保留旧绑定。

默认键位下，按住**左上角 Tab** 进入 System：顶行 **Q** 选择槽 0，**Backspace** 清除该槽，**Y** 选择 USB，**U** 选择 BLE。右侧 USB 被电脑成功识别后自动切换有线，即使此前保存过蓝牙首选输出；充电器不会强制切换，拔线后回退到已连接的蓝牙主机。插线期间仍可手动选择蓝牙，下一次接入电脑时重新优先 USB。Studio 保存过的布局可能不同。

使用 [ZMK Studio](https://zmk.studio/) 或 [DYA Studio](https://studio.dya.cormoran.works/) 时，将**右侧通过 USB** 连接电脑，选择 USB 输出及对应串口。**Studio 默认保持解锁，无需按解锁键，空闲或断开连接后也不会重新锁定。** 关闭占用同一串口的其他网页，编辑后保存。更新会保留 Studio／DYA 设置。以前在 DYA 手动补偿过轨迹球旋转时，应取消额外补偿：安装方向校正在鼠标和滚动处理器之前执行。

两个界面均支持键位编辑，DYA 还可调整 mouse／scroll 参数及**每层旋钮顺时针／逆时针行为**。首层旋钮默认模拟鼠标滚轮：顺时针向下、逆时针向上。CI 核对三个固定 DYA 扩展协议和最终无锁配置；不包含未实现的传感器图像等硬件功能。

## 八层默认键位

参考 LiNEA40 七层键位，适配 GridRoll 的 47 键，并增加第八层 System，八层全部启用。[查看全部键位图、每个键的准确键值、进入方式和旋钮定义](docs/keymap.md)，英文首页也直接展示八张图。图表由源码生成，CI 核对一致性。

**普通更新保留 Studio 已保存的键位。** 采用本版默认值前先导出旧布局，再在 Studio 恢复默认；无需刷 reset 清除配对。参考方案的日文符号键码予以保留，实际字符取决于电脑输入布局。

## 低功耗与唤醒

- 无输入 **30 秒**后进入空闲，保持蓝牙可用。
- 电池供电、无输入 **15 分钟**后进入深睡。分别按一下每个已休眠半边的按键，等待蓝牙恢复。不保证拨球或旋转编码器能从深睡唤醒。
- USB 供电的半边保持唤醒，便于 USB／Studio 使用。电池深睡前应保存 Studio 修改，RAM 中未保存内容会丢失。
- 轨迹球采用 MOTION 中断和既有传感器休眠设置。整机电流及唤醒可靠性仍需实测。
- 蓝牙轨迹球将位移合并为间隔至少 **8ms** 的报告，保留总位移；USB 仍即时输出。右侧请求 **7.5ms** 主机连接间隔及零外设延迟，实际参数由主机决定；蓝牙连接待机耗电可能增加。流畅度和功耗仍待实物复测。

更多内容见[维护说明](docs/maintenance.md)、[固件兼容性](docs/hardware.md)和[验证状态](docs/validation.md)。依赖版本固定于 config/west.yml。原创代码采用 MIT 许可，依赖许可见[第三方声明](THIRD_PARTY_NOTICES.md)。
