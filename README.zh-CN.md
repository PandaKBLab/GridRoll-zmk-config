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

默认采用 Planck 风格：按住 **Lower + Raise** 进入 System，顶行 Q 选槽 0、Backspace 清除该槽、Y 选 USB、U 选 BLE。右侧 USB 被电脑成功识别后自动优先有线，拔线后回退已连接的蓝牙主机；充电器不强制切换，插线期间仍可手动选蓝牙。保存过的布局可能不同。

使用 [ZMK Studio](https://zmk.studio/) 或 [DYA Studio](https://studio.dya.cormoran.works/) 时，将**右侧通过 USB** 连接电脑，选择 USB 输出及对应串口。**Studio 默认保持解锁，无需按解锁键，空闲或断开连接后也不会重新锁定。** 关闭占用同一串口的其他网页，编辑后保存。更新会保留 Studio／DYA 设置。以前在 DYA 手动补偿过轨迹球旋转时，应取消额外补偿：安装方向校正在鼠标和滚动处理器之前执行。

两个界面均支持键位编辑，DYA 还可调整 mouse／scroll 参数及**每层旋钮顺时针／逆时针行为**。首层旋钮默认模拟鼠标滚轮：顺时针向下、逆时针向上。CI 核对三个固定 DYA 扩展协议和最终无锁配置；不包含未实现的传感器图像等硬件功能。

## 八层默认键位

默认采用常规 **Planck QWERTY／Lower／Raise**，适配 GridRoll 的 47 键，保留 Mouse、Navigation、Scroll、Wireless、System 共八层。Tab、Esc、Shift、标点、Enter 为普通按键；Lower + Raise 进入 System。删除上一版 LiNEA40 打字组合键。[查看全部键位图、准确键值、进入方式和旋钮定义](docs/keymap.md)。英文首页展示八张图，CI 核对图表和源码一致。

## 自动鼠标层与旋钮

- 有效拨球立即进入 Mouse；最近 **200ms** 内按过键时暂不触发，避免打字误碰。200ms 是打字保护，不是必须连续滚球的时间。
- 最后一次拨球、旋钮滚轮或鼠标／修饰键释放后 **1200ms** 退出。按住一个或多个鼠标键／修饰键时不超时，保护拖拽；普通透明打字键立即退出，Esc 回基础层。
- **J 左键、K 右键、H 中键、L 后退、分号前进；U/I 上下滚轮，O/P 横向滚轮。** 按住 M 把轨迹球转成滚动。右空格点按为空格、按住为手动鼠标层。
- 首层旋钮改为每个传感器事件直接发送一个滚轮刻度：顺时针下滚、逆时针上滚。上一版 20ms 短按在 10 刻度／秒下可能取整为零，这次不再使用该定时模拟。
- **DYA 参数与 Studio 键位独立保存。** 旧值仍在时，请把 mouse 的临时层设为启用、目标层 1、激活保护 200ms、退出 1200ms，并把首层旋钮 CW 选 wheel down、CCW 选 wheel up 后保存。仅恢复 Studio 默认键位不会清除旧的处理器和旋钮参数；无需刷 reset。

**普通更新保留 Studio 已保存的键位。** 采用本版默认值前先导出旧布局，再在 Studio 恢复默认；无需刷 reset 清除配对。符号使用常规 US 键码，实际字符取决于电脑输入布局。

## 低功耗与唤醒

- 无输入 **30 秒**后进入空闲，保持蓝牙可用。
- 电池供电、无输入 **15 分钟**后进入深睡。分别按一下每个已休眠半边的按键，等待蓝牙恢复。不保证拨球或旋转编码器能从深睡唤醒。
- USB 供电的半边保持唤醒，便于 USB／Studio 使用。电池深睡前应保存 Studio 修改，RAM 中未保存内容会丢失。
- 轨迹球采用 MOTION 中断和既有传感器休眠设置。整机电流及唤醒可靠性仍需实测。
- 蓝牙轨迹球将位移合并为间隔至少 **8ms** 的报告，保留总位移；USB 仍即时输出。右侧请求 **7.5ms** 主机连接间隔及零外设延迟，实际参数由主机决定；蓝牙连接待机耗电可能增加。流畅度和功耗仍待实物复测。

更多内容见[维护说明](docs/maintenance.md)、[固件兼容性](docs/hardware.md)和[验证状态](docs/validation.md)。依赖版本固定于 config/west.yml。原创代码采用 MIT 许可，依赖许可见[第三方声明](THIRD_PARTY_NOTICES.md)。
