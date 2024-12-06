# -*- coding: utf-8 -*-
'''
@Project : zwdx_minjiang
@File : __init__.py
@description : Packaging requires files
@Author : anonymous
@Date : 2024.11.01
'''
import os
import csv
import ctypes
import numpy as np
from pathlib import Path
from scipy.stats import norm
import matplotlib.pyplot as plt
 
path = str(Path(__file__).parent/'c_method.so')
c_method_delay=ctypes.cdll.LoadLibrary(path)

def sleep_ms(ms:int):
    assert ms >= 1
    c_method_delay.delay_ms(int(ms))

def write_data_to_csv(path,file_name,env_para,test_para,trig_para,mdata):
    """ 将数据写到csv文件

    Args:
        path (_type_): csv文件的存储路径
        file_name (_type_): csv文件的存储名称
        env_para (_type_): 实验环境参数
        test_para (_type_): 实验测试参数(含QCS参数)
        trig_para (_type_): 实验Trig设备参数
        data (_type_): 要存储的数据
    """
    with open(f'{path}/{file_name}.csv','w',newline='') as f:
        writer = csv.writer(f)
        writer.writerow([f'Environmental parameter:'])
        for i in env_para:
            writer.writerow([i,env_para[i]])

        writer.writerow([f'Test parameter:'])
        for j in test_para:
            writer.writerow([j,test_para[j]])

        writer.writerow([f'Trig parameter:'])
        for k in trig_para:
            writer.writerow([k,trig_para[k]]) 

        writer.writerow([f'Test Data:'])
        key_list = list(mdata.keys())
        writer.writerow(key_list)
        if len(key_list) == 2:
            for ix in range(len(mdata[key_list[0]])):
                row = [mdata[key_list[0]][ix],mdata[key_list[1]][ix]]
                writer.writerow(row)
        elif len(key_list) == 3:
            for ix in range(len(mdata[key_list[0]])):
                for iy in range(len(mdata[key_list[1]])):
                    row = [mdata[key_list[0]][ix],mdata[key_list[1]][iy],mdata[key_list[2]][ix][iy]]
                    writer.writerow(row)
        elif len(key_list) == 4:
            for ix in range(len(mdata[key_list[0]])):
                row = [mdata[key_list[0]][ix],mdata[key_list[1]][ix],mdata[key_list[2]][ix],mdata[key_list[3]][ix]]
                writer.writerow(row)
        

def func_to_S(func, beta_list, beta_step_list, x_list, y_list):
    """
        计算残差平方和
        beta_list: 当前参数的估计值。
        beta_diff_step_list: 差分步长列表
        x_list: x 数据。
        y_list: 真实的 y 数据。
        S: 残差平方和
    """    
    r_list = func(beta_list, x_list) - y_list
    S = (np.sqrt(np.mean(r_list**2)))**2  # 计算均方根并平方
    return r_list, S

def func_to_J(func, beta_list, beta_step_list, x_list, y_list):
    """
    计算 Jacobian 矩阵和残差
    参数：
    func: 这是一个函数，接受参数列表和 x 数据，并返回相应的 y 值。
    beta_list: 当前参数的估计值。
    beta_diff_step_list: 差分步长列表，用于计算 Jacobian。
    x_list: 输入的 x 数据。
    y_list: 实际的 y 数据。
    返回值：
    J_matrix: Jacobian 矩阵，表示模型对参数的敏感度。
    r_list: 残差，计算为实际 y 值与模型预测 y 值之间的差值。
    残差的平方和（用于评估模型拟合的好坏）。
    """    
    r_list = func(beta_list, x_list) - y_list
    S = (np.sqrt(np.mean(r_list**2)))**2
    m = len(beta_list)
    n = len(r_list)
    J_matrix = np.zeros((n, m))
    for cnt_beta in range(m):
        vector_temp = np.zeros(m)
        vector_temp[cnt_beta] = 1
        r_list_diff = func(beta_list + vector_temp * beta_step_list, x_list) - y_list
        J_column = (r_list_diff - r_list) / beta_step_list[cnt_beta]
        J_matrix[:, cnt_beta] = J_column
    return J_matrix, r_list, S

def gradient_descend_LM(func, beta_list, beta_diff_step_list, x_list, y_list, figure_num):
    # 配置
    traditional_lambda_option = 0
    lambda_0 = 100  # 初始lambda
    traditional_lambda_multiple = 10
    decreasing_multiple = 5
    increasing_multiple = 2
    max_iteration_num = 40

    # 初始化
    lambda_temp = lambda_0

    # 迭代
    REC_lambda_temp = []
    REC_S_temp = []
    REC_delta_S = []
    REC_step_length = []

    for cnt in range(max_iteration_num):  # Python的索引从0开始
        plt.pause(0.01)  # 用于观察曲线变化规律
        y_list_temp = func(beta_list, x_list)
        J_matrix, r_list, S = func_to_J(func, beta_list, beta_diff_step_list, x_list, y_list)
        J_sqr = np.dot(J_matrix.T, J_matrix)
        delta_beta_list_0 = -np.linalg.inv(J_sqr + lambda_temp * np.eye(len(J_sqr))) @ J_matrix.T @ r_list

        if np.sum(np.isnan(delta_beta_list_0)) > 0:  # 防止1/0情况发生
            raise ValueError('NaN due to inv(). Check the initial guess.')

        # 若传统lambda选择
        if traditional_lambda_option == 1:
            beta_list_temp = beta_list + delta_beta_list_0
            _, S_temp = func_to_S(func, beta_list_temp, beta_diff_step_list, x_list, y_list)

            while S_temp > S:  # 新残差平方和大于原残差平方和
                lambda_temp *= traditional_lambda_multiple
                J_sqr = np.dot(J_matrix.T, J_matrix)
                delta_beta_list_0 = -np.linalg.inv(J_sqr + lambda_temp * np.eye(len(J_sqr))) @ J_matrix.T @ r_list

                if np.sum(np.isnan(delta_beta_list_0)) > 0:
                    raise ValueError('NaN due to inv(). Check the initial guess.')

                beta_list_temp = beta_list + delta_beta_list_0
                _, S_temp = func_to_S(func, beta_list_temp, beta_diff_step_list, x_list, y_list)

            beta_list = beta_list_temp
            lambda_temp /= traditional_lambda_multiple  # 成功步进后，减小lambda
        else:  # 若delay gratification
            beta_list_temp = beta_list + delta_beta_list_0
            _, S_temp = func_to_S(func, beta_list_temp, beta_diff_step_list, x_list, y_list)
            beta_list = beta_list_temp  # 按照预期步进

            if S_temp > S:
                lambda_temp *= increasing_multiple  # 增大lambda
            else:
                lambda_temp /= decreasing_multiple  # 减小lambda

        REC_lambda_temp.append(lambda_temp)
        REC_S_temp.append(S_temp)

        if cnt == 0:
            REC_delta_S.append(1)
        else:
            REC_delta_S.append(REC_S_temp[cnt] / REC_S_temp[cnt - 1])

        REC_step_length.append(np.sqrt(np.mean(delta_beta_list_0**2)))

    # 结果评估
    _, S_result = func_to_S(func, beta_list, beta_diff_step_list, x_list, y_list)

    return beta_list, S_result, cnt, lambda_temp

def T1_match(x,y,data_save_path,file_name):
    x_list_original = x
    y_list_original = y

    # 数据归一化
    x_normal = np.max(x_list_original) - np.min(x_list_original)
    x_list = x_list_original / x_normal
    y_list = y_list_original 

    # Levenberg-Marquardt 方法
    beta_list = np.array([y_list[0] - y_list[-1], -((x_list[-1] - x_list[0]) / 2) ** -1, y_list[-1]])  # 初始猜测
    beta_diff_step_list = np.array([1e-4, 1e-4, 1e-4])  # 差分间隔

    def T1_func(beta_list, x):
        return beta_list[0] * np.exp(beta_list[1] * x) + beta_list[2]
    beta_list, S_result, cnt, lambda_temp = gradient_descend_LM(T1_func, beta_list, beta_diff_step_list, x_list, y_list, 2)

    t1 = np.round(((-beta_list[1] / x_normal) ** -1 )/1000,4) #计算T1时间
    y_list_temp = T1_func(beta_list, x_list) #最后的拟合数据

    plt.figure(figsize=(7,5))
    plt.plot(x_list * x_normal, y_list, 'd', label='exp.', color='b')            
    plt.plot(x_list * x_normal, y_list_temp, label='fitted', color='r')
    plt.title(f'T1 match')
    plt.xlabel('times(ns)')
    plt.ylabel('Amplitude')
    plt.text(max(x)/2.5, max(y), f"Time:{t1}us")
    plt.legend(loc='upper right')
    plt.savefig(f'{data_save_path}/{file_name}.png', dpi=800)
    plt.show()

def T2_match(x,y,data_save_path,file_name,xy_freq_offset):
    
    x_list_original = x
    y_list_original = y

    # 数据归一化
    x_normal = np.max(x_list_original) - np.min(x_list_original)
    y_normal = np.max(y_list_original) - np.min(y_list_original)
    x_list = x_list_original / x_normal
    y_list = y_list_original / y_normal

    # Levenberg-Marquardt 方法
    index_min = np.argmin(y_list)  # y 最小的 x 索引
    index_max = np.argmax(y_list)   # y 最大的 x 索引

    beta_list = np.array([
        y_list[0] - y_list[-1],
        -((x_list[-1] - x_list[0]) / 2) ** -1,
        y_list[-1],
        (2 * abs(x_list[index_max] - x_list[index_min])) ** -1,
        0
    ])
    beta_diff_step_list = np.array([1e-4] * 5)  # 差分间隔

    def T2_func(beta_list, x):
        return beta_list[0] * np.exp(beta_list[1] * x) * np.cos(2 * np.pi * beta_list[3] * x + beta_list[4]) + beta_list[2]
    # 执行 Levenberg-Marquardt 方法
    beta_list, S_result, cnt, lambda_temp = gradient_descend_LM(T2_func, beta_list, beta_diff_step_list, x_list, y_list, 2)

    y_list_temp = T2_func(beta_list, x_list) #最后的拟合数据
    t2 = np.round((-beta_list[1] / x_normal) ** -1,4) #计算T2时间
    plt.figure(figsize=(7,5))
    plt.plot(x_list * x_normal, y_list, 'd', label='exp.', color='b')            
    plt.plot(x_list * x_normal, y_list_temp, label='fitted', color='r')
    plt.title(f'T2 match')
    plt.xlabel('times(ns)')
    plt.ylabel('Amplitude')
    plt.text(max(x)/3, max(y_list), f"Time:{t2}us \n Amp:{beta_list[0]} \n Freq:{beta_list[3]}MHz \n Phase:{beta_list[4]} \n ▲Freq:{beta_list[3]-xy_freq_offset}")
    plt.legend(loc='upper right')
    plt.savefig(f'{data_save_path}/{file_name}.png', dpi=800)
    plt.show()

def  fidelity(x0,y0,x1,y1,data_save_path,file_name):
    complex_set_0 = x0 + y0 * 1j
    complex_set_1 = x1 + y1 * 1j
    # 数据可视化
    plt.figure(figsize=(7,5))
    plt.scatter(np.real(complex_set_0), np.imag(complex_set_0), s=9, label='0')
    plt.scatter(np.real(complex_set_1), np.imag(complex_set_1), s=9, label='1')
    plt.legend(loc='upper right')
    plt.grid()
    plt.axis('equal')

    # 寻找圆心（粗略）
    center_0_estimate = np.mean(complex_set_0)
    center_1_estimate = np.mean(complex_set_1)  # 注意：由于衰减，这个估计并不是center_1的无偏估计
    plt.scatter(np.real(center_0_estimate), np.imag(center_0_estimate), s=72, marker='D', label='center 0 estimate')
    plt.scatter(np.real(center_1_estimate), np.imag(center_1_estimate), s=72, marker='D', label='center 1 estimate')

    # 旋转坐标轴
    delta_phi = -np.angle(center_1_estimate - center_0_estimate)
    complex_set_0_rotated = complex_set_0 * np.exp(1j * delta_phi)
    complex_set_1_rotated = complex_set_1 * np.exp(1j * delta_phi)
    center_0_estimate_rotated = center_0_estimate * np.exp(1j * delta_phi)
    center_1_estimate_rotated = center_1_estimate * np.exp(1j * delta_phi)

    # 数据归一化
    data_0_original = np.real(complex_set_0_rotated)
    data_1_original = np.real(complex_set_1_rotated)
    min_data = min(np.min(data_0_original), np.min(data_1_original))
    max_data = max(np.max(data_0_original), np.max(data_1_original))
    data_normal = max_data - min_data
    data_0 = data_0_original / data_normal
    data_1 = data_1_original / data_normal

    # 旋转后的x轴上的直方图
    hist_0, bins_0 = np.histogram(data_0, bins=30, density=True)
    hist_1, bins_1 = np.histogram(data_1, bins=30, density=True)
    # 计算直方图的中心
    line_0_x = (bins_0[:-1] + np.diff(bins_0) / 2)
    line_0_y = hist_0
    line_1_x = (bins_1[:-1] + np.diff(bins_1) / 2)
    line_1_y = hist_1

    # 非线性拟合 - 0态初始猜测
    std_0 = np.std(data_0)
    beta_list = [1 / (np.sqrt(2 * np.pi) * std_0), np.mean(data_0), std_0]
    beta_diff_step_list = [1e-4, 1e-4, 1e-4]  # 差分间隔

    #拟合函数
    def func_gaussian(beta_list, x):
        return beta_list[0] * np.exp(-((x - beta_list[1]) / (np.sqrt(2) * beta_list[2]))**2)

    def func_double_gaussian(beta_list, x):
        return  (beta_list[0] * np.exp(-((x - beta_list[1]) / (np.sqrt(2) * beta_list[2]))**2) + beta_list[3] * np.exp(-((x - beta_list[4]) / (np.sqrt(2) * beta_list[5]))**2))

    # 执行拟合
    beta_list, S_result, cnt, lambda_temp = gradient_descend_LM(func_gaussian, beta_list, beta_diff_step_list, line_0_x, line_0_y, 30)

    # 0态双高斯初始参数猜测
    beta_list_q0 = np.array([1 / (np.sqrt(2 * np.pi) * std_0), np.mean(data_0), std_0, 
                            0 / (np.sqrt(2 * np.pi) * std_0), np.mean(data_1), std_0])
    beta_diff_step_list_q0 = np.array([1e-4, 1e-4, 1e-4, 1e-4, 1e-4, 1e-4])
    # 进行拟合
    beta_list_q0, S_result_q0, cnt_q0, lambda_temp_q0 = gradient_descend_LM(func_double_gaussian, beta_list_q0, beta_diff_step_list_q0, line_0_x, line_0_y, 35)
    
    diff_step_modified_option = 0
    # 精细调整差分间隔的可选项
    if diff_step_modified_option == 1:
        beta_diff_step_list /= 100
        beta_list_2, S_result_2, cnt_2, lambda_temp_2 = gradient_descend_LM(func_gaussian, beta_list, beta_diff_step_list, line_0_x, line_0_y, 40)
        S_result_diff_1 = S_result_2 - S_result

        beta_diff_step_list /= 100
        beta_list_3, S_result_3, cnt_3, lambda_temp_3 = gradient_descend_LM(func_gaussian, beta_list, beta_diff_step_list, line_0_x, line_0_y, 50)
        S_result_diff_2 = S_result_3 - S_result_2

    # 1态分布初始猜测
    beta_list_q1 = np.array([1 / (np.sqrt(2 * np.pi) * std_0), np.mean(data_1), std_0, 
                            0 / (np.sqrt(2 * np.pi) * std_0), np.mean(data_0), std_0])
    beta_diff_step_list_q1 = np.array([1e-4, 1e-4, 1e-4, 1e-4, 1e-4, 1e-4])

    beta_list_q1, S_result_q1, cnt_q1, lambda_temp_q1 = gradient_descend_LM(func_double_gaussian, beta_list_q1, beta_diff_step_list_q1, line_1_x, line_1_y, 60)

    if diff_step_modified_option == 1:
        beta_diff_step_list_q1 /= 100
        beta_list_q1_2, S_result_q1_2, cnt_q1_2, lambda_temp_q1_2 = gradient_descend_LM(func_double_gaussian, beta_list_q1, beta_diff_step_list_q1, line_1_x, line_1_y, 70)
        S_result_diff_q1 = S_result_q1_2 - S_result_q1

        beta_diff_step_list_q1 /= 100
        beta_list_q1_3, S_result_q1_3, cnt_q1_3, lambda_temp_q1_3 = gradient_descend_LM(func_double_gaussian, beta_list_q1_2, beta_diff_step_list_q1, line_1_x, line_1_y, 80)
        S_result_diff_q1_2 = S_result_q1_3 - S_result_q1_2

    # 保真度和衰变概率估计
    x_distinct_estimate = (beta_list[1] + beta_list_q1[1]) / 2  # 拆分坐标
    r_distinct_estimate = abs(beta_list[1] - beta_list_q1[1]) / 2  # 中心距离
    decay_probability_1to0_estimate = (beta_list_q1[3] * beta_list_q1[5] * np.sqrt(2 * np.pi)) / \
        ((beta_list_q1[0] * beta_list_q1[2] * np.sqrt(2 * np.pi)) + (beta_list_q1[3] * beta_list_q1[5] * np.sqrt(2 * np.pi)))

    decay_probability_0to1_estimate = (beta_list_q0[3] * beta_list_q0[5] * np.sqrt(2 * np.pi)) / \
        ((beta_list_q0[0] * beta_list_q0[2] * np.sqrt(2 * np.pi)) + (beta_list_q0[3] * beta_list_q0[5] * np.sqrt(2 * np.pi)))
    #保真度结果
    e_0_intrinsic_estimate = np.around(norm.cdf(abs(x_distinct_estimate - beta_list[1]), 0, beta_list[2]),4)
    e_1_intrinsic_estimate = np.around(norm.cdf(abs(x_distinct_estimate - beta_list_q1[1]), 0, beta_list_q1[2]),4)
    e_1_estimate = np.around(e_1_intrinsic_estimate * (1 - decay_probability_1to0_estimate),4)
    e_0_estimate = np.around(e_0_intrinsic_estimate * (1 - decay_probability_0to1_estimate),4)

    # 拟合的高斯曲线
    plt.figure(figsize=(7,5))  # 拟合的高斯曲线
    plt.hist(data_0, bins=30, density=True, alpha=0.5)
    plt.hist(data_1, bins=30, density=True, alpha=0.5)
    plt.plot(line_0_x, line_0_y, label='line of hist 0')
    plt.plot(line_1_x, line_1_y, label='line of hist 1')
    x_vals = np.linspace(np.min(line_0_x), np.max(line_0_x), 100)
    # plt.plot(x_vals, func_gaussian(beta_list, x_vals), linewidth=4, label='0 fitted single_gaussian')
    plt.plot(x_vals, func_double_gaussian(beta_list_q0, x_vals), linewidth=4, label='0 fitted double_gaussian')
    plt.plot(x_vals, func_double_gaussian(beta_list_q1, x_vals), linewidth=4, label='1 fitted double_gaussian')
    plt.legend(loc='upper right')
    plt.title(f'QUbit 0fidelity :{e_0_estimate} 1fidelity :{e_1_estimate}')
    # plt.gcf().set_size_inches(15/2.54, 9/2.54)  # 转换为英寸
    plt.savefig(f"{data_save_path}/{file_name.replace('mod','fidelity_res')}.png", dpi=800)
    # 2倍标准差圆（仅示意）

    plt.figure(figsize=(7,5))
    plt.scatter(np.real(complex_set_0_rotated), np.imag(complex_set_0_rotated), s=9, label='0 rotated')
    plt.scatter(np.real(complex_set_1_rotated), np.imag(complex_set_1_rotated), s=9, label='1 rotated')
    plt.scatter(np.real(center_0_estimate_rotated), np.imag(center_0_estimate_rotated), s=72, marker='D', label='center 0 estimate rotated')
    plt.scatter(np.real(center_1_estimate_rotated), np.imag(center_1_estimate_rotated), s=72, marker='D', label='center 1 estimate rotated')
    center_0_x = beta_list[1] * data_normal
    center_0_y = np.mean(np.imag(complex_set_0_rotated))
    r_0 = beta_list[2] * data_normal
    phi_list = np.arange(0, 2 * np.pi, 0.01)
    x_temp = center_0_x + 2 * r_0 * np.cos(phi_list)
    y_temp = center_0_y + 2 * r_0 * np.sin(phi_list)
    plt.plot(x_temp, y_temp, linewidth=4)
    center_1_x = beta_list_q1[1] * data_normal
    center_1_y = np.mean(np.imag(complex_set_1_rotated))
    r_1 = beta_list_q1[2] * data_normal
    x_temp = center_1_x + 2 * r_1 * np.cos(phi_list)
    y_temp = center_1_y + 2 * r_1 * np.sin(phi_list)
    plt.plot(x_temp, y_temp, linewidth=4)
    plt.legend(loc='upper right')
    plt.grid()
    plt.axis('equal')
    plt.title(f'QUbit Scatter diagram')
    # plt.gcf().set_size_inches(15/2.54, 9/2.54)  # 转换为英寸
    plt.savefig(f"{data_save_path}/{file_name.replace('mod','scatter_diagram')}.png", dpi=800)
    plt.show()