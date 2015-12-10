#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import subprocess


BAR = '=========================='
OUT = '======= OUT =============='
LINE = '--------------------------'

HEAD_CODE = '=================================='
TAIL_CODE = '----------------------------------'
HEAD_MD = '======Markdown===================='
TAIL_MD = '------Markdown--------------------'


def get_user_input():
    uinput = raw_input('termnb>>')
    return uinput


def show_cell(cell, id_current_cell):
    tag_id = ': ' + str(id_current_cell)
    if cell['source'] != []:
        source_string = reduce(lambda a, b: a + b, cell['source'])
        if cell['cell_type'] == 'code':
            print HEAD_CODE + HEAD_CODE[-1]*30 + tag_id
            print source_string.rstrip('\n')
            print TAIL_CODE + TAIL_CODE[-1]*30 + tag_id
        else:
            print HEAD_MD + HEAD_MD[-1]*30 + tag_id
            print source_string.rstrip('\n')
            print TAIL_MD + TAIL_MD[-1]*30 + tag_id


def show_all(js_ipynb):
    for cell in js_ipynb['cells']:
        show_cell(cell)
import sys

def controller(cells):
    id_current_cell = 0

    while id_current_cell < len(cells):
        current_cell = cells[id_current_cell]
        show_cell(current_cell, id_current_cell)
        if (current_cell['cell_type'] == 'code') and (current_cell['source'] != ''):
            source_string = reduce(lambda a, b: a + b, current_cell['source'])
            input_ = raw_input('execute?[Y-es,n-ext,e-dit,b-ack,c-ommand]')
            if input_ in ['', 'y', 'Y']:
                try:
                    print '===== Out ==========='
                    success_command = False
                    exec(source_string)
                    success_command = True
                except:
                    print '===== Exception ====='
                    print sys.exc_info()[0]
                    print sys.exc_info()[1]
                    print sys.exc_info()[2]
                    print '---------------------'
                if success_command:
                    id_current_cell += 1
                    try:
                        exec('print ' + current_cell['source'][-1])
                    except:
                        pass
                    command_ = raw_input(':')
                    while command_ != '':
                        try:
                            exec('print ' + command_)
                        except:
                            try:
                                exec(command_)
                            except:
                                print sys.exc_info()[0]
                                print sys.exc_info()[1]
                                print sys.exc_info()[2]
                        command_ = raw_input(':')
                else:
                    input_ = raw_input('[N-ext,e-dit,b-ack,c-ommand]')
                    if input_ in ['', 'n']:
                        id_current_cell += 1
                    elif input_ == 'e':
                        source_string = reduce(lambda a, b: a + b, current_cell['source'])
                        with open('tmp.py', 'w') as fw:
                            fw.write(source_string.encode('utf-8'))
                        subprocess.check_call('vim ./tmp.py', shell=True)
                        with open('tmp.py', 'r') as fr:
                            source_string = fr.read().decode('utf-8').rstrip('\n')
                            current_cell['source'] = [eachrow + '\n' for eachrow in source_string.split('\n')]
                            current_cell['source'][-1].rstrip('\n')
                            current_cell['source'][-1].rstrip('\n')
                    elif input_ == 's':
                        id_current_cell += 1
                    elif input_ in ['b', 'back']:
                        id_current_cell -= 1
                    elif input_ == 'c':
                        command_ = raw_input(':')
                        while command_ != '':
                            try:
                                exec('print ' + command_)
                            except:
                                try:
                                    exec(command_)
                                except:
                                    print sys.exc_info()[0]
                                    print sys.exc_info()[1]
                                    print sys.exc_info()[2]
                            command_ = raw_input(':')
            elif input_ == 'c':
                command_ = raw_input(':')
                while command_ != '':
                    try:
                        exec('print ' + command_)
                    except:
                        try:
                            exec(command_)
                        except:
                            print sys.exc_info()[0]
                            print sys.exc_info()[1]
                            print sys.exc_info()[2]
                    command_ = raw_input(':')
            elif input_ == 'e':
                with open('tmp.py', 'w') as fw:
                    fw.write(source_string.encode('utf-8'))
                subprocess.check_call('vim ./tmp.py', shell=True)
                with open('tmp.py', 'r') as fr:
                    source_string = fr.read().decode('utf-8').rstrip('\n')
                    current_cell['source'] = [eachrow + '\n' for eachrow in source_string.split('\n')]
                    current_cell['source'][-1].rstrip('\n')
                    current_cell['source'][-1].rstrip('\n')
            elif input_ in ['n']:
                id_current_cell += 1
            elif input_ in ['b', 'back']:
                id_current_cell -= 1
        else:
            input_ = raw_input('[N-ext,e-dit,b-ack,c-ommand]')
            if input_ in ['', 'n']:
                id_current_cell += 1
            elif input_ == 'e':
                source_string = reduce(lambda a, b: a + b, current_cell['source'])
                with open('tmp.py', 'w') as fw:
                    fw.write(source_string.encode('utf-8'))
                subprocess.check_call('vim ./tmp.py', shell=True)
                with open('tmp.py', 'r') as fr:
                    source_string = fr.read().decode('utf-8').rstrip('\n')
                    current_cell['source'] = [eachrow + '\n' for eachrow in source_string.split('\n')]
                    current_cell['source'][-1].rstrip('\n')
                    current_cell['source'][-1].rstrip('\n')
            elif input_ == 's':
                id_current_cell += 1
            elif input_ in ['b', 'back']:
                id_current_cell -= 1
            elif input_ == 'c':
                command_ = raw_input(':')
                while command_ != '':
                    try:
                        exec('print ' + command_)
                    except:
                        try:
                            exec(command_)
                        except:
                            print sys.exc_info()[0]
                            print sys.exc_info()[1]
                            print sys.exc_info()[2]
                    command_ = raw_input(':')


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
