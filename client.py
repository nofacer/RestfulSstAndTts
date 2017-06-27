#!usr/bin/env python
# coding=utf-8
import os
import numpy as np
from pyaudio import PyAudio, paInt16
from datetime import datetime
import wave
import zmq


print ('Process id:',str(os.getpid()) )


NUM_SAMPLES = 2000      # pyAudio内部缓存的块的大小
SAMPLING_RATE = 8000    # 取样频率
LEVEL = 1500            # 声音保存的阈值
COUNT_NUM = 20          # NUM_SAMPLES个取样之内出现COUNT_NUM个大于LEVEL的取样则记录声音
SAVE_LENGTH = 8         # 声音记录的最小长度：SAVE_LENGTH * NUM_SAMPLES 个取样


def save_wave_file(socket,filename, data):
    '''''save the date to the wav file'''
    print('Saving file')
    wf = wave.open(filename, 'wb')
    wf.setnchannels(1)
    wf.setsampwidth(2)
    wf.setframerate(SAMPLING_RATE)
    wf.writeframes(b"".join(data))
    wf.close()
    print('Send message to server')
    socket.send_string(filename)
    msg = socket.recv()
    print(msg)




def record_wave(socket):

    # 开启声音输入
    pa = PyAudio()
    stream = pa.open(format=paInt16, channels=1, rate=SAMPLING_RATE, input=True,
                     frames_per_buffer=NUM_SAMPLES)

    save_count = SAVE_LENGTH
    save_buffer = []
    if_first = 0
    while True:

        string_audio_data = stream.read(NUM_SAMPLES)
        # print((str(string_audio_data).encode('utf-8').decode()))
        print('*')
        audio_data = np.fromstring(string_audio_data, dtype=np.short)
        large_sample_count = np.sum(audio_data > LEVEL)
        if large_sample_count > COUNT_NUM:
            print('Catching...')
            save_count = SAVE_LENGTH
            if_first = 1
        else:
            save_count -= 1
        if save_count < 0:
            save_count = 0
        print(save_count)
        if save_count > 0:

            save_buffer.append(string_audio_data)
        else:

            if (len(save_buffer) > 0) and if_first > 0:
                filename ="wav/" + datetime.now().strftime("%Y-%m-%d_%H_%M_%S") + ".wav"

                save_wave_file(socket,filename, save_buffer)
                save_buffer = []



def main():
    context = zmq.Context()
    socket = context.socket(zmq.REQ)
    socket.connect('tcp://127.0.0.1:5555')
    # socket.send_string(args.bar)
    # msg = socket.recv()
    # print(msg)
    record_wave(socket)


if __name__ == "__main__":
    main()
