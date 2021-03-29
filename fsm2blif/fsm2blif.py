#!/usr/bin/python
# -*- coding: UTF-8 -*-
#
# для печати
from __future__ import print_function

# для параметров
import sys
import argparse

# для работы с векторами и матрицами
import numpy as np
import math

# разборщик параметров
def createParamParser ():
    parser = argparse.ArgumentParser()
    parser.add_argument('fsmFile', type = str, action = 'store', help = 'path to the file with an FSM in KITIDIS format')
    parser.add_argument('resultFile', type = str, action = 'store', help = 'path to file, where to store the result')
    return parser

if __name__ == '__main__':
    parser = createParamParser()
    args = parser.parse_args()
    
    fsm_file = open(args.fsmFile, 'r')
    res_file = open(args.resultFile, 'w')
    
    res_file.write('.model' + ' FSM_' + args.fsmFile  + '\n')
    
    # F 0
    fsm_file.readline()
    #TODO check the F 0
    
    # s 16 => 4 bits
    line = fsm_file.readline()
    c_line = line.split()
    # print ('c_line is ', c_line)
    states_num_bit = (int(c_line[1]) - 1).bit_length()
    # print('Number of state vars:', states_num_bit)
    
    # i 4 => 2
    line = fsm_file.readline()
    c_line = line.split()
    inputs_num_bit = (int(c_line[1]) - 1).bit_length()
    # print('Number of input vars:', inputs_num_bit)
    
    # o 4 => 2
    line = fsm_file.readline()
    c_line = line.split()
    outputs_num_bit = (int(c_line[1]) - 1).bit_length()
    # print('Number of output vars:', outputs_num_bit)
    
    # n0 0
    line = fsm_file.readline()
    c_line = line.split()
    initial_state = int(c_line[1])
    # print('Initial state:', initial_state)

    
    # p 64
    line = fsm_file.readline()
    c_line = line.split()
    trans_num = int(c_line[1])
    # print('Transitions number:', trans_num)
    
    res_file.write('.inputs ')
    for i in range(inputs_num_bit - 1):
        res_file.write('x' + str(i) + ' ')
    res_file.write('x' + str(inputs_num_bit - 1) + '\n')

    res_file.write('.outputs ')
    for i in range(outputs_num_bit - 1):
        res_file.write('y' + str(i) + ' ')
    res_file.write('y' + str(outputs_num_bit - 1) + '\n')
    
    res_file.write('\n')
    for i in range(states_num_bit):
        res_file.write('.latch ns' + str(i) + ' cs' + str(i) + ' 0\n')
    
    # список списков вектор из множеств M1. states_num_bit и outputs_num_bit -- это количество битов!!!
    # для каждой комбинации состояния и выходного символа свой список (входных значений, обеспечивающих данный выход в данном состоянии)
    ns_out_list = [[] for i in range(states_num_bit + outputs_num_bit)]
    
    # ожидаем строки вида <s> <i> <s> <o>
    
    # для случая константы 0
    any_input = '-'*(states_num_bit + inputs_num_bit)
    
    for i in range(trans_num):
        line = fsm_file.readline()
        if (line == ''):
            break
        
        c_list = line.split()                   # разобьём на отдельные "слова"
        
        st_word = (bin(int(c_list[0]))[2:])     #двоичный вид нач.сост
        st_lngth = len(st_word)                 #длина двоичного слова
        in_word = (bin(int(c_list[1]))[2:])     #двоичный вид вх.символа
        in_lngth = len(in_word)
        cs_inp_word = (states_num_bit - st_lngth)*'0' + st_word + (inputs_num_bit - in_lngth)*'0' + in_word
        
        nx_word = (bin(int(c_list[2]))[2:])
        nx_lngth = len(nx_word)
        ou_word = (bin(int(c_list[3]))[2:])
        ou_lngth = len(ou_word)
        ns_out_word = (states_num_bit - nx_lngth)*'0' + nx_word + (outputs_num_bit - ou_lngth)*'0' + ou_word
        
        for j in range(len(ns_out_word)):
            if (ns_out_word[j] == '1'):
                ns_out_list[j].append(cs_inp_word)
        
        #print (
        #    (states_num_bit - st_lngth)*'0' + st_word + ' ' + 
        #    (inputs_num_bit - in_lngth)*'0' + in_word + '|' + 
        #    (states_num_bit - nx_lngth)*'0' + nx_word + ' ' + 
        #    (outputs_num_bit - ou_lngth)*'0' + ou_word
        #)
        # print(cs_inp_word + '|' + ns_out_word)

    # входы (биты состояний и биты входных символов)
    names_string = '.names'
    for j in range(states_num_bit):
        names_string = names_string + ' cs' + str(j)
    for j in range(inputs_num_bit):
        names_string = names_string + ' x' + str(j)
    
    for i in range(states_num_bit):
        res_file.write('\n' + names_string)
        res_file.write(' ns' + str(i) + '\n')
        if (len(ns_out_list[i]) == 0):
            res_file.write(any_input + ' 0')
        else:
            for jj in ns_out_list[i]:
                res_file.write(jj + ' 1\n')
    
    for i in range(outputs_num_bit):
        res_file.write('\n' + names_string)
        res_file.write(' y' + str(i) + '\n')
        if (len(ns_out_list[i + states_num_bit]) == 0):
            res_file.write(any_input + ' 0')
        else:
            for jj in ns_out_list[i + states_num_bit]:  #i заменено на i + states_num_bit
                res_file.write(jj + ' 1\n')

    res_file.write('.end')

    fsm_file.close()
    res_file.close()
