import threading
from control import *
import utils
import param

class RunStatus:
    def __init__(self):
        self._is_running = False
    def set_status(self, status):
        print(f'set _is_running: {status}')
        self._is_running = status
    def get_status(self):
        print(f'get _is_running: {self._is_running}')
        return self._is_running


run_status = RunStatus()
task_ctrls = {}
index = 0
lock = threading.Lock()


def start_script(mode, type):
    global index

    if run_status.get_status():
        print('[ERROR] 脚本不支持并发运行')
        return
    run_status.set_status(True)

    lock.acquire()

    ctrl = Control(param.process_name)
    task_ctrls[index] = ctrl
    type_handle = __import__(f"musical_{type}")

    print(f'[{mode}模式] 开始【{type}】演奏')

    @utils.new_thread
    def loop_thread_func(index):
        try:
            loop_script_body(ctrl, mode, type)
            print(f'[{mode}模式] 完成【{type}】演奏')
        except OperationInterrupt:
            print(f'[{mode}模式] 中止【{type}】演奏')
            del task_ctrls[index]
        except Exception as e:
            print(e)
            raise

    @utils.new_thread
    def scan_thread_func(index):
        getattr(type_handle, 'start')(ctrl)
        del task_ctrls[index]

    if mode == '循环':
        loop_thread_func(index)
    else:
        scan_thread_func(index)

    index += 1
    lock.release()


def stop_script():
    print('尝试中止所有演奏操作')
    for ctrl in task_ctrls.values():
        ctrl.interrupt()
    for type in param.instrument_types:
        getattr(__import__(f"musical_{type}"), 'stop')()
    up_all_key()
    run_status.set_status(False)


# 避免 循环-通用 功能中 退出乐器后，由于一直按着某些按键导致的卡流程。
def up_all_key(ctrl=None):
    if ctrl is None:
        ctrl = Control(param.process_name)

    instrument_params = param.get_instrument_params()
    for key in list(instrument_params.map_top.values()) + list(instrument_params.map_middle.values()) + list(instrument_params.map_bottom.values()):
        ctrl.keyup(key)


def loop_script_body(ctrl, mode, type):
    c = ctrl
    type_handle = __import__(f"musical_{type}")

    while run_status.get_status():
        # 长按E 开始演奏 (可能会有bug，多重复几次吧)
        while not utils.find_music_book():
            c.keypress(param.interaction_key, 2)
            c.delay(1)
        c.delay(1)

        # 演奏几次
        times = 2
        for i in range(times):
            # 打开 曲艺手册
            # c.moveto(1818, 356)
            c.moveto(int(1818 * param.scale_x), int(356 * param.scale_y))
            c.delay(0.1)
            c.left_click()
            c.delay(1)

            # 曲艺手册 翻到最后
            # c.moveto(996, 710)
            c.moveto(int(996 * param.scale_x), int(710 * param.scale_y))
            c.delay(0.5)
            c.mouse_wheel(-int(3000 * param.scale_y))
            c.delay(1)

            # 选择 《专家-天选》，锣选择 《专家-Unchained》
            if type == "锣":
                # c.moveto(1350, 710)
                c.moveto(int(1350 * param.scale_x), int(710 * param.scale_y))
            else:
                # c.moveto(996, 710)
                c.moveto(int(996 * param.scale_x), int(710 * param.scale_y))
            c.delay(0.1)
            c.left_click()

            # 点击 开始演奏
            # c.moveto(1689, 943)
            c.moveto(int(1689 * param.scale_x), int(943 * param.scale_y))
            c.delay(0.1)
            c.left_click()

            # 演奏 并 等待演奏完成
            utils.new_thread(getattr(type_handle, 'start'))(ctrl)
            # 乐曲时长
            if type == "锣":
                c.delay(3 * 60 + 7)
            else:
                c.delay(3 * 60 + 24)
            c.delay(6)
            getattr(type_handle, 'stop')()

            # 确认获取熟练度窗口，有时会出两次
            c.keypress(' ')
            c.delay(2)
            c.keypress(' ')
            c.delay(2)

            if type == '通用':
                up_all_key(c)

        # 按esc起身
        c.keypress('\x1b')
        c.delay(2)
        # 确认获取熟练度窗口，有时这里也会出现
        c.keypress(' ')
        c.delay(2)

        # 大跳一下 (为了屏幕中显示 E 键)
        c.keypress(' ', 2)
        c.delay(0.5)