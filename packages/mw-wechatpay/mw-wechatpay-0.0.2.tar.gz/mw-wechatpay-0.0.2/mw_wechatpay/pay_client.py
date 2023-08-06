import random
import json
import requests
import logging
from .time_util import linux_timestamp
# from .wecatpay_certificates import WechatpayCertificates
from .rsa_crypt_util import sign_rsa_sha256,wepay_validate

logger= logging.getLogger(__name__)

SYMBOLS = "0123456789abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"




WECHATPAY_DOMAIN ='https://api.mch.weixin.qq.com'

class WechatPay2Credentials:
    def __init__(self,merchant_id,private_key,serial_no):
        self.merchant_id = merchant_id
        # self.signer = signer
        self.private_key = private_key
        self.schema = "WECHATPAY2-SHA256-RSA2048"
        self.serial_no = serial_no

    def  generate_noncestr(self):
        s=''
        for i in range(len(SYMBOLS)):
            s+= SYMBOLS[int(random.random()* len(SYMBOLS))]
        return s

    def get_token(self,method,canonical_url,data):
        # message = self.build_message(method,canonical_url,data)
        body = data or ''
        method = method.upper()

        ts = linux_timestamp()
        noncestr = self.generate_noncestr()
        message = method + "\n" + \
               canonical_url + "\n" + \
               str(ts) + "\n" + \
               noncestr + "\n" + \
               body + "\n"

        # print('message:%s' % message)

        signature = self.sign_message(message)
        return 'mchid="%s",nonce_str="%s",signature="%s",timestamp="%s",serial_no="%s"'%\
               (self.merchant_id,noncestr,signature,str(ts),self.serial_no)


    def sign_message(self,message):
        return sign_rsa_sha256(self.private_key,message.encode())
        # encrypt_data = rsa.sign(message.encode(), self.private_key, 'SHA-256')
        # return str(base64.b64encode(encrypt_data), encoding='utf-8')

    def build_message(self,method,canonical_url,data):

        body =''
        method = method.upper()
        if data is not None:
            body = json.dumps(data)

        return method + "\n" +\
         canonical_url + "\n" +\
         str(linux_timestamp()) + "\n" +\
         self.generate_noncestr() + "\n" +\
         body + "\n"


    def sign_pay_data(self,package,appid):
        '''
        https://pay.weixin.qq.com/wiki/doc/apiv3/apis/chapter3_1_4.shtml
        JSAPI调起支付的参数需要按照签名规则进行签名计算：
        需要将列表中的数据签名
        :param package:
        :return:
        '''
        # 应用ID
        # 时间戳
        # 随机字符串
        # 订单详情扩展字符串
        ts = linux_timestamp()
        noncestr = self.generate_noncestr()

        message= '%s\n%s\n%s\n%s\n' %(
            appid,ts,noncestr,package
        )

        signature = self.sign_message(message)
        return {"appId": appid,
                "timeStamp": str(ts),
                "nonceStr": noncestr,
                "package": package,
                "signType": "RSA",
                "paySign": signature}


def wechat_pay_validate_resp(headers, body, cert):
    ts = headers.get('Wechatpay-Timestamp')
    nonce = headers.get('Wechatpay-Nonce')
    signature = headers.get('Wechatpay-Signature')
    data = {'ts': ts,
            'nonce': nonce,
            'signature': signature
            }
    print(data)
    try:
        wepay_validate(cert, ts, nonce, signature, body)
    except Exception as e:
        raise Exception('validate error:%s' % str(e))

class WeChatPayClient():
    def __init__(self,merchant_id,private_key,serial_no,appid,certlist=None):
        self.credentials = WechatPay2Credentials(merchant_id,private_key,serial_no)
        self.merchant_id = merchant_id
        self.appid = appid

        self.certlist=certlist


    def decrypt_wepay_data(self,nonce, ciphertext, associated_data):
        if self.certlist is None:
            raise Exception('not set certlist')

        return self.certlist.decrpyt_wepay_data(nonce, ciphertext, associated_data)

    def validate_wepay_data(self,headers,text):
        if self.certlist is not None:
            serial_no = headers.get('Wechatpay-Serial')
            if serial_no is None:
                raise Exception('resp has not serial no')
            cert = self.certlist.get_cert(serial_no)

            #lazy load
            if cert is None:
                self.get_certificates_with_decrypt()
            else:
                # 验证签名

                wechat_pay_validate_resp(headers, text,cert)
        else:
            raise Exception('not set certlist')


    def get_certificates_with_decrypt(self):
        resp = self.get_certificates()
        if self.certlist is None:
            raise Exception('')
        serial_no = resp.headers.get('Wechatpay-Serial')
        cert = self.certlist.get_cert(serial_no)
        if cert is not None:
            # 解密数据
            body = resp.json()
            self.certlist.load(body)




    def get_certificates(self):
        '''
        获取平台证书
        https://pay.weixin.qq.com/wiki/doc/apiv3/apis/wechatpay5_1.shtml
        :param apiv3key:
        :return:
        '''
        # pay_certs=WechatpayCertificates(apiv3key)
        return self.request('GET','/v3/certificates')



    def post_jsapi(self,payer_openid ,out_trade_no,description,total,currency='CNY',notify_url=''):
        data = {
            "mchid": self.merchant_id,
            "out_trade_no": out_trade_no,
            "appid": self.appid,
            "description": description,
            "notify_url": notify_url,
            "amount": {
                "total": total,
                "currency": currency
            },
            "payer": {
                "openid": payer_openid
            }
        }
        return self.request('POST','/v3/pay/transactions/jsapi',data)

    def get_transactions_transaction_id(self,transaction_id):
        '''
        微信支付订单号查询
        :param transaction_id:
        :return:
        '''
        url = '/v3/pay/transactions/id/{transaction_id}?mchid={mchid}'.format(
            transaction_id= transaction_id,
        mchid = self.merchant_id)
        return self.request('GET',url)

    def get_transactions_outtrade_no(self,out_trade_no):
        '''
                商户订单号查询
                :param out_trade_no:
                :return:
                '''
        url = '/v3/pay/transactions/out-trade-no/{out_trade_no}?mchid={mchid}'.format(
            out_trade_no=out_trade_no,
            mchid=self.merchant_id)
        return self.request('GET', url)

    def post_transactions_close(self,out_trade_no):
        '''
        关闭订单API
        https://pay.weixin.qq.com/wiki/doc/apiv3/apis/chapter3_1_3.shtml
        :param out_trade_no:
        :return:
        '''
        url ='/v3/pay/transactions/out-trade-no/{out_trade_no}/close'.format(out_trade_no=out_trade_no)
        data ={"mchid": self.merchant_id}
        return self.request('POST',url,data)

    def post_domestic_refund(self,data):
        '''
        https://pay.weixin.qq.com/wiki/doc/apiv3/apis/chapter3_1_9.shtml
        :param data:
        :return:
        '''
        url = '/v3/refund/domestic/refunds'
        return self.request('POST',url,data)

    def get_refunds_out_refund_no(self,out_refund_no):
        '''
        查询单笔退款API
        https://pay.weixin.qq.com/wiki/doc/apiv3/apis/chapter3_1_10.shtml
        :param out_refund_no:
        :return:
        '''
        url ='/v3/refund/domestic/refunds/{out_refund_no}'.format(out_refund_no = out_refund_no)
        return self.request('GET',url)


    def get_bill_tradebill(self,bill_date,bill_type):
        '''
        申请交易账单API
        https://pay.weixin.qq.com/wiki/doc/apiv3/apis/chapter3_1_6.shtml
        :param bill_date:
        :param bill_type:
        :return:
        '''
        url ='/v3/bill/tradebill?bill_date=%s&bill_type=%s' %(bill_date,bill_type)
        return self.request('GET',url)

    def get_(self,bill_date):
        url ='/v3/bill/fundflowbill?bill_date=%s' % bill_date
        return  self.request('GET',url)

    # async def request(self,method,endpoint,**args):
    #     url = WECHATPAY_DOMAIN +endpoint
    #     token =self.credentials.get_token(method,endpoint,args.get('json'))
    #     headers = {'Authorization': '%s %s' %(self.credentials.schema,token),
    #                'Accept':'application/json'}
    #
    #     with self.client_session.request(method,url,headers=headers, **args) as resp:
    #         return resp


    def request(self,method,endpoint,data=None,**args):
        url = WECHATPAY_DOMAIN +endpoint
        text =''
        if data is not None:
            text = json.dumps(data)
        token =self.credentials.get_token(method,endpoint,text)
        headers = {'Authorization': '%s %s' % (self.credentials.schema, token),
                    'Accept':'application/json'}

        resp =requests.request(method,url,json = data,headers = headers,**args)
        return resp
