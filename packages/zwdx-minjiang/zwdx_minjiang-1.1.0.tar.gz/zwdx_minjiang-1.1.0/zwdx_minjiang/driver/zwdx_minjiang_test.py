# -*- coding: utf-8 -*-
'''
@Project : zwdx_quantumcontrol
@File : .py
@description : Equipment control adapter interface
@Author : anonymous
@Date : 2024.11.01
'''

import os
import time
import math
import datetime
import threading

import zerorpc
import numpy as np
import pandas as pd
import seaborn as sns
from collections import defaultdict
from matplotlib import pyplot as plt
import matplotlib.widgets as widgets
from IPython.display import clear_output

from zwdx_minjiang.driver.CTP100_Dev import ZW_CTP100_Dev
from zwdx_minjiang.driver.qulab_toolbox import wavedata as WD
from zwdx_minjiang.driver import zwdx_minjiang_tools as MinJiangTools

class MinJiangTest(object):
    def __init__(self) -> None:
        self.STOP_FLAG = False # 停止判定,用于中断测试的FLAG
        self.dev_ctp = None # CTP100设备对象
        self.dev_qcs = None # QCS220设备对象
        self.env_para = None # 实验环境参数
        self.finish_len = 100 # 存储实验的已完成次数,打印进度条和画波形时使用
        self.all_len = 100 # 存储实验的总循环次数,打印进度条和画波形时使用
        self.data_save_path = '' # 数据存储路径
        self.file_name = 'test' # 数据存储名称
        self.sampleRate_Hz = 8e9 # QCS采样率
        self.test_data = defaultdict(list) # 存储数据
        self.mask = None # 绘制热力图时，控制未绘制的区域不显示
        self.__path = 'test'

    def connect_dev(self, para):
        """ 连接设备
        """
        # 连接CTP
        if para['trig_name'] == 'CTP100':
            self.dev_ctp = ZW_CTP100_Dev(para['trig_ip'])
            try:
                st = self.dev_ctp.trigger_open()
                if st in ['ok']:
                    self.dev_ctp.trigger_close()
                else:
                    self.dev_ctp = None
            except:
                self.dev_qcs = None
        # 连接QCS
        if para['qcs_name'] == 'QCS220':
            self.dev_qcs = zerorpc.Client()
            try:
                self.dev_qcs.connect('tcp://' + para['qcs_ip'])
                if not self.dev_qcs.my_status() in ['ok']:
                    self.dev_qcs = None
            except:
                self.dev_qcs = None

        if self.dev_ctp is None or self.dev_qcs is None:
            print('Failed to connect device')
        else:
            print('Connect success')

    def close_qcs_all_channels(self):
        """关闭QCS所有通道
        """
        if self.dev_qcs is not None:
            for i in range(14):
                self.dev_qcs.dac_close(i)
                self.set_qcs_freq(i, 0, 2e-6, 0, delay=0e-9, replay_continue=False)
            for i in range(14,21,1):
                self.dev_qcs.set_ch_offset(i, 0)

    def set_qcs_sampling_nyquist(self,sampling_mhz:int = 8000,nyquist:int = 1):
        """ 设置QCS设备采样率和奈奎斯特域

        Args:
            sampling_mhz (int): 采样率 ,单位 MHZ
            nyquist (int): 奈奎斯特域
        """
        if self.dev_qcs is None:
            return False
        self.sampleRate_Hz = round(sampling_mhz * 1e6)
        if self.dev_qcs is not None:
            #set all DA channel sampling rate 
            self.dev_qcs.rfdac_sampling(sampling_mhz,0) # DA channel 0 to 5 use a nyquist 
            self.dev_qcs.rfdac_sampling(sampling_mhz,6) # DA channel 6 to 13 use a nyquist
            self.dev_qcs.rfdac_sampling(sampling_mhz,14) # DA channel 14 to 21 use a nyquist
            
            #set all DA channel nyquist
            self.dev_qcs.rfdac_SetNyquistZone(nyquist,0) # DA channel 0 to 5 use a nyquist 
            self.dev_qcs.rfdac_SetNyquistZone(nyquist,6) # DA channel 6 to 13 use a nyquist 
            self.dev_qcs.rfdac_SetNyquistZone(0,14) # DA channel 14 to 21 use a nyquist，Z-PULSE channel is usually set to 0

    def set_qcs_freq(self, ch_num, fout, datalen, amp=1, delay=0e-9, phi=0, replay_continue:bool=False):
        """设置QCS220设备频率

        Args:
            ch_num (_type_): 通道号
            fout (_type_): 输出频率
            datalen (_type_): 输出数据长度
            amp (int, optional):输出功率. 默认为 1.
            delay (_type_, optional): 延时时间. 默认为 0e-9.
            phi (int, optional): 相位. 默认为 0.
            replay_continue (bool, optional): 连续播放. 默认为 False.
        """
        if self.dev_qcs is None:
            return False
        fs_fout = self.sampleRate_Hz/256/1024
        fout = fout * 1e6
        if replay_continue:
            fout_wr = (fout//fs_fout) * fs_fout # dac_data_continue
        else:
            fout_wr = fout
        sin1=WD.Sin(fout_wr*2*np.pi, phi, datalen, self.sampleRate_Hz) * (2**13 - 1) * amp
        dac_data = np.int16(sin1.data)
        dac_data = dac_data.tolist()
        da_trigger_delay = int(delay*self.sampleRate_Hz)
        replay_times = 100000
        self.dev_qcs.dac_updata(ch_num, da_trigger_delay, replay_times, replay_continue, dac_data)


    def set_freq_xy_gauss(self, ch_num, fout, datalen, amp=1, delay =10e-9, phi = 0): 
        """_summary_

        Args:
            ch_num (_type_): 通道号
            fout (_type_): 输出频率
            datalen (_type_): 输出数据长度
            amp (int, optional):输出功率. 默认为 1.
            delay (_type_, optional): 延时时间. 默认为 10e-9.
            phi (int, optional): 相位. 默认为 0.
        """
        if self.dev_qcs is None:
            return False
        fout = fout * 1e6
        sin1=WD.Sin(fout*2*np.pi, phi, datalen, self.sampleRate_Hz)
        gaussian = WD.Gaussian2(datalen, self.sampleRate_Hz, a=5)
        data = (gaussian.data * sin1.data)*(2**13-1) * amp
        dac_data = np.int16(data)
        dac_data = dac_data.tolist()
        da_trigger_delay = int(delay*self.sampleRate_Hz)
        replay_times = 100000
        replay_continue = 0
        self.dev_qcs.dac_updata(ch_num, da_trigger_delay, replay_times, replay_continue, dac_data)


    def set_xy_two_pluse_t_gauss(self, ch_num, fout, datalen, amp=1, t_s=0, t_delay=10e-9):
        """_summary_

        Args:
            ch_num (_type_): 通道号
            fout (_type_): 输出频率
            datalen (_type_): 输出数据长度
            amp (int, optional): 输出功率. 默认为 1.
            t_s (int, optional): _description_. 默认为0.
            t_delay (_type_, optional): 延时时间. 默认为10e-9.
        """
        if self.dev_qcs is None:
            return False
        alltime = datalen * 2 + t_s
        assert alltime < 30e-6, "pluse length is over [30us]"
        fout = fout * 1e6
        sin1 = WD.Sin(fout*2*np.pi, 0, alltime, self.sampleRate_Hz)
        gaussian1 = WD.Gaussian2(datalen, self.sampleRate_Hz, a=5)
        t = np.zeros(math.ceil(t_s*self.sampleRate_Hz))
        gaussian2 = WD.Gaussian2(datalen, self.sampleRate_Hz,a=5)

        length = len(gaussian1.data.tolist()) + len(t.tolist()) + len(gaussian2.data.tolist())
        if length > len(sin1.data.tolist()):
            t1 = np.zeros(len(t)-1)
        elif length < len(sin1.data.tolist()):
            t1 = np.append(t,np.zeros(1))
        else:
            t1 = t
        wave = gaussian1.data.tolist() + t1.tolist() + gaussian2.data.tolist()
        data = wave * sin1.data *(2**13-1) * amp
        # Send the combined pulse data to the xyz device
        dac_data = np.int16(data)
        dac_data = dac_data.tolist()
        da_trigger_delay = int(t_delay * self.sampleRate_Hz)
        replay_times = 100000
        replay_continue = 0
        self.dev_qcs.dac_updata(ch_num, da_trigger_delay, replay_times, replay_continue, dac_data)
         
    def draw_line_chart(self,title='test',xlabel='x',ylabel='y'):
        """ xy类型数据画图, 数据来源于键值对, x为键,y为值
        Args:
            title (str, optional): 标题
            xlabel (str, optional): x轴标签
            ylabel (str, optional): y轴标签
        """
        plt.ion() 
        time.sleep(1)
        while not self.STOP_FLAG:
            _finish_len = self.finish_len
            _all_len = self.all_len
            mdata = self.test_data.copy()
            if not len(mdata['x']) == len(mdata['y']):
                continue
            clear_output(wait=True)
            plt.figure(figsize=(7,5))
            plt.title(title) 
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.plot(mdata['x'], mdata['y'])
            plt.grid()
            finish = round(self.finish_len/self.all_len*70)
            if _finish_len == _all_len:
                plt.savefig(f'{self.__path}/{self.file_name}.png',bbox_inches='tight')
            plt.show()
            print(f'\r[{"■"*finish}{"-"*(70-finish)}] {round(finish/70*100)}% ', end="")
            time.sleep(0.1)
            if _finish_len == _all_len:
                break
        
    def draw_finally_line(self,title='test',xlabel='x',ylabel='y'):
        mdata = self.test_data.copy()
        clear_output(wait=True)
        plt.figure(figsize=(7,5))
        plt.title(title) 
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.plot(mdata['x'], mdata['y'])
        plt.grid()
        plt.show()
        
    def draw_heatmap_chart(self,title='test',xlabel='x',ylabel='y'):
        """ xyz类型数据画图, 数据来源于键值对, x为键,y为值
        Args:
            title (str, optional): 标题
            xlabel (str, optional): x轴标签
            ylabel (str, optional): y轴标签
        """
        plt.ion() 
        time.sleep(1)
        while not self.STOP_FLAG:
            mdata = self.test_data.copy()
            _finish_len = self.finish_len
            _all_len = self.all_len
            clear_output(wait=True)
            plt.figure(figsize=(7, 5))
            sns.set(font_scale=1)
            df = pd.DataFrame(data=mdata['z'], index=mdata['x'] ,columns=mdata['y'])
            sns.heatmap(df,cmap="viridis_r",mask=self.mask)
            plt.title(title) 
            plt.xlabel(xlabel)
            plt.ylabel(ylabel)
            plt.grid()
            finish = round(self.finish_len/self.all_len*70)
            if _finish_len == _all_len:
                plt.savefig(f'{self.__path}/{self.file_name}.png',bbox_inches='tight')
            plt.show()
            print(f'\r[{"■"*finish}{"-"*(70-finish)}] {round(finish/70*100)}% ', end="")
            time.sleep(0.1)
            if _finish_len == _all_len:
                break
            
    def draw_finally_heatmap(self,title='test',xlabel='x',ylabel='y'):
        mdata = self.test_data.copy()
        df = pd.DataFrame(data=mdata['z'], index=mdata['x'] ,columns=mdata['y'])
        clear_output(wait=True)
        fig,ax = plt.subplots()
        sns.set(font_scale=1)
        sns.heatmap(df,cmap="viridis_r")
        plt.title(title) 
        plt.xlabel(xlabel)
        plt.ylabel(ylabel)
        plt.grid()
        plt.show()
        widgets.Cursor(ax, useblit=True, color='red', linewidth=1)
        def show_coordinates(event):
            row = event.ydata
            col = event.xdata
            if row is not None and col is not None and 0 <= row < df.shape[0] and 0 <= col < df.shape[1]:
                text.set_text('x: %.1f, y: %.1f, z: %.2f' % (mdata['x'][int(row)], mdata['y'][int(col)],mdata['z'][int(row)][int(col)]))
        fig.canvas.mpl_connect('motion_notify_event', show_coordinates)
        text = ax.text(0.5, 0.9, '', transform=ax.transAxes, color='red')
        
    def demo_line(self):
        """演示程序"""
        self.__path = f'{self.data_save_path}/demo'
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        self.file_name = f'demo_line'
        self.test_data.clear() 
        test_point = np.linspace(2500, 3500,101)
        self.all_len = len(test_point)
        self.finish_len = 0
        t1 = threading.Thread(target=self.draw_line_chart,args=('demo_line','x','y',))
        t1.start()
        for index in range(len(test_point)):
            if self.STOP_FLAG:
                break
            y_mod = np.random.randint(20,300)
            self.test_data['x'].append(index)
            self.test_data['y'].append(y_mod)
            self.finish_len = index + 1
            MinJiangTools.sleep_ms(50)
        t1.join()        

    def demo_heatmap(self):
        """演示程序"""
        self.__path = f'{self.data_save_path}/demo'
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        self.file_name = f'demo_heatmap'
        self.test_data.clear() 
        x = np.linspace(2900, 3100,21)
        y = [0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1]
        self.test_data['x'] = x
        self.test_data['y'] = y
        z_temp = []
        for i in range(len(x)):
            z_temp.append(np.zeros_like(y))
        self.test_data['z'] = z_temp
        self.mask = (np.random.randint(1,size=(len(x),len(y)))==0)
        self.all_len = len(x) * len(y)
        self.finish_len = 0
        t1 = threading.Thread(target=self.draw_heatmap_chart,args=('demo_hetmap','x','y',))
        t1.start()
        for ix in range(len(x)):
            if self.STOP_FLAG:
                break
            for iy in range(len(y)):
                if self.STOP_FLAG:
                    break
                z_mod = np.random.randint(20,300)
                self.test_data['z'][ix][iy] = z_mod
                self.mask[ix][iy] = False
                self.finish_len = ix * len(y) + iy + 1
                MinJiangTools.sleep_ms(50)
        t1.join()  

    def delay_test(self,test_para,trig_para):
        """ 延时标定测试

        Args:
            test_para (_type_): 实验测试参数
            trig_para (_type_): 实验Trig设备参数

        Returns:
            _type_: _description_
        """
        if self.dev_qcs is None or self.dev_ctp is None:
            return False
        self.__path = f'{self.data_save_path}/0_delay_test'
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        now_time = datetime.datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
        self.file_name = f'{self.env_para["qubit"]}_delay_test_{now_time}'
        self.test_data.clear()
        self.close_qcs_all_channels()
        self.dev_ctp.trigger_ctrl(test_para['trig_ch'], trig_para)  
        test_point = np.linspace(test_para['read_in_delay']['start'], test_para['read_in_delay']['end'],
                    round(abs(test_para['read_in_delay']['end'] - test_para['read_in_delay']['start'])/test_para['read_in_delay']['step']) + 1)
        self.all_len = len(test_point)
        self.finish_len = 0
        t1 = threading.Thread(target=self.draw_line_chart,args=('delay_test','delay/s','mod',))
        t1.start()
        for index in range(len(test_point)):
            if self.STOP_FLAG:
                break
            delay = test_point[index]
            self.dev_qcs.trigger_close()
            self.dev_ctp.trigger_close()
            self.set_qcs_freq(test_para['read_out_ch'], test_para['read_out_freq'], test_para['read_out_pw'], test_para['read_out_amp'], delay=test_para['read_out_delay'], replay_continue=False)
            ad_trigger_delay = round(delay*2.5e9 ) #AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到
            mul_start_phase = 0     #解模参数：初相
            mul_f_freq = test_para['read_out_freq'] * 1e6    #解模参数：频率，一般每个qubit对应不同频率
            mul_f_len = round(test_para['read_in_pw']*2.5e9)      #解模参数：单次解模shot数据样点数量 
            mul_f = [[mul_start_phase, mul_f_freq]]    #解模参数列表，最多32组，对应一条线路上的32qubit
            self.dev_qcs.rd_adc_mul_data_ctrl(test_para['read_in_ch'], ad_trigger_delay, test_para['shots'],mul_f_len,mul_f)
            self.dev_qcs.trigger_ctrl(test_para['trig_mode'],trig_para['trigger_us'],test_para['shots'],trig_para['trigger_continue'])
            self.dev_ctp.trigger_open()
            # MinJiangTools.sleep_ms(1)
            while 1:
                mul_data_bufe,read_data_len = self.dev_qcs.rd_adc_mul_data(test_para['read_in_ch'],0,test_para['shots'])
                if read_data_len != -1:
                    break
            for i in range(read_data_len):
                mul_data_bufe[i] = complex(mul_data_bufe[i])
            y_mod = np.abs(np.mean(mul_data_bufe) / mul_f_len / 8191)
            self.test_data['x'].append(delay)
            self.test_data['y'].append(y_mod)
            self.finish_len = index + 1
        MinJiangTools.write_data_to_csv(self.__path,self.file_name,self.env_para,test_para,trig_para,self.test_data)
        t1.join()
            
    def plot_raw_data(self,test_para,trig_para):
        """ 原始数据采集并画波形

        Args:
            test_para (_type_): 实验测试参数
            trig_para (_type_): 实验Trig设备参数

        Returns:
            _type_: _description_
        """
        if self.dev_qcs is None or self.dev_ctp is None:
            return False
        self.dev_qcs.trigger_close()
        self.dev_ctp.trigger_close()
        self.dev_ctp.trigger_ctrl(test_para['trig_ch'],trig_para)
        self.set_qcs_freq(test_para['read_out_ch'], test_para['read_out_freq'], test_para['read_out_pw'],test_para['read_out_amp'], delay=test_para['read_out_delay'],replay_continue=False)
        ad_trigger_delay = test_para['read_in_delay'] * 2.5e9  #AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到datalen_s*2.5e9
        self.dev_qcs.rd_adc_data_ctrl(test_para['read_in_ch'], ad_trigger_delay, test_para['shots'], round(test_para['read_in_pw'] * 2.5e9))     
        self.dev_qcs.trigger_ctrl(test_para['trig_mode'],trig_para['trigger_us'],test_para['shots'],trig_para['trigger_continue'])
        self.dev_ctp.trigger_open()
        time.sleep(0.1)
        adc_data_buf, save_len_i = self.dev_qcs.rd_adc_data(test_para['read_in_ch'], test_para['shots'], round(test_para['read_in_pw'] * 2.5e9))
        adc_data_w = []
        data_w = np.kaiser(save_len_i, 8)
        adc_data_w = adc_data_buf
        adc_data_w = adc_data_w * data_w
        plt.plot(adc_data_buf[0:round(test_para['plot_pw'] * 2.5e9)])
        plt.show()

    def sweep_cavity_freq(self,test_para,trig_para):
        """ 扫腔频测试

        Args:
            test_para (_type_): 实验测试参数
            trig_para (_type_): 实验Trig设备参数

        Returns:
            _type_: _description_
        """
        if self.dev_qcs is None or self.dev_ctp is None:
            return False
        self.__path = f'{self.data_save_path}/1_cavity_freq'
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        now_time = datetime.datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
        self.file_name = f'{self.env_para["qubit"]}_cavity_freq_{now_time}'
        self.test_data.clear()
        self.close_qcs_all_channels()
        self.dev_ctp.trigger_ctrl(test_para['trig_ch'], trig_para)
        test_point = np.around(np.linspace(test_para['sweep_freq']['start'], test_para['sweep_freq']['end'], 
                                round(abs(test_para['sweep_freq']['end'] - test_para['sweep_freq']['start'])/test_para['sweep_freq']['step']) + 1), 2)
        self.all_len = len(test_point)
        self.finish_len = 0
        t1 = threading.Thread(target=self.draw_line_chart,args=('cavity_freq','MHz','mod',))
        t1.start()
        for index in range(len(test_point)):
            if self.STOP_FLAG:
                break
            freq = test_point[index]
            self.dev_qcs.trigger_close()
            self.dev_ctp.trigger_close()
            self.set_qcs_freq(test_para['read_out_ch'], freq, test_para['read_out_pw'], test_para['read_out_amp'], delay=test_para['read_out_delay'], replay_continue=False)
            #解模参数配置
            ad_trigger_delay = (260e-9 + test_para['read_in_delay'])*2.5e9  #AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到
            mul_start_phase = 0     #解模参数：初相
            mul_f_freq = (freq) * 1e6    #解模参数：频率，一般每个qubit对应不同频率
            mul_f_len = round(test_para['read_in_pw'] * 2.5e9)       #解模参数：单次解模shot数据样点数量 
            mul_f = [[mul_start_phase, mul_f_freq]]    #解模参数列表，最多32组，对应一条线路上的32qubit
            self.dev_qcs.rd_adc_mul_data_ctrl(test_para['read_in_ch'],ad_trigger_delay,test_para['shots'],mul_f_len,mul_f)
            self.dev_qcs.trigger_ctrl(test_para['trig_mode'],trig_para['trigger_us'],test_para['shots'],trig_para['trigger_continue'])
            self.dev_ctp.trigger_open()
            # MinJiangTools.sleep_ms(1)
            while 1:
                mul_data_bufe,read_data_len = self.dev_qcs.rd_adc_mul_data(test_para['read_in_ch'],0,test_para['shots'])
                if read_data_len != -1:
                    break
            for i in range(read_data_len):
                mul_data_bufe[i] = complex(mul_data_bufe[i])
            y_mod = np.abs(np.mean(mul_data_bufe) /mul_f_len / (2**13-1))
            self.test_data['x'].append(freq)
            self.test_data['y'].append(y_mod)
            self.finish_len = index + 1
        MinJiangTools.write_data_to_csv(self.__path,self.file_name,self.env_para,test_para,trig_para,self.test_data)
        t1.join()


    def sweep_qa_power_freq(self,test_para,trig_para):
        """读取腔色散频移扫描

        Args:
            test_para (_type_): 实验测试参数
            trig_para (_type_): 实验Trig设备参数

        Returns:
            _type_: _description_
        """
        if self.dev_qcs is None or self.dev_ctp is None:
            return False
        self.__path = f'{self.data_save_path}/2_dispersion_freqshift'
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        now_time = datetime.datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
        self.file_name = f'{self.env_para["qubit"]}_dispersion_freqshift_{now_time}'
        self.test_data.clear()
        self.close_qcs_all_channels()
        self.dev_ctp.trigger_ctrl(test_para['trig_ch'], trig_para)
        x = np.around(np.linspace(test_para['sweep_amp']['start'], test_para['sweep_amp']['end'], 
                                round(abs(test_para['sweep_amp']['end'] - test_para['sweep_amp']['start'])/test_para['sweep_amp']['step']) + 1), 2)
        y = np.around(np.linspace(test_para['sweep_freq']['start'], test_para['sweep_freq']['end'], 
                                round(abs(test_para['sweep_freq']['end'] - test_para['sweep_freq']['start'])/test_para['sweep_freq']['step']) + 1), 2)
        self.test_data['x'] = x
        self.test_data['y'] = y
        z_temp = []
        for i in range(len(x)):
            z_temp.append(np.zeros_like(y))
        self.test_data['z'] = z_temp
        self.mask = (np.random.randint(1,size=(len(x),len(y)))==0)
        self.all_len = len(x) * len(y)
        self.finish_len = 0
        t1 = threading.Thread(target=self.draw_heatmap_chart,args=('dispersion_freqshift','freq/MHz','amp',))
        t1.start()
        for index_x in range(len(x)):
            if self.STOP_FLAG:
                break
            power = x[index_x]
            for index_y in range(len(y)):
                if self.STOP_FLAG:
                    break
                freq = y[index_y]
                self.dev_qcs.trigger_close()
                self.dev_ctp.trigger_close()
                self.set_qcs_freq(test_para['read_out_ch'], freq, test_para['read_out_pw'], amp=power, delay=test_para['read_out_delay'], replay_continue=False)
                ad_trigger_delay = (260e-9 + test_para['read_in_delay']) * 2.5e9  #AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到
                mul_start_phase = 0     #解模参数：初相
                mul_f_freq = (freq) * 1e6    #解模参数：频率，一般每个qubit对应不同频率
                mul_f_len = int(test_para['read_in_pw'] * 2.5e9)       #解模参数：单次解模shot数据样点数量 
                mul_f = [[mul_start_phase, mul_f_freq]]    #解模参数列表，最多32组，对应一条线路上的32qubit
                self.dev_qcs.rd_adc_mul_data_ctrl(test_para['read_in_ch'], ad_trigger_delay, test_para['shots'], mul_f_len, mul_f)
                self.dev_qcs.trigger_ctrl(test_para['trig_mode'],trig_para['trigger_us'],test_para['shots'],trig_para['trigger_continue'])
                self.dev_ctp.trigger_open()
                # MinJiangTools.sleep_ms(1)
                while 1:
                    mul_data_bufe,read_data_len = self.dev_qcs.rd_adc_mul_data(test_para['read_in_ch'],0,test_para['shots'])
                    if read_data_len != -1:
                        break
                for i in range(read_data_len):
                    mul_data_bufe[i] = complex(mul_data_bufe[i])
                iq_lh = np.mean(mul_data_bufe) / mul_f_len / (2**13-1) /power
                self.test_data['z'][index_x][index_y] = np.abs(iq_lh)
                self.mask[index_x][index_y] = False
                self.finish_len = index_x * len(y) + index_y + 1
        MinJiangTools.write_data_to_csv(self.__path,self.file_name,self.env_para,test_para,trig_para,self.test_data)
        t1.join()
                
    def sweep_z_qa_freq(self,test_para,trig_para):
        """能谱腔频实验

        Args:
            test_para (_type_): 实验测试参数
            trig_para (_type_): 实验Trig设备参数

        Returns:
            _type_: _description_
        """
        if self.dev_qcs is None or self.dev_ctp is None:
            return False
        self.__path = f'{self.data_save_path}/3_Zbias_cavityfreq_sweep'
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        now_time = datetime.datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
        self.file_name = f'{self.env_para["qubit"]}_Zbias_cavityfreq_sweep_{now_time}'
        self.test_data.clear()
        self.close_qcs_all_channels()
        self.dev_ctp.trigger_ctrl(test_para['trig_ch'],trig_para)
        x = np.around(np.linspace(test_para['sweep_z_amp']['start'], test_para['sweep_z_amp']['end'],
                        round(abs(test_para['sweep_z_amp']['end'] - test_para['sweep_z_amp']['start'])/test_para['sweep_z_amp']['step']) + 1), 2)
        y = np.around(np.linspace(test_para['sweep_cavity_freq']['start'], test_para['sweep_cavity_freq']['end'], 
                                round(abs(test_para['sweep_cavity_freq']['end'] - test_para['sweep_cavity_freq']['start'])/test_para['sweep_cavity_freq']['step']) + 1), 2)
        self.test_data['x'] = x
        self.test_data['y'] = y
        z_temp = []
        for i in range(len(x)):
            z_temp.append(np.zeros_like(y))
        self.test_data['z'] = z_temp
        self.mask = (np.random.randint(1,size=(len(x),len(y)))==0)
        self.all_len = len(x) * len(y)
        self.finish_len = 0
        t1 = threading.Thread(target=self.draw_heatmap_chart,args=('Zbias_cavityfreq_sweep','freq/MHz','zbais',))
        t1.start()
        for index_x in range(len(x)):
            if self.STOP_FLAG:
                break
            temp_amp = x[index_x]
            self.dev_qcs.dac_close(0)
            self.dev_qcs.set_ch_offset(test_para['z_ch'], temp_amp)
            for index_y in range(len(y)):
                if self.STOP_FLAG:
                    break
                freq = y[index_y]
                self.dev_qcs.trigger_close()
                self.dev_ctp.trigger_close()
                self.set_qcs_freq(test_para['read_out_ch'], freq, test_para['read_out_pw'], amp=test_para['read_out_amp'], delay=test_para['read_out_delay'], replay_continue=False)
                ad_trigger_delay = (260e-9 + test_para['read_in_delay']) * 2.5e9  #AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到
                mul_start_phase = 0     #解模参数：初相
                mul_f_freq = (freq) * 1e6    #解模参数：频率，一般每个qubit对应不同频率
                mul_f_len = round(test_para['read_in_pw'] * 2.5e9)       #解模参数：单次解模shot数据样点数量 
                mul_f = [[mul_start_phase, mul_f_freq]]    #解模参数列表，最多32组，对应一条线路上的32qubit
                self.dev_qcs.rd_adc_mul_data_ctrl(test_para['read_in_ch'],ad_trigger_delay,test_para['shots'],mul_f_len,mul_f)
                self.dev_qcs.trigger_ctrl(test_para['trig_mode'],trig_para['trigger_us'],test_para['shots'],trig_para['trigger_continue'])
                self.dev_ctp.trigger_open()
                # MinJiangTools.sleep_ms(1)
                while 1:
                    mul_data_bufe,read_data_len = self.dev_qcs.rd_adc_mul_data(test_para['read_in_ch'],0,test_para['shots'])
                    if read_data_len != -1:
                        break
                for i in range(read_data_len):
                    mul_data_bufe[i] = complex(mul_data_bufe[i])
                iq_lh = np.mean(mul_data_bufe) / mul_f_len / (2**13-1)
                self.test_data['z'][index_x][index_y] = np.abs(iq_lh)
                self.mask[index_x][index_y] = False
                self.finish_len = index_x * len(y) + index_y + 1
        MinJiangTools.write_data_to_csv(self.__path,self.file_name,self.env_para,test_para,trig_para,self.test_data)
        t1.join()

    def sweep_cavity_freq_fine(self,test_para,trig_para):
        """细扫腔频

        Args:
            test_para (_type_): 实验测试参数
            trig_para (_type_): 实验Trig设备参数

        Returns:
            _type_: _description_
        """
        if self.dev_qcs is None or self.dev_ctp is None:
            return False
        self.__path = f'{self.data_save_path}/4_cavity_freq_dine'
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        now_time = datetime.datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
        self.file_name = f'{self.env_para["qubit"]}_cavity_freq_{now_time}'
        self.test_data.clear()
        self.close_qcs_all_channels()
        self.dev_qcs.set_ch_offset(test_para['z_ch'],test_para['zbias'])
        self.dev_ctp.trigger_ctrl(test_para['trig_ch'], trig_para)
        test_point = np.around(np.linspace(test_para['sweep_freq']['start'], test_para['sweep_freq']['end'], 
                                round(abs(test_para['sweep_freq']['end'] - test_para['sweep_freq']['start'])/test_para['sweep_freq']['step']) + 1), 2)
        self.all_len = len(test_point)
        self.finish_len = 0
        t1 = threading.Thread(target=self.draw_line_chart,args=('cavity_freq_dine','MHz','mod',))
        t1.start()
        for index in range(len(test_point)):
            if self.STOP_FLAG:
                break
            freq = test_point[index]
            self.dev_qcs.trigger_close()
            self.dev_ctp.trigger_close()
            self.set_qcs_freq(test_para['read_out_ch'], freq, test_para['read_out_pw'], amp=test_para['read_out_amp'], delay=test_para['read_out_delay'], replay_continue=False)
            #解模参数配置
            ad_trigger_delay = (260e-9 + test_para['read_in_delay'])*2.5e9  #AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到
            mul_start_phase = 0     #解模参数：初相
            mul_f_freq = (freq) * 1e6    #解模参数：频率，一般每个qubit对应不同频率
            mul_f_len = round(test_para['read_in_pw'] * 2.5e9)       #解模参数：单次解模shot数据样点数量 
            mul_f = [[mul_start_phase, mul_f_freq]]    #解模参数列表，最多32组，对应一条线路上的32qubit
            self.dev_qcs.rd_adc_mul_data_ctrl(test_para['read_in_ch'],ad_trigger_delay,test_para['shots'],mul_f_len,mul_f)
            self.dev_qcs.trigger_ctrl(test_para['trig_mode'],trig_para['trigger_us'],test_para['shots'],trig_para['trigger_continue'])
            self.dev_ctp.trigger_open()
            # MinJiangTools.sleep_ms(1)
            while 1:
                mul_data_bufe,read_data_len = self.dev_qcs.rd_adc_mul_data(test_para['read_in_ch'],0,test_para['shots'])
                if read_data_len != -1:
                    break
            for i in range(read_data_len):
                mul_data_bufe[i] = complex(mul_data_bufe[i])
            y_mod = np.abs(np.mean(mul_data_bufe) /mul_f_len / (2**13-1))
            self.test_data['x'].append(freq)
            self.test_data['y'].append(y_mod)
            self.finish_len = index + 1
        MinJiangTools.write_data_to_csv(self.__path,self.file_name,self.env_para,test_para,trig_para,self.test_data)
        t1.join()

    def sweep_xy_freq(self,test_para,trig_para):
        """扫bit频率01

        Args:
            test_para (_type_): 实验测试参数
            trig_para (_type_): 实验Trig设备参数

        Returns:
            _type_: _description_
        """
        if self.dev_qcs is None or self.dev_ctp is None:
            return False
        self.__path = f'{self.data_save_path}/5.1_sweep_xy_freq'
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        now_time = datetime.datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
        self.file_name = f'{self.env_para["qubit"]}_sweep_xy_freq_{now_time}'
        self.test_data.clear()
        self.close_qcs_all_channels()
        self.dev_ctp.trigger_ctrl(test_para['trig_ch'],trig_para)
        self.dev_qcs.set_ch_offset(test_para['z_ch'], test_para['zbias'])   
        test_point = np.around(np.linspace(test_para['sweep_xy_freq']['start'], test_para['sweep_xy_freq']['end'],
                                round(abs(test_para['sweep_xy_freq']['end'] - test_para['sweep_xy_freq']['start'])/test_para['sweep_xy_freq']['step']) + 1), 2)
        self.all_len = len(test_point)
        self.finish_len = 0
        t1 = threading.Thread(target=self.draw_line_chart,args=('sweep_xy_freq','xy_freq','mod',))
        t1.start()
        for index in range(len(test_point)):
            if self.STOP_FLAG:
                break
            freq = test_point[index]
            self.dev_qcs.trigger_close()
            self.dev_ctp.trigger_close()
            xy_timelen = test_para['xy_pw']
            xy_delay = test_para['xy_delay']
            self.set_qcs_freq(test_para['read_out_ch'], test_para['read_out_freq'], test_para['read_out_pw'], amp=test_para['read_out_amp'], delay=xy_delay + xy_timelen + test_para['read_out_delay'], replay_continue=False)
            self.set_freq_xy_gauss(test_para['xy_ch'], freq, xy_timelen, amp=test_para['xy_amp'], delay=xy_delay)
            ad_fixed_delay = round(260e-9*2.5e9)
            ad_trigger_delay = ad_fixed_delay + int(xy_timelen*2.5e9)  + int(xy_delay * 2.5e9)+ int(test_para['read_in_delay'] * 2.5e9)#AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到
            mul_start_phase = 0     #解模参数：初相
            mul_f_freq = test_para['read_out_freq'] * 1e6    #解模参数：频率，一般每个qubit对应不同频率
            mul_f_len = round(test_para['read_in_pw'] *2.5e9)            #解模参数：单次解模shot数据样点数量
            mul_f = [[mul_start_phase, mul_f_freq]]    #解模参数列表，最多32组，对应一条线路上的32qubit
            self.dev_qcs.rd_adc_mul_data_ctrl(test_para['read_in_ch'],ad_trigger_delay,test_para['shots'],mul_f_len,mul_f)
            self.dev_qcs.trigger_ctrl(test_para['trig_mode'],trig_para['trigger_us'],test_para['shots'],trig_para['trigger_continue'])
            self.dev_ctp.trigger_open()
            # MinJiangTools.sleep_ms(1)
            while 1:
                mul_data_bufe,read_data_len = self.dev_qcs.rd_adc_mul_data(test_para['read_in_ch'],0,test_para['shots'])
                if read_data_len != -1:
                    break
            for i in range(read_data_len):
                mul_data_bufe[i] = complex(mul_data_bufe[i])
            y_mod = np.abs(np.mean(mul_data_bufe) /mul_f_len / (2**13-1))
            self.test_data['x'].append(freq)
            self.test_data['y'].append(y_mod)
            self.finish_len = index + 1
        MinJiangTools.write_data_to_csv(self.__path,self.file_name,self.env_para,test_para,trig_para,self.test_data)
        t1.join()


    def sweep_x_z_y_xyfreq(self,test_para,trig_para):
        """找bit频率f01的z偏置 2d swiff

        Args:
            test_para (_type_): 实验测试参数
            trig_para (_type_): 实验Trig设备参数

        Returns:
            _type_: _description_
        """
        if self.dev_qcs is None or self.dev_ctp is None:
            return False
        self.__path = f'{self.data_save_path}/5.2_f01_z_2D'
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        now_time = datetime.datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
        self.file_name = f'{self.env_para["qubit"]}_sweep_x_z_y_xyfreq_{now_time}'
        self.test_data.clear()
        self.close_qcs_all_channels()
        self.dev_ctp.trigger_ctrl(test_para['trig_ch'],trig_para)
        self.dev_qcs.set_ch_offset(test_para['z_ch'], test_para['zbias']) 
        y = np.around(np.linspace(test_para['sweep_z_amp']['start'], test_para['sweep_z_amp']['end'],
                        round(abs(test_para['sweep_z_amp']['end'] - test_para['sweep_z_amp']['start'])/test_para['sweep_z_amp']['step']) + 1), 2)
        x = np.around(np.linspace(test_para['sweep_xy_freq']['start'], test_para['sweep_xy_freq']['end'],
                                round(abs(test_para['sweep_xy_freq']['end'] - test_para['sweep_xy_freq']['start'])/test_para['sweep_xy_freq']['step']) + 1), 2)
        self.test_data['x'] = x
        self.test_data['y'] = y
        z_temp = []
        for i in range(len(x)):
            z_temp.append(np.zeros_like(y))
        self.test_data['z'] = z_temp
        self.mask = (np.random.randint(1,size=(len(x),len(y)))==0)
        self.all_len = len(x) * len(y)
        self.finish_len = 0
        self.set_qcs_freq(test_para['read_out_ch'], test_para['read_out_freq'], test_para['read_out_pw'], amp=test_para['read_out_amp'], delay=test_para['xy_delay'] + test_para['read_out_delay'] + test_para['xy_pw'], replay_continue=False)
        ad_fixed_delay = round(260e-9*2.5e9)
        ad_trigger_delay = ad_fixed_delay + round(test_para['xy_pw']*2.5e9)  + round(test_para['xy_delay'] * 2.5e9) + round(test_para['read_in_delay'] * 2.5e9) #AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到
        mul_start_phase = 0     #解模参数：初相
        mul_f_freq = test_para['read_out_freq'] * 1e6    #解模参数：频率，一般每个qubit对应不同频率
        mul_f_len = round(test_para['read_in_pw']  * 2e9 )      #解模参数：单次解模shot数据样点数量
        mul_f = [[mul_start_phase, mul_f_freq]]    #解模参数列表，最多32组，对应一条线路上的32qubit
        t1 = threading.Thread(target=self.draw_heatmap_chart,args=('f01_z_2D_xy','zbais','freq/MHz',))
        t1.start()
        for index_x in range(len(x)):
            if self.STOP_FLAG:
                break
            freq = x[index_x]
            for index_y in range(len(y)):
                if self.STOP_FLAG:
                    break
                z_amp = y[index_y]
                self.dev_qcs.trigger_close()
                self.dev_ctp.trigger_close()
                self.dev_qcs.set_ch_offset(test_para['z_ch'], z_amp)
                self.set_freq_xy_gauss(test_para['xy_ch'], freq, test_para['xy_pw'], amp = test_para['xy_amp'], delay = test_para['xy_delay'])
                self.dev_qcs.rd_adc_mul_data_ctrl(test_para['read_in_ch'],ad_trigger_delay,test_para['shots'] ,mul_f_len,mul_f)
                self.dev_qcs.trigger_ctrl(test_para['trig_mode'],trig_para['trigger_us'],test_para['shots'],trig_para['trigger_continue'])
                self.dev_ctp.trigger_open()
                # MinJiangTools.sleep_ms(1)
                while 1:
                    mul_data_bufe,read_data_len = self.dev_qcs.rd_adc_mul_data(test_para['read_in_ch'],0,test_para['shots'])
                    if read_data_len != -1:
                        break
                for i in range(read_data_len):
                    mul_data_bufe[i] = complex(mul_data_bufe[i])
                self.test_data['z'][index_x][index_y] = np.abs(np.mean(mul_data_bufe) / mul_f_len / (2**13-1))
                self.mask[index_x][index_y] = False
                self.finish_len = index_x * len(y) + index_y + 1
        MinJiangTools.write_data_to_csv(self.__path,self.file_name,self.env_para,test_para,trig_para,self.test_data)
        t1.join()

    def rabi_test(self,test_para,trig_para):
        """RABI幅度

        Args:
            test_para (_type_): 实验测试参数
            trig_para (_type_): 实验Trig设备参数

        Returns:
            _type_: _description_
        """
        if self.dev_qcs is None or self.dev_ctp is None:
            return False
        self.__path = f'{self.data_save_path}/6_rabi_amp'
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        now_time = datetime.datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
        self.file_name = f'{self.env_para["qubit"]}_rabi_test_{now_time}'
        self.test_data.clear()
        self.close_qcs_all_channels()
        self.dev_ctp.trigger_ctrl(test_para['trig_ch'],trig_para)
        self.dev_qcs.set_ch_offset(test_para['z_ch'], test_para['zbias'])
        test_point = np.around(np.linspace(test_para['sweep_xy_amp']['start'], test_para['sweep_xy_amp']['end'],
                        round(abs(test_para['sweep_xy_amp']['end'] - test_para['sweep_xy_amp']['start'])/test_para['sweep_xy_amp']['step']) + 1), 2)
        self.all_len = len(test_point)
        self.finish_len = 0
        t1 = threading.Thread(target=self.draw_line_chart,args=('rabi_amp','xy_amp','mod',))
        t1.start()
        for index in range(len(test_point)):
            if self.STOP_FLAG:
                break
            amp = test_point[index]
            xy_timelen = test_para['xy_pw']
            xy_delay = test_para['xy_delay']
            self.set_qcs_freq(test_para['read_out_ch'], test_para['read_out_freq'], test_para['read_out_pw'], amp=test_para['read_out_amp'], delay=xy_delay + xy_timelen + test_para['read_out_delay'], replay_continue=False)
            self.set_freq_xy_gauss(test_para['xy_ch'], test_para['xy_freq'], xy_timelen, amp, delay=xy_delay)
            ad_fixed_delay = round(260e-9*2.5e9)
            ad_trigger_delay = ad_fixed_delay + round(xy_timelen*2.5e9)  + round((xy_delay+test_para['read_in_delay']) * 2.5e9)#AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到
            mul_start_phase = 0     #解模参数：初相
            mul_f_freq = test_para['read_out_freq'] * 1e6    #解模参数：频率，一般每个qubit对应不同频率
            mul_f_len = round(test_para['read_in_pw'] * 2.5e9)       #解模参数：单次解模shot数据样点数量
            mul_f = [[mul_start_phase, mul_f_freq]]    #解模参数列表，最多32组，对应一条线路上的32qubit
            self.dev_qcs.rd_adc_mul_data_ctrl(test_para['read_in_ch'],ad_trigger_delay,test_para['shots'],mul_f_len,mul_f)
            self.dev_qcs.trigger_ctrl(test_para['trig_mode'],trig_para['trigger_us'],test_para['shots'],trig_para['trigger_continue'])
            self.dev_ctp.trigger_open()
            # MinJiangTools.sleep_ms(1)
            while 1:
                mul_data_bufe,read_data_len = self.dev_qcs.rd_adc_mul_data(test_para['read_in_ch'],0,test_para['shots'])
                if read_data_len != -1:
                    break
            for i in range(read_data_len):
                mul_data_bufe[i] = complex(mul_data_bufe[i])
            y_mod = np.abs(np.mean(mul_data_bufe)) / mul_f_len / 8191
            self.test_data['x'].append(amp)
            self.test_data['y'].append(y_mod)
            self.finish_len = index + 1
        MinJiangTools.write_data_to_csv(self.__path,self.file_name,self.env_para,test_para,trig_para,self.test_data)
        t1.join()

    def rabi_test_len(self,test_para,trig_para):
        """RABI脉宽

        Args:
            test_para (_type_): 实验测试参数
            trig_para (_type_): 实验Trig设备参数

        Returns:
            _type_: _description_
        """
        if self.dev_qcs is None or self.dev_ctp is None:
            return False
        self.__path = f'{self.data_save_path}/7_rabi_pw'
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        now_time = datetime.datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
        self.file_name = f'{self.env_para["qubit"]}_rabi_test_len_{now_time}'
        self.test_data.clear()
        self.close_qcs_all_channels()
        self.dev_ctp.trigger_ctrl(test_para['trig_ch'],trig_para)
        self.dev_qcs.set_ch_offset(test_para['z_ch'], test_para['zbias'])   
        test_point = np.linspace(test_para['sweep_xy_pw']['start'], test_para['sweep_xy_pw']['end'],
                                round(abs(test_para['sweep_xy_pw']['end'] - test_para['sweep_xy_pw']['start'])/test_para['sweep_xy_pw']['step']) + 1)
        self.all_len = len(test_point)
        self.finish_len = 0
        t1 = threading.Thread(target=self.draw_line_chart,args=('rabi_duration','xy_pulse_len/ns','mod',))
        t1.start()
        for index in range(len(test_point)):
            if self.STOP_FLAG:
                break
            add_delay = test_point[index]
            self.dev_qcs.trigger_close()
            self.dev_ctp.trigger_close()
            xy_timelen = add_delay
            xy_delay = test_para['xy_delay']
            self.set_qcs_freq(test_para['read_out_ch'], test_para['read_out_freq'], test_para['read_out_pw'], amp=test_para['read_out_amp'], delay=xy_delay + xy_timelen + test_para['read_out_delay'], replay_continue=False)
            self.set_freq_xy_gauss(test_para['xy_ch'], test_para['xy_freq'], xy_timelen, amp=test_para['xy_amp'], delay=xy_delay) #
            ad_fixed_delay = round(260e-9*2.5e9)
            ad_trigger_delay = ad_fixed_delay + round(xy_timelen*2.5e9)  + round(xy_delay * 2.5e9) + round(test_para['read_in_delay'] * 2.5e9)#AD采集延迟，样点数量，用户可以根据采样率5Gsps和时间计算取整后得到 
            mul_start_phase = 0     #解模参数：初相
            mul_f_freq = test_para['read_out_freq'] * 1e6    #解模参数：频率，一般每个qubit对应不同频率
            mul_f_len = round(test_para['read_in_pw']*2.5e9)      #解模参数：单次解模shot数据样点数量
            mul_f = [[mul_start_phase, mul_f_freq]]    #解模参数列表，最多32组，对应一条线路上的32qubit
            self.dev_qcs.rd_adc_mul_data_ctrl(test_para['read_in_ch'],ad_trigger_delay,test_para['shots'],mul_f_len,mul_f)
            self.dev_qcs.trigger_ctrl(test_para['trig_mode'],trig_para['trigger_us'],test_para['shots'],trig_para['trigger_continue'])
            self.dev_ctp.trigger_open()
            # MinJiangTools.sleep_ms(1)
            while 1:
                mul_data_bufe,read_data_len = self.dev_qcs.rd_adc_mul_data(test_para['read_in_ch'],0,test_para['shots'])
                if read_data_len != -1:
                    break
            for i in range(read_data_len):
                mul_data_bufe[i] = complex(mul_data_bufe[i])
            y_mod = np.abs(np.mean(mul_data_bufe) / mul_f_len / 8191)
            self.test_data['x'].append(add_delay*1e9)
            self.test_data['y'].append(y_mod)
            self.finish_len = index + 1
        MinJiangTools.write_data_to_csv(self.__path,self.file_name,self.env_para,test_para,trig_para,self.test_data)
        t1.join()

    def t1_test(self,test_para,trig_para):
        """T1测量

        Args:
            test_para (_type_): 实验测试参数
            trig_para (_type_): 实验Trig设备参数

        Returns:
            _type_: _description_
        """
        if self.dev_qcs is None or self.dev_ctp is None:
            return False
        self.__path = f'{self.data_save_path}/8_t1'
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        now_time = datetime.datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
        self.file_name = f'{self.env_para["qubit"]}_t1_test_{now_time}'
        self.test_data.clear()
        self.close_qcs_all_channels()
        self.dev_ctp.trigger_ctrl(test_para['trig_ch'],trig_para)
        self.dev_qcs.set_ch_offset(test_para['z_ch'], test_para['zbias'])
        test_point = np.linspace(test_para['sweep_read_delay']['start'], test_para['sweep_read_delay']['end'],
                        round(abs(test_para['sweep_read_delay']['end'] - test_para['sweep_read_delay']['start'])/test_para['sweep_read_delay']['step']) + 1)
        self.all_len = len(test_point)
        self.finish_len = 0
        t1 = threading.Thread(target=self.draw_line_chart,args=('t1','tau/ns','mod',))
        t1.start()
        for index in range(len(test_point)):
            if self.STOP_FLAG:
                break
            add_delay = test_point[index]
            self.dev_qcs.trigger_close()
            self.dev_ctp.trigger_close()
            xy_timelen = test_para['xy_pw']
            xy_delay = test_para['xy_delay']        
            self.set_qcs_freq(test_para['read_out_ch'], test_para['read_out_freq'], test_para['read_out_pw'], amp=test_para['read_out_amp'], delay=xy_delay + xy_timelen + add_delay + test_para['read_out_delay'], replay_continue=False)
            self.set_freq_xy_gauss(test_para['xy_ch'], test_para['xy_freq'], xy_timelen, amp=test_para['xy_amp'], delay=xy_delay) #
            ad_fixed_delay = round(260e-9*2.5e9)
            ad_trigger_delay = ad_fixed_delay + round(xy_timelen*2.5e9)  + round(xy_delay * 2.5e9) + round(test_para['read_in_delay']*2.5e9) +  round(add_delay * 2.5e9) 
            mul_start_phase = 0     #解模参数：初相
            mul_f_freq = test_para['read_out_freq'] * 1e6    #解模参数：频率，一般每个qubit对应不同频率
            mul_f_len = round(test_para['read_in_pw']*2.5e9)        #解模参数：单次解模shot数据样点数量
            mul_f = [[mul_start_phase, mul_f_freq]]    #解模参数列表，最多32组，对应一条线路上的32qubit
            self.dev_qcs.rd_adc_mul_data_ctrl(test_para['read_in_ch'],ad_trigger_delay,test_para['shots'],mul_f_len,mul_f)
            self.dev_qcs.trigger_ctrl(test_para['trig_mode'],trig_para['trigger_us'],test_para['shots'],trig_para['trigger_continue'])
            self.dev_ctp.trigger_open()
            MinJiangTools.sleep_ms(1)
            while 1:
                mul_data_bufe,read_data_len = self.dev_qcs.rd_adc_mul_data(test_para['read_in_ch'],0,test_para['shots'])
                if read_data_len != -1:
                    break
            for i in range(read_data_len):
                mul_data_bufe[i] = complex(mul_data_bufe[i])
            
            y_mod = np.abs(np.mean(mul_data_bufe) / mul_f_len / 8191)
            self.test_data['x'].append(add_delay*1e9)
            self.test_data['y'].append(y_mod)
            self.finish_len = index + 1
        MinJiangTools.write_data_to_csv(self.__path,self.file_name,self.env_para,test_para,trig_para,self.test_data)
        t1.join()
        MinJiangTools.T1_match(self.test_data['x'],self.test_data['y'],self.__path,self.file_name.replace('test','match'))

    def t2_test(self,test_para,trig_para):
        """T2测量

        Args:
            test_para (_type_): 实验测试参数
            trig_para (_type_): 实验Trig设备参数

        Returns:
            _type_: _description_
        """
        if self.dev_qcs is None or self.dev_ctp is None:
            return False
        self.__path = f'{self.data_save_path}/9_t2'
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        now_time = datetime.datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
        self.file_name = f'{self.env_para["qubit"]}_t2_test_{now_time}'
        self.test_data.clear()
        self.close_qcs_all_channels()
        self.dev_ctp.trigger_ctrl(test_para['trig_ch'],trig_para)
        self.dev_qcs.set_ch_offset(test_para['z_ch'], test_para['zbias']) 
        test_point = np.linspace(test_para['sweep_t_delay']['start'], test_para['sweep_t_delay']['end'],
                            round(abs(test_para['sweep_t_delay']['end'] - test_para['sweep_t_delay']['start'])/test_para['sweep_t_delay']['step']) + 1)
        self.all_len = len(test_point)
        self.finish_len = 0
        t1 = threading.Thread(target=self.draw_line_chart,args=('t2','t2(ns)','mod',))
        t1.start()
        for index in range(len(test_point)):
            if self.STOP_FLAG:
                break
            t = test_point[index]
            self.dev_qcs.trigger_close()
            self.dev_ctp.trigger_close()       
            xy_one_pluse_timelen = test_para['xy_pw']
            xy_delay = test_para['xy_delay']
            ad_fixed_delay = round(260e-9*2.5e9)
            xy_all_timelen = xy_one_pluse_timelen * 2 + t   
            self.set_qcs_freq(test_para['read_out_ch'], test_para['read_out_freq'], test_para['read_out_pw'], amp=test_para['read_out_amp'], delay=xy_delay + xy_all_timelen + test_para['read_out_delay'], replay_continue=False)
            self.set_xy_two_pluse_t_gauss(test_para['xy_ch'], np.round((test_para['xy_freq']-test_para['xy_freq_offset']),2), xy_one_pluse_timelen, amp=test_para['xy_amp'], t_s = t,t_delay=xy_delay)    
            ad_trigger_delay = ad_fixed_delay + round(xy_all_timelen*2.5e9)  + round(xy_delay * 2.5e9) + round(test_para['read_in_delay']*2.5e9) 
            shots = 2048
            mul_start_phase = 0     #解模参数：初相
            mul_f_freq = test_para['read_out_freq'] * 1e6    #解模参数：频率，一般每个qubit对应不同频率
            mul_f_len = round(test_para['read_in_pw']*2.5e9)        #解模参数：单次解模shot数据样点数量
            mul_f = [[mul_start_phase, mul_f_freq]]    #解模参数列表，最多32组，对应一条线路上的32qubit
            self.dev_qcs.rd_adc_mul_data_ctrl(test_para['read_in_ch'],ad_trigger_delay,shots,mul_f_len,mul_f)
            self.dev_qcs.trigger_ctrl(test_para['trig_mode'],trig_para['trigger_us'],test_para['shots'],trig_para['trigger_continue'])
            self.dev_ctp.trigger_open()
            # MinJiangTools.sleep_ms(1)
            while 1:
                mul_data_bufe,read_data_len = self.dev_qcs.rd_adc_mul_data(test_para['read_in_ch'],0,test_para['shots'])
                if read_data_len != -1:
                    break
            for i in range(read_data_len):
                mul_data_bufe[i] = complex(mul_data_bufe[i])
            y_mod = np.abs(np.mean(mul_data_bufe) / mul_f_len / 8191)
            self.test_data['x'].append(t*1e9)
            self.test_data['y'].append(y_mod)
            self.finish_len = index + 1
        MinJiangTools.write_data_to_csv(self.__path,self.file_name,self.env_para,test_para,trig_para,self.test_data)
        t1.join()
        MinJiangTools.T2_match(self.test_data['x'],self.test_data['y'],self.__path,self.file_name.replace('test','match'),test_para['xy_freq_offset'])

    def __get_01_stateIQ(self,test_para,trig_para):
        """获取01态IQ数据

        Args:
            test_para (_type_): 实验测试参数
            trig_para (_type_): 实验Trig设备参数

        Returns:
            _type_: 实部(list),虚部(list),MOD
        """
        self.close_qcs_all_channels()
        self.dev_qcs.trigger_close()
        self.dev_ctp.trigger_close()
        ad_samp = 2.5e9
        self.dev_qcs.set_ch_offset(test_para['z_ch'], test_para['zbias']) 
        self.set_qcs_freq(test_para['read_out_ch'], test_para['read_out_freq'], test_para['read_out_pw'], amp=test_para['read_out_amp'], delay=test_para['read_out_delay'] + test_para['xy_pw'] + test_para['xy_delay'] , replay_continue=False)
        if test_para['01_state'] == 0:# 0态-不给任何信号
            self.set_freq_xy_gauss(test_para['xy_ch'], test_para['xy_freq'], 
                            test_para['xy_pw'], test_para['xy_amp_0state'], test_para['xy_delay'] ) 
        elif test_para['01_state'] == 1: # 1态-XY给高斯脉冲
            self.set_freq_xy_gauss(test_para['xy_ch'], test_para['xy_freq'], 
                            test_para['xy_pw'], test_para['xy_amp_1state'], test_para['xy_delay'] ) 
        elif test_para['01_state'] == 2: # 叠加态
            self.set_freq_xy_gauss(test_para['xy_ch'], test_para['xy_freq'], 
                            test_para['xy_pw'], test_para['xy_amp_muxstate'], test_para['xy_delay'] )   
        else:
            pass
        ad_fixed_delay =260e-9 
        ad_trigger_delay = round((ad_fixed_delay + test_para['xy_pw'] + test_para['xy_delay'] 
                                +  test_para['read_in_delay'] ) * ad_samp)           #解模次数
        mul_start_phase = 0    #解模参数：初相
        mul_f_freq = test_para['read_out_freq'] * 1e6    #解模参数：频率，一般每个qubit对应不同频率
        mul_f_len = round(test_para['read_in_pw']  *2.5e9)       # 解模参数：单次解模shot数据样点数量 
        mul_f = [[mul_start_phase, mul_f_freq]]    #解模参数列表，最多32组，对应一条线路上的32qubit
        self.dev_qcs.rd_adc_mul_data_ctrl(test_para['read_in_ch'],ad_trigger_delay,test_para['shots'],mul_f_len,mul_f)
        self.dev_qcs.trigger_ctrl(test_para['trig_mode'],trig_para['trigger_us'],test_para['shots'],trig_para['trigger_continue'])
        self.dev_ctp.trigger_ctrl(test_para['trig_ch'],trig_para)
        self.dev_ctp.trigger_open()
        # MinJiangTools.sleep_ms(1)
        while 1:
            mul_data_bufe,read_data_len = self.dev_qcs.rd_adc_mul_data(test_para['read_in_ch'],0,test_para['shots'])
            if read_data_len != -1:
                break
        real,imag=[],[]    
        for i in range(read_data_len):
            mul_data_bufe[i] = complex(mul_data_bufe[i])
            real.append(mul_data_bufe[i].real/mul_f_len)
            imag.append(mul_data_bufe[i].imag/mul_f_len)
        return real,imag,np.abs(np.mean(mul_data_bufe)/mul_f_len/(2**13-1))
    
    def qubit_01_stateIQ(self,test_para,trig_para):
        """01态IQ图

        Args:
            test_para (_type_): 实验测试参数
            trig_para (_type_): 实验Trig设备参数

        Returns:
            _type_: _description_
        """
        if self.dev_qcs is None or self.dev_ctp is None:
            return False
        self.__path = f'{self.data_save_path}/10_mod_ref'
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        now_time = datetime.datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
        self.test_data.clear()

        test_para["01_state"] = 0
        x0,y0,mod0 = self.__get_01_stateIQ(test_para,trig_para)
        test_para["01_state"] = 1
        x1,y1,mod1 = self.__get_01_stateIQ(test_para,trig_para)
        for  i in range(len(x0)):
            self.test_data['x0'].append(x0[i])
            self.test_data['y0'].append(y0[i])
            self.test_data['x1'].append(x1[i])
            self.test_data['y1'].append(y1[i])

        self.file_name = f'{self.env_para["qubit"]}_mod_{now_time}'
        MinJiangTools.write_data_to_csv(self.__path,self.file_name,self.env_para,test_para,trig_para,self.test_data)

        plt.figure(figsize = (8, 8))
        ax = plt.subplot(2,2,1)
        ax.scatter(x0, y0, s = 9, c = 'red', label='|0⟩')
        ax.scatter(x1, y1, s = 9, c = 'blue', label='|1⟩')
        ax.legend(loc='upper right')

        ax = plt.subplot(2,2,2)
        ax.text(0.2, 0.6, f"mod0:{mod0}")
        ax.text(0.2, 0.5, f"mod1:{mod1}")

        ax = plt.subplot(2,2,3)
        ax.scatter(x0, y0, s = 9, c = 'red', label='|0⟩')
        ax.legend( loc='upper right')

        ax = plt.subplot(2,2,4)
        ax.scatter(x1, y1,  s = 9, c = 'blue', label='|1⟩')
        ax.legend(loc='upper right')

        plt.savefig(f'{self.__path}/{self.file_name}.png',bbox_inches='tight')
        plt.show()
        MinJiangTools.fidelity(np.asarray(x0),np.asarray(y0),np.asarray(x1),np.asarray(y1),self.__path,self.file_name)
    
    def __sweep_freq_01state(self,qubit_st,test_para,trig_para):
        """01态扫腔频测试函数

        Args:
            qubit_st (_type_): qubit状态 0即0态,1即1态
            test_para (_type_): 实验测试参数
            trig_para (_type_): 实验Trig设备参数

        Returns:
            _type_: _description_
        """
        self.close_qcs_all_channels()
        self.dev_qcs.set_ch_offset(test_para['z_ch'],test_para['zbias'])
        temp_data = [] 
        y_mod = []
        self.dev_ctp.trigger_ctrl(test_para['trig_ch'], trig_para)
        x = np.around(np.linspace(test_para['sweep_freq']['start'], test_para['sweep_freq']['end'], 
                                round(abs(test_para['sweep_freq']['end'] - test_para['sweep_freq']['start'])/test_para['sweep_freq']['step']) + 1), 2)
        if qubit_st == 0:
            amp = 0
        else:
            amp =test_para['xy_amp']
        for freq in x:
            self.dev_qcs.trigger_close()
            self.dev_ctp.trigger_close()
            self.set_qcs_freq(test_para['read_out_ch'], freq, test_para['read_out_pw'], amp=test_para['read_out_amp'],
                               delay=test_para['read_out_delay'] + test_para['xy_pw'] + test_para['xy_delay'] , replay_continue=False)
            self.set_freq_xy_gauss(test_para['xy_ch'], test_para['xy_freq'], test_para['xy_pw'], amp, test_para['xy_delay'])
            ad_fixed_delay =260e-9 
            ad_trigger_delay = round((ad_fixed_delay + test_para['xy_pw'] + test_para['xy_delay'] 
                                    +  test_para['read_in_delay'] ) * 2.5e9) 
            mul_start_phase = 0     #解模参数：初相
            mul_f_freq = (freq) * 1e6    #解模参数：频率，一般每个qubit对应不同频率
            mul_f_len = round(test_para['read_in_pw'] * 2.5e9)       #解模参数：单次解模shot数据样点数量 
            mul_f = [[mul_start_phase, mul_f_freq]]    #解模参数列表，最多32组，对应一条线路上的32qubit
            
            self.dev_qcs.rd_adc_mul_data_ctrl(test_para['read_in_ch'],ad_trigger_delay,test_para['shots'],mul_f_len,mul_f)
            self.dev_qcs.trigger_ctrl(test_para['trig_mode'],trig_para['trigger_us'],test_para['shots'],trig_para['trigger_continue'])
            self.dev_ctp.trigger_open()
            # MinJiangTools.sleep_ms(1))
            while 1:
                mul_data_bufe,read_data_len = self.dev_qcs.rd_adc_mul_data(test_para['read_in_ch'],0,test_para['shots'])
                if read_data_len != -1:
                    break
            for i in range(read_data_len):
                mul_data_bufe[i] = complex(mul_data_bufe[i])
            temp_data.append(np.mean(mul_data_bufe))
            y_mod = np.abs(np.asarray(temp_data) /mul_f_len / (2**13-1))
        return x, y_mod,temp_data

    def sweep01_cavity_freq(self,test_para,trig_para):
        """01态扫腔频

        Args:
            test_para (_type_): 实验测试参数
            trig_para (_type_): 实验Trig设备参数

        Returns:
            _type_: _description_
        """
        if self.dev_qcs is None or self.dev_ctp is None:
            return False
        self.__path = f'{self.data_save_path}/11_sweep01_cavity_freq'
        if not os.path.exists(self.__path):
            os.makedirs(self.__path)
        now_time = datetime.datetime.now().strftime('%Y.%m.%d_%H.%M.%S')
        self.file_name = f'{self.env_para["qubit"]}_01_cavity_freq_{now_time}'

        self.test_data.clear()
        I0, Q0, res_complex0 = self.__sweep_freq_01state(0,test_para,trig_para)
        I1, Q1, res_complex1 = self.__sweep_freq_01state(1,test_para,trig_para)
        delt_Q = np.abs(Q1-Q0)
        delt_complex = np.abs(res_complex1-res_complex0)
        for  i in range(len(I0)):
            self.test_data['I0'].append(I0[i])
            self.test_data['Q0'].append(Q0[i])
            self.test_data['I1'].append(I1[i])
            self.test_data['Q1'].append(Q1[i])

        plt.figure(figsize = (7, 5))
        plt.title("sweep01_cavity_freq")
        plt.xlabel('MHz')
        plt.ylabel('mod')
        plt.plot(I0, Q0, label='|0⟩')
        plt.plot(I1, Q1, label='|1⟩')
        plt.plot(I1, delt_Q, label='|1⟩-|0⟩')
        plt.plot(I1, delt_complex, label='abs(|1⟩-|0⟩)')
        plt.legend(loc='upper right')
        plt.savefig(f'{self.__path}/{self.file_name}.png',bbox_inches='tight')
        plt.show()
        MinJiangTools.write_data_to_csv(self.__path,self.file_name,self.env_para,test_para,trig_para,self.test_data)