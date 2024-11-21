import config

# 进程名称
process_name = "NarakaBladepoint.exe"

# 每秒截取最大帧数
fps = 20

# 全部乐器
instrument_types = ['古筝', '通用', '疆鼓', '梆子', '锣']

# 自定义分辨率缩放
DEFAULT_RESOLUTION = (1920, 1080)
resolution = config.resolution
scale_x = resolution[0] / DEFAULT_RESOLUTION[0]
scale_y = resolution[1] / DEFAULT_RESOLUTION[1]


class DictToClass:
    def __init__(self, dictionary):
        # 将字典的每个键值对作为属性赋值给类实例
        self.__dict__ = dictionary

    def __getattr__(self, name):
        # 允许通过属性访问字典中的项
        if name in self.__dict__:
            return self.__dict__[name]
        raise AttributeError(f"'{self.__class__.__name__}' object has no attribute '{name}'")


def get_instrument_params(instrument_type='通用'):
    instrument_params = {}
    x = 538 + 120
    width = 28
    height = 23

    instrument_params['map_top'] = {1: 'Q', 2: 'W', 3: 'E', 4: 'R', 5: 'T', 6: 'Y', 7: 'U'}
    instrument_params['map_middle'] = {1: 'A', 2: 'S', 3: 'D', 4: 'F', 5: 'G', 6: 'H', 7: 'J'}
    instrument_params['map_bottom'] = {1: 'Z', 2: 'X', 3: 'C', 4: 'V', 5: 'B', 6: 'N', 7: 'M'}

    if instrument_type == "梆子":
        width -= 5
        instrument_params['key_top'] = 'D'
        instrument_params['key_middle'] = 'G'
        instrument_params['key_bottom'] = 'J'
    elif instrument_type == "疆鼓":
        width -= 10
        instrument_params['key_line1'] = 'D'
        instrument_params['key_line2'] = 'F'
        instrument_params['key_line3'] = 'H'
        instrument_params['key_line4'] = 'J'

        instrument_params['args_line1'] = (
        int(x * scale_x), int(128 * scale_y), int(width * scale_x), int(height * scale_y), 'top')
        instrument_params['args_line2'] = (
        int(x * scale_x), int(202 * scale_y), int(width * scale_x), int(height * scale_y), 'middle')
        instrument_params['args_line3'] = (
        int(x * scale_x), int(276 * scale_y), int(width * scale_x), int(height * scale_y), 'bottom')
        instrument_params['args_line4'] = (
        int(x * scale_x), int(348 * scale_y), int(width * scale_x), int(height * scale_y), 'bottom')

    elif instrument_type == "锣":
        x -= 10
        width += 10
        instrument_params['map_top'] = {9: 'E', 10: 'R', 11: 'T', 12: 'Y', 13: 'U'}
        instrument_params['map_middle'] = {5: 'D', 6: 'F', 7: 'H', 8: 'J'}
        instrument_params['map_bottom'] = {1: 'C', 2: 'V', 3: 'N', 4: 'M'}

    instrument_params['args_top'] = (
    int(x * scale_x), int(145 * scale_y), int(width * scale_x), int(height * scale_y), 'top')
    instrument_params['args_middle'] = (
    int(x * scale_x), int(240 * scale_y), int(width * scale_x), int(height * scale_y), 'middle')
    instrument_params['args_bottom'] = (
    int(x * scale_x), int(335 * scale_y), int(width * scale_x), int(height * scale_y), 'bottom')

    # 用于判断/计算长按按键相关
    long_width = 1000
    long_height = 56
    instrument_params['long_top'] = (x, 135, long_width, long_height)
    instrument_params['long_middle'] = (x, 232, long_width, long_height)
    instrument_params['long_bottom'] = (x, 327, long_width, long_height)

    return DictToClass(instrument_params)
