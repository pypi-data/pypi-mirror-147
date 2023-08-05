import random
import string


def rand_tel():
    """随机生成中国大陆11位手机号"""
    return str(random.randint(13000000000, 19999999999))


def rand_code(n=4):
    """随机生成n位英文数字验证码"""
    return "".join(random.choice(string.digits + string.ascii_letters) for i in range(n))


if __name__ == '__main__':
    print(rand_tel())
    print(rand_code(10))
