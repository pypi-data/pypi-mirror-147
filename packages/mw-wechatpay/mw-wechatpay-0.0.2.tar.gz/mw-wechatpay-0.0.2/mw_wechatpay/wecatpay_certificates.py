from .rsa_crypt_util import decrpyt_certificate,load_cert

from .time_util import convert_timestr_to_ts

class WechatpayCertificates:
    def __init__(self,apiv3key):
        super().__init__()
        self.apiv3key = apiv3key
        self.certs = {}

    def decrpyt_wepay_data(self,nonce, ciphertext, associated_data):
        return decrpyt_certificate(self.apiv3key,nonce, ciphertext, associated_data)

    def load(self,body):
        items = body['data']
        for item in items:
            try:
                encrypt_cert = item.get('encrypt_certificate')
                certificate = self.decrpyt_wepay_data(
                                                  encrypt_cert['nonce'],
                                                  encrypt_cert['ciphertext'],
                                                  encrypt_cert['associated_data'])
                certificate=certificate.decode()

            except Exception as e:
                print('decrpyt_wepay_data:error %s' %str(e))
            else:
                self.certs[item['serial_no']]=WechatpayCertificate(
                    item['serial_no'],
                    convert_timestr_to_ts(item['effective_time']),
                    convert_timestr_to_ts(item['expire_time']),
                    certificate)


    def get_cert(self,serial_no):
        cert = self.certs.get(serial_no)
        if cert is not None:
            return cert.cert



class WechatpayCertificate:
    def __init__(self,serial_no,effective_time,expire_time,certificate):
        self.serial_no = serial_no
        self.effective_time = effective_time
        self.expire_time = expire_time
        self.certificate = certificate

        self.cert = load_cert(self.certificate.encode())


    # @classmethod
    # def load_encryptdata(cls,apiv3key,data):
    #     try:
    #         encrypt_cert = data.get('encrypt_certificate')
    #         certificate= decrpyt_certificate(apiv3key,
    #                             encrypt_cert['nonce'],
    #                             encrypt_cert['ciphertext'],
    #                             encrypt_cert['associated_data'])
    #
    #         return WechatpayCertificate(data['serial_no'],
    #                                     convert_timestr_to_ts(data['effective_time']),
    #                                     convert_timestr_to_ts(data['expire_time']),
    #                                     certificate)
    #     except Exception as e:
    #         pass


