#!/usr/local/bin/python
# -*- coding: UTF-8 -*-
#
## PYTHON 3


# для параметров
import sys
import argparse

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
    
    # F 0
    fsm_file.readline()
    #TODO check the F 0
    
    # s 16 => 4 bits
    line = fsm_file.readline()
    c_line = line.split()
    states_num = int(c_line[1])
    print('Number of states: {0}'.format(states_num))
    
    # i 4 => 2
    line = fsm_file.readline()
    c_line = line.split()
    inputs_num = int(c_line[1])
    print("Number of inputs: {0}".format(inputs_num))
    
    # o 4 => 2
    line = fsm_file.readline()
    c_line = line.split()
    outputs_num = int(c_line[1])
    print('Number of outputs: {0}'.format(outputs_num))
    
    # n0 0
    line = fsm_file.readline()
    c_line = line.split()
    initial_state = int(c_line[1])
    print('Initial state: {0}'.format(initial_state))

    
    # p 64
    line = fsm_file.readline()
    c_line = line.split()
    trans_num = int(c_line[1])
    print('Transitions number: ', trans_num)
    
    table = [[[] for j in range(states_num)] for i in range(inputs_num)]
	
    for i in range(trans_num):
        line = fsm_file.readline()
        if (line == ''):
            break
        c_list = line.split() # разобьём на отдельные "слова"
        #s i s o
        table[int(c_list[1])][int(c_list[0])] = (int(c_list[2]), int(c_list[3]))
    for i in range(inputs_num):
        for j in range(states_num):
            res_file.write("{0}/{1}\t".format(table[i][j][0], table[i][j][1]))
        res_file.write("\n")

    fsm_file.close()
    res_file.close()
