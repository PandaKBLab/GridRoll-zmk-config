# 调整、Studio 与开发维护

## 键位

`config/gridroll.keymap` 是源码默认值。每层都按全局行优先排列：前三行各 12 键，底行 11 键，省略列 8 的空位。底行旋钮按压只占全局列 3。修改默认键位后提交即可触发 Actions。

键盘已在 Studio 保存键位时，正常 UF2 更新会继续使用保存值。优先在 Studio 中修改并保存；要重新采用源码默认值，使用 Studio 提供的恢复默认操作，或按首次烧录说明把设置清除 UF2 刷到两侧再刷回正常固件。清除操作也会清空蓝牙／DYA 设置。

八层为 Base 0、Mouse 1、Lower 2、Navigation 3、Raise 4、Scroll 5、Wireless 6、System 7，采用常规 Planck 风格。Lower + Raise 进入 System，右空格点按 Space／按住 Mouse；Lower+底行 Ctrl 位进 Navigation，Raise+左 Shift 位进 Wireless，Mouse+M 或 Lower+右空格进 Scroll。图表见[keymap.md](keymap.md)，用 `python scripts/keymap_docs.py` 更新。普通更新保留旧键位，采用新默认值前先导出旧布局，再用 Studio 恢复默认。

## DYA Studio 与轨迹球

用桌面 Chrome／Edge 打开 [DYA Studio](https://studio.dya.cormoran.works/) 或 [ZMK Studio](https://zmk.studio/)，右侧通过 USB 连接，选择 USB 输出及 GridRoll 串口。Studio 默认无锁，不需要按键解锁，也不因空闲或断连重新上锁；网页首次串口授权仍由用户选择。旧布局里的 studio_unlock 行为保留以兼容已保存键位，但不再是编辑的前提。

后续固件默认 `CONFIG_ZMK_STUDIO_LOCKING=n`。仓库 AGENTS.md 和最终编译配置检查共同固定该要求；只有用户明确要求时才恢复编辑锁。DYA 与标准 ZMK Studio 共用基础键位协议；DYA 轨迹球扩展的字段编号、类型及样例读写由 `scripts/check_studio_protocols.py` 对固定前端快照核对，不能把源码协议检查当成已连接实物。

固件提供 mouse、scroll 两个运行时处理器；仅 Scroll 5 将球 XY 转为滚动。mouse 默认开启临时 Mouse 1，打字保护 200ms，无操作退出 1200ms。首次有效运动在保护窗口之外立即激活，不要求连续运动 200ms。拨球、离散滚轮、鼠标／修饰键释放续时，按住期间保护拖拽，普通透明打字键立即退出。固定模块的 `patches/runtime-temp-layer.patch` 修复单帧不退层、按键续时、多键拖拽和手动层归属；CI 提取实际修补函数进行主机回归测试。DYA 的自动层时间仍可调整，保存结构和协议未更改。

旋钮首层不用短暂 &msc 模拟，改为 wheel_down／wheel_up 离散行为，每个 sensor trigger 一刻度；它们通过独立 input listener 进入正常 USB／BLE 指针输出。DYA cormoran_rsr 仍可按层修改。若存在旧保存值，在 DYA 将 Base CW=wheel down、CCW=wheel up，并将 mouse Temp-layer enabled / layer 1 / activation 200 / deactivation 1200 后保存；仅恢复 Studio 键位不会清掉这些参数，也无需清配对。

GridRoll 的 PAW3222 安装方向在驱动输出时固定校正为 `X=-rawY`、`Y=rawX`，先完成安装方向校正，再进入 DYA 处理器；鼠标和滚动两种模式使用相同的校正输入。该修改对应用户报告的“上→左、下→右、左→下、右→上”，新固件应使四个方向与实际拨球一致，仍需烧录后实测。若之前在 DYA 手动补偿过方向，请将 mouse 和 scroll 的额外旋转恢复为 0、X/Y 反向关闭并保存，避免重复补偿；可以保留已调好的速度和键位。

运行时设置有 RAM 与 Flash 两种模式。临时调参可选 Memory only；确定后 **Save All** 保存，断电后应保持。**Discard All** 重新载入已保存值，**Reset All** 恢复固件中的处理器默认值并保存。没有相应按钮或接口时，可打开上游 [Runtime input processor 页面](https://cormoran.github.io/zmk-module-runtime-input-processor/) 直接通过 USB 调整；避免两个页面同时占用串口。

上游 DYA 页面可能展示其他型号的功能。本版提供键位编辑和两个处理器的运行时调参；没有定义电池采样、原始传感器图像、传感器硬件 CPI RPC 或额外硬件，不应把这些项目当成已经支持。

惯性默认关闭，自动鼠标层默认开启。保留已调好的速度、方向和配对；旧 DYA 保存参数覆盖源码默认值时按上面的字段单独修改。退出时间指鼠标活动结束后的 1200ms；普通打字键会提前退出，手动按住鼠标层时不由自动控制器关层。

## 蓝牙轨迹球报告与延迟

蓝牙输出时，驱动保留每次传感器读取的位移，但将它们合并为间隔至少 8ms 的输入帧，避免每次 MOTION 中断都占用一个 BLE HID 报告。第一帧在距离上一帧已满 8ms 时立即发出；停球后的一次性定时任务会发完剩余位移。没有待发位移时不运行周期报告定时器。USB 输出绕过此间隔，方向校正、DYA 鼠标／滚动处理器和键位保持原定义。

右侧请求主机连接间隔为 6×1.25ms=7.5ms、peripheral latency=0；Studio 的蓝牙偏好延迟也为 0，避免开启 Studio 时重新请求较大延迟。电脑可能拒绝或调整这些参数，不能把配置值当成实测报告率或端到端延迟。左右分体连接的省电参数未调整。零外设延迟可能增加右侧蓝牙连接待机电流，深睡仍为 15 分钟，需重新测量实际功耗。

复测时先关闭持续使用的 Studio／DYA 页面，并用同一电脑比较 USB 输出、USB 供电且选择 BLE 输出、两侧纯电池 BLE 输出。确认连续移动没有拖尾、停球立即停止、短距离微调和 Scroll 层滚动正常；再测试按键同时输入、断电重连及深睡唤醒。如果只有纯电池模式卡顿，再测电源稳定性；如果两种 BLE 模式都卡顿，继续核查实际协商间隔、主机蓝牙适配器和射频环境。普通更新保留绑定，本次不要求清空设置。

## 低功耗、深睡与唤醒

默认空闲超时为 30 秒，电池模式的深睡超时为 15 分钟。空闲保留蓝牙连接；深睡断开连接并在按键唤醒后重新启动。左右均保留矩阵 wakeup-source；两侧都已深睡时，分别按两侧按键，不保证单独唤醒一侧能通过蓝牙唤醒另一侧。

右侧轨迹球正常待机采用 MOTION 中断，没有固定周期的无运动轮询；只有中断后的运动处理或故障恢复才重新调度。传感器保留已有的内部休眠设置。不将轨迹球或旋钮旋转声明为深睡唤醒源。

所固定版本的 ZMK 在检测到 USB 供电时不进入定时深睡，便于 USB 和 Studio 使用。Studio 编辑前选择 USB 输出，编辑后保存。电池深睡会清空 RAM 中未保存的编辑；普通 UF2 更新和睡眠不会主动清除 Flash 中保存的配对、键位或 DYA 参数。

编译会检查两侧的休眠开关、超时和矩阵唤醒声明；仍须在实物分别验证电池空闲电流、15 分钟深睡电流、两侧按键唤醒、蓝牙重新连接、USB Studio 持续连接和断电后的设置保留。未测量前不报告具体续航或休眠电流。

## 旋钮校准

左侧 `gridroll.dtsi` 的 `steps` 描述驱动每圈原始步数，`triggers-per-rotation` 描述每圈期望行为事件数；两者初始为 20。先缓慢转一整圈再快速转一整圈，记录各自事件数，目标 16–40，无反向／漏报／重复。

实际编码器的脉冲与卡点规格可能不同；按测得原始步数调整 steps，再调整事件数。不要只凭 EC11 名称判断。方向反了可交换 A/B 配置或该层 sensor-bindings 的顺序，避免改动已经确认的 PCB 接线。按压以矩阵 `RC(3,3)` 测一次，不另加 GPIO 按压行为。

## 蓝牙与输出

右侧与电脑配对，左侧仅与右侧连接。Lower + Raise 进入 System，Q–T 选槽 0–4、Backspace 清当前槽、Y 选 USB、U 选 BLE、I 切换。新 USB 枚举和启动加载设置后优先 USB，纯充电不强制切换，拔线回退已连接的 BLE；插线后手动 BLE 选择保持到下一次重新接入。此策略无周期轮询，保留现有绑定。

正常应用的键盘名称、蓝牙广播名称和右侧 USB 产品名称均固定默认值为 **GridRoll**；构建脚本检查最终 `.config`，防止配置未实际生效。右侧显式启用 USB／BLE，并关闭 2M PHY 以保持与常见主机的兼容性。原有 `ZMK_BLE_EXPERIMENTAL_CONN` 已间接关闭 2M，本次将该要求写明，不把它当成已经查明的故障原因。普通更新仍保留配对关系，不在每次开机时清除绑定。

搜不到蓝牙时，先按以下顺序检查：

1. 确认右侧安装的是本次成功构建的 `GridRoll-right.uf2` 或诊断版，左侧安装 `GridRoll-left.uf2`；`GridRoll-settings-reset.uf2` 不广播键盘，必须换回正常固件。电脑只与右侧配对，左侧不会作为第二个主机键盘使用。
2. 默认 Lower + Raise 进入 System，顶行 Q 选槽 0、Backspace 清该槽、U 选 BLE。也可 Raise + 左 Shift 位进入 Wireless 选择槽。先试未配对的槽可保留旧绑定。保存过的布局请按实际位置操作。
3. 在电脑或手机中“忽略／删除”旧设备，暂时关闭旧主机的蓝牙，给右侧重新上电，然后添加蓝牙设备并搜索 **GridRoll**。已连接其他主机的当前槽可能停止广播；改名和普通 UF2 更新也不会自动清掉旧绑定或主机缓存。
4. DYA／Studio 保存过自定义键位时，上述位置可能已有变化；先在右侧 USB Studio 中查看实际的蓝牙槽、BT_CLR 和 BLE 输出键，再操作。不要假设重新刷普通 UF2 会覆盖已保存键位。
5. 仍搜不到时，先只给右侧正常应用供电，用手机和电脑分别搜索。安装 `GridRoll-right-diagnostics.uf2` 并通过 SWD／RTT 查看 Bluetooth 初始化和 advertising 错误。两台设备均不可见而 USB 正常时，需要这些实物日志才能区分无线供电、射频和初始化问题，不能仅凭配置认定蓝牙已修复。

最后才考虑按首次烧录说明将设置清除 UF2 刷入两侧，再分别刷回正常固件。此操作会清除两侧蓝牙、Studio 和 DYA 设置，执行前先记录需要保留的键位和参数。

官方参考：[蓝牙配置与主机槽](https://zmk.dev/docs/features/bluetooth)、[连接问题与恢复](https://zmk.dev/docs/troubleshooting/connection-issues)。

分体重连失败时，先确认两侧文件和电源，再同时清除两侧设置；主机也删除旧的 GridRoll 配对。不要只清一侧后长期混用旧绑定。

## 诊断

标准 Actions 下载只有一个 GridRoll-firmware 包，且仅包含左手、右手和 settings-reset 三个 UF2；不包含诊断固件、启动程序、HEX、日志或配置文件。

需要诊断时，可从源码单独构建 `GridRoll-right-diagnostics.uf2`。它保留正常功能和 Studio，通过 SEGGER RTT 输出传感器日志。接 SWD 探针，用 RTT 客户端查看启动 ID、初始化 CPI 及总线错误；日志不与 Studio USB 串口混用。无传感器／探测失败时仅停止轨迹球，键盘与分体应继续工作。

GPIO 总线采用 mode 3、MSB 优先，默认半周期 5µs、读转向等待 100µs、事务间隔 50µs，均可在右侧传感器节点中调整。读取前 SDIO 转为输入；所有 GPIO 失败路径均尝试 CS 释放、SCLK 恢复高、SDIO 释放。初始化最多 3 次尝试；运行错误最多 3 次快速重试，随后降至 1Hz，避免持续占用工作队列。

输入队列暂时满时，轨迹球报告按 2、4、8、16、32ms 的有界退避重试，新传感器输入也须遵守同一截止时间，避免高频中断绕过重试限制。已经成功进入队列的 X 不重复发送，Y 同步帧和剩余位移保留。运动中断不会提前覆盖已有的采样／故障恢复计划，防止噪声触发快速重试。无待发位移时不周期重试。

实际波形、模式／时序余量和轨迹球方向须在实物验证。诊断固件也没有改为上游的共享 MOSI/MISO SPI 实现。

## 固定依赖与兼容处理

`config/west.yml` 固定 ZMK custom-studio 分支、Zephyr 4.1 修复版和两个 DYA 模块的完整提交 SHA，传递依赖由这些固定 manifest 决定；构建过程生成的 `west-frozen.yml` 不进入标准下载包。Python 工具锁定于 `ci/requirements.lock`。固件构建镜像固定 digest；启动程序固定 Adafruit 0.11.0 SHA、Git 子模块 SHA 和 Arm GNU 12.3.rel1 下载 SHA256。

右侧使用完整 Newlib 数学库、GNU 静态初始化及较大的输入／RPC 线程栈：Studio RPC 6144B、低优先级工作线程 4096B、系统工作队列 4096B。本地模块为所固定的上游 Studio C 源码补充 stdio 声明，并提供 Arm GNU 14 Newlib 所需的弱 `_fini` 结束钩子，不编辑下载依赖。CI 输出实际 FLASH／RAM 使用量，避免仅加栈而不检查容量。固件编译使用镜像内固定的 Python 工具集；`ci/requirements.lock` 用于启动程序和本地环境。

升级时一次只改一组依赖，检查完整 Actions、47 键、Studio 无需解锁即可编辑／保存、DYA 参数保存、分体重连和供电。不要把 revision 改成 main 来绕过失败。

## 本地构建

需要 Zephyr 4.1 兼容 SDK、Python 3.12+、CMake、Ninja、Git。仓库本身是模块，应把依赖工作区放在仓库外：

```sh
python3 -m venv ../gridroll-tools
. ../gridroll-tools/bin/activate
pip install -r ci/requirements.lock
mkdir -p ../gridroll-workspace/config
cp config/west.yml ../gridroll-workspace/config/west.yml
west init -l ../gridroll-workspace/config
cd ../gridroll-workspace
west update --narrow --fetch-opt=--filter=blob:none
cd ../GridRoll
python scripts/check_hardware.py
cc -Wall -Wextra -Werror -std=c11 -Idrivers/input tests/test_sdio.c drivers/input/paw3222_sdio.c -o /tmp/gridroll-test-sdio
/tmp/gridroll-test-sdio
python scripts/build_firmware.py --workspace ../gridroll-workspace --out artifacts
```

使用官方 Arm GNU 代替 Zephyr SDK 时，设 `ZEPHYR_TOOLCHAIN_VARIANT=gnuarmemb` 和 `GNUARMEMB_TOOLCHAIN_PATH=实际工具链目录`，不要用缺少 libc 能力声明的 cross-compile 模式构建 DYA。

启动程序：按 `bootloader/upstream.json` 克隆并检出固定 SHA，初始化子模块；执行 `python scripts/build_bootloader.py --source 启动程序目录 --out artifacts`。脚本会验证 SHA、安装 GridRoll 板定义，并构建两种上游基准板。

## 产品化前

使用正式分配的产品标识后，重新构建并测试 UF2／SWD 恢复、配对与 Studio 连接。电池百分比监测目前未启用，不将缺失的电量报告误判为蓝牙功能失效。真实验收记录保存在 validation 文档中；本仓库不保存内部电路文档。
