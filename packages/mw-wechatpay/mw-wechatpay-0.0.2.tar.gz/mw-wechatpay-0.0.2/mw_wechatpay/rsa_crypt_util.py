'''敏感信息加解密https://pay.weixin.qq.com/wiki/doc/apiv3_partner/wechatpay/wechatpay4_3.shtml
开发者应当使用 微信支付平台证书中的公钥，对上送的敏感信息进行加密。
微信支付使用商户证书中的公钥对下行的敏感信息进行加密。
开发者应使用商户私钥对下行的敏感信息的密文进行解密。
'''

from Crypto.Cipher import PKCS1_OAEP
import base64
from cryptography.hazmat.primitives.ciphers.aead import AESGCM
import OpenSSL

# def load_pk_file(filename):
#     with open(filename) as f:
#         data = f.read()
#
#     return RSA.import_key(data.encode())
def load_private_key_file(filename):
    with open(filename) as f:
        prikey_data = f.read().encode()

    return load_private_key(prikey_data)

def load_private_key(prikey_data):
    return OpenSSL.crypto.load_privatekey(OpenSSL.crypto.FILETYPE_PEM, prikey_data)

def load_cert_file(filename):
    with open(filename) as f:
        cert_data = f.read().encode()

    return load_cert(cert_data)

def load_cert(cert_data):
    return OpenSSL.crypto.load_certificate(OpenSSL.crypto.FILETYPE_PEM, cert_data)


def sign_rsa_sha256(pkey,data):
    encrypt_data = OpenSSL.crypto.sign(pkey,data,'RSA-SHA256')
    return str(base64.b64encode(encrypt_data), encoding='utf-8')

def encrypt_oaep(public_key,message:str):
    '''
    开发者应当使用 微信支付平台证书中的公钥，对上送的敏感信息进行加密。
    :param public_key:
    :param message:
    :return:
    '''
    cipher_rsa =PKCS1_OAEP.new(public_key)
    encrypt_data =cipher_rsa.encrypt(message.encode())
    return str(base64.b64encode(encrypt_data), encoding='utf-8')

def decrypt_oaep(private_key,ciphertext):
    '''
    开发者应使用商户私钥对下行的敏感信息的密文进行解密。
    :param private_key:
    :param ciphertext:
    :return:
    '''
    cipher_rsa = PKCS1_OAEP.new(private_key)
    data =base64.b64decode(ciphertext)
    return cipher_rsa.decrypt(data)

def decrpyt_certificate(apiv3key,nonce, ciphertext, associated_data):
    '''
    为了保证安全性，微信支付在回调通知和平台证书下载接口中，对关键信息进行了AES-256-GCM加密。本章节详细介绍了加密报文的格式，以及如何进行解密。
    https://pay.weixin.qq.com/wiki/doc/apiv3_partner/wechatpay/wechatpay4_2.shtml
    :param nonce:
    :param ciphertext:
    :param associated_data:
    :return:
    '''
    key_bytes = str.encode(apiv3key)
    nonce_bytes = str.encode(nonce)
    ad_bytes = str.encode(associated_data)
    data = base64.b64decode(ciphertext)

    aesgcm = AESGCM(key_bytes)
    return aesgcm.decrypt(nonce_bytes, data, ad_bytes)

'''
验证签名
很多编程语言的签名验证函数支持对验签名串和签名 进行签名验证。
强烈建议商户调用该类函数，使用微信支付平台公钥对验签名串和签名进行SHA256 with RSA签名验证。
https://pay.weixin.qq.com/wiki/doc/apiv3_partner/wechatpay/wechatpay4_1.shtml
'''

def wepay_validate(cert,ts,nonce,signature,text):
    # ts = resp.headers.get('Wechatpay-Timestamp')
    # nonce = resp.headers.get('Wechatpay-Nonce')
    # signature =resp.headers.get('Wechatpay-Signature')
    # body = await resp.text()
    message = '%s\n%s\n%s\n' %(str(ts),nonce,text)
    # base64.b64decode(signature)
    return OpenSSL.crypto.verify(cert,base64.b64decode(signature),message.encode(),'SHA256')