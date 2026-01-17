import functools

"""

人生若只如初见
何事秋风悲画扇
等闲变却故人心
却道故人心易变
骊山语罢清宵半
泪雨霖铃终不怨
何如薄幸锦衣郎
比翼连枝当日愿

select * from sc.user where user_name='xinbo.zhang'

""".strip()


@functools.lru_cache
def fibonacci(n):
    ##########################################################
    """
    :param n:
    :return:
    """
    #########################################################
    if n <= 1:
        return n
    else:
        return fibonacci(n - 1) + fibonacci(n - 2)


if __name__ == '__main__':
    char = 26 * 2
    num = 10
    s = 18

    r = (char + num + s) ** 10
    print(1 / r, r)










































    

    a = 78877888888888888
