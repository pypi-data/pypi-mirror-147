import base64
import os

from Crypto import Random
from Crypto.Cipher import PKCS1_v1_5 as Cipher_pkcs1_v1_5
from Crypto.PublicKey import RSA

# 伪随机数生成器
random_generator = Random.new().read
# rsa算法生成实例
rsa = RSA.generate(1024, random_generator)
path = os.path.dirname(os.path.abspath(__file__))
print(path)


def encrypt(message, pub_rsa_path='chanjetrskey.py'):
    '''使用公钥加密'''

    def pre_process(msg):
        # base64.b64encode(cipher.encrypt(message[:100].encode()))
        return base64.b64encode(cipher.encrypt(msg.encode()))

    rsa_path = os.path.join(path, pub_rsa_path)
    with open(rsa_path) as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        # 长字符串加密报错解决
        if message:
            if len(message) > 100:
                cipher_text = pre_process(message[:100]) + pre_process(message[100:])
            else:
                cipher_text = pre_process(message)
        else:
            cipher_text = None
        return str(cipher_text, encoding='utf-8')


def decrypt(secret_message, rsa_path='chanjetrs.py'):
    '''使用私钥解密'''

    def pre_process(msg):
        # cipher.decrypt(base64.b64decode(secret_message[:174]), random_generator)
        return cipher.decrypt(base64.b64decode(msg), random_generator)

    rsas_path = os.path.join(path, rsa_path)
    print(rsas_path)
    with open(rsas_path) as f:
        key = f.read()
        rsakey = RSA.importKey(key)
        cipher = Cipher_pkcs1_v1_5.new(rsakey)
        if secret_message:
            if len(secret_message) > 172:
                text = pre_process(secret_message[:172]) + pre_process(secret_message[172:])
            else:
                text = pre_process(secret_message)
            return text.decode('utf-8')
        else:
            return None


if __name__ == '__main__':
    passw = "GafVgKkl7Rqkgu0Ra+tee6jDkj+1peE5wEALqQNhY+fAIJjv/4VShH5nwjCSwxrSoWBgPbQQickA/dK49pbuKyQt+TcwJ6BU6CP/ypNrNQRCYbaKhFCm1GM6Aw/ArKZIEdPfRh2dmUN/yO7/AadGrt4Ri63yGfXOmY5LY7aUows="

    ret = decrypt(passw)

    print(ret)
