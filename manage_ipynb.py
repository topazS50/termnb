#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import subprocess


BAR  = '=========================='
OUT  = '======= OUT =============='
LINE = '--------------------------'
def get_user_input():
    uinput = raw_input('termnb>>')
    return uinput

def show_cell(cell):
    if cell['source'] != []:
        source_string = reduce(lambda a, b: a + b, cell['source'])
        print BAR
        print source_string.rstrip('\n')
        print LINE

def show_all(js_ipynb):
    for cell in js_ipynb['cells']:
        show_cell(cell)


def controller(cells):
    id_current_cell = 0

    while id_current_cell < 100:
        current_cell = cells[id_current_cell]
        show_cell(current_cell)
        if (current_cell['cell_type'] == 'code') and (current_cell['source'] != ''):
            source_string = reduce(lambda a, b: a + b, current_cell['source'])
            input_ = raw_input('execute?[Y-es,s-kip,e-dit]')
            if input_ == '':
                print '===== Out      ====='
                try:
                    exec(source_string)
                    id_current_cell += 1
                except:
                    print 'exception'
                command_ = raw_input(':')
                try:
                    exec(command_)
                except:
                    pass
            if input_ == 'e':
                with open('tmp.py', 'w') as fw:
                    fw.write(source_string.encode('utf-8'))
                subprocess.check_call('vim ./tmp.py', shell=True)
                with open('tmp.py', 'r') as fr:
                    source_string = fr.read().decode('utf-8').rstrip('\n')
                    current_cell['source'] = [eachrow + '\n' for eachrow in source_string.split('\n')]
                    current_cell['source'][-1].rstrip('\n')
                    current_cell['source'][-1].rstrip('\n')
            if input_ == 's':
                id_current_cell += 1
        else:
            input_ = raw_input(':')
            if input_ == '':
                id_current_cell += 1
def exec_cell(cell):
    if cell['cell_type'] == 'code':
        source_string = reduce(lambda a, b: a + b, cell['source'])
        exec(source_string)
        #for line in cell['source']:
        #    exec(line)
    else:
        pass
        # show_cell(cell)


def exec_nb(js_ipynb):
    for cell in js_ipynb['cells']:
        exec_cell(cell)


def load_ipynb(filename):
    f = open(filename)
    js_ipynb = json.load(f)
    return js_ipynb['cells']

def main():
    if len(sys.argv) < 2:
        print 'usage: python ' + sys.argv[0] + ' [input filename(xxx.ipynb)]'
        quit()

    filename = str(sys.argv[1])
    f = open(filename)
    js_ipynb = json.load(f)

    #show_all(js_ipynb)
    cells = js_ipynb['cells']
    controller(cells)

if __name__ == '__main__':
    main()
