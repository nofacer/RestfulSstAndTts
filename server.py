import os
import zmq
import urllib.request
import urllib
import json
import base64
import subprocess
import wave
import pyaudio

class BaiduRest:
    def __init__(self, cu_id, api_key, api_secert):
        # token认证的url
        self.token_url = "https://openapi.baidu.com/oauth/2.0/token?grant_type=client_credentials&client_id=%s&client_secret=%s"
        # 语音合成的resturl
        self.getvoice_url = "http://tsn.baidu.com/text2audio?tex=%s&lan=zh&cuid=%s&ctp=1&tok=%s"
        # 语音识别的resturl
        self.upvoice_url = 'http://vop.baidu.com/server_api'

        self.cu_id = cu_id
        self.getToken(api_key, api_secert)
        return

    def getToken(self, api_key, api_secert):
        # 1.获取token
        token_url = self.token_url % (api_key,api_secert)

        r_str = urllib.request.urlopen(token_url).read()
        token_data = json.loads(r_str.decode('utf-8'))
        self.token_str = token_data['access_token']
        pass

    def getVoice(self, text, filename):
        # 2. 向Rest接口提交数据
        get_url = self.getvoice_url % (urllib.parse.quote(text), self.cu_id, self.token_str)
        subprocess.Popen(['mpg123', '-q', get_url]).wait()


        # voice_data = urllib.request.urlopen(get_url).read()
        # # 3.处理返回数据
        # voice_fp = open(filename,'wb+')
        # voice_fp.write(voice_data)
        # voice_fp.close()
        pass

    def getText(self, filename):
        # 2. 向Rest接口提交数据
        data = {}
        # 语音的一些参数
        data['format'] = 'wav'
        data['rate'] = 8000
        data['channel'] = 1
        data['cuid'] = self.cu_id
        data['token'] = self.token_str
        wav_fp = open(filename,'rb')
        voice_data = wav_fp.read()
        data['len'] = len(voice_data)
        data['speech'] = base64.b64encode(voice_data).decode('utf-8')

        post_data = json.dumps(data)
        r_data = urllib.request.urlopen(self.upvoice_url,data=bytes(post_data,encoding="utf-8")).read()
        wav_fp.close()
        if os.path.exists(filename):
            os.remove(filename)
        else:
            print("no such file")
        # 3.处理返回数据
        temp=json.loads(r_data.decode('utf-8'))
        print(temp)
        try:
            result=json.dumps(temp['result'], ensure_ascii=False).replace('"',"").replace('[',"").replace(']',"").replace('，',"")
        except:
            result="error"

        return  result




if __name__ == "__main__":
    # print('Process id:', str(os.getpid()))
    # # 我的api_key,供大家测试用，在实际工程中请换成自己申请的应用的key和secert
    #
    api_key = "HHDkfiKXG1Zyzzu7VC65iW9Q"
    api_secert = "vqLn7zaeiq3Rd3wPI67HGuhMZErLNmP2"
    # # 初始化
    bdr = BaiduRest("test_python", api_key, api_secert)
    # 将字符串语音合成并保存为out.mp3
    # bdr.getVoice("哈哈哈!", "out.mp3")
    # 识别test.wav语音内容并显示
    # print(bdr.getText("out.wav"))


    # server
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind('tcp://127.0.0.1:5555')
    while True:
        msg = socket.recv().decode('utf-8')
        voice2text=bdr.getText(msg)
        print(voice2text)
        if(("名字" in voice2text) and ("你" in voice2text)):
            bdr.getVoice("我叫王八蛋", "out.mp3")


        socket.send_string("received")
