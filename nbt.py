#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import subprocess
import itertools


LENGTH = 50
HEAD_EXCEPTION = '=====Exception=' + LENGTH * '='
TAIL_EXCEPTION = '-----Exception-' + LENGTH * '-'
HEAD_CODE = '===============' + LENGTH * '='
TAIL_CODE = '---------------' + LENGTH * '-'
HEAD_MD = '=====Markdown==' + LENGTH * '='
TAIL_MD = '-----Markdown--' + LENGTH * '-'
HEAD_EXEC = '=====Out=======' + LENGTH * '='
TAIL_EXEC = '---------------' + LENGTH * '-'


count_ = itertools.count()
MODE_SHOWCELL = count_.next()
MODE0 = count_.next()
MODE1 = count_.next()
MODE_EXECCELL = count_.next()
MODE_EDIT = count_.next()
MODE_COMMANDPROMPT = count_.next()


def get_user_input():
    uinput = raw_input('termnb>>')
    return uinput


def show_cell(cell, id_current_cell):
    tag_id = ': ' + str(id_current_cell)
    if cell['source'] != []:
        source_string = reduce(lambda a, b: a + b, cell['source'])
        if cell['cell_type'] == 'code':
            print HEAD_CODE + tag_id
            print source_string.rstrip('\n')
            print TAIL_CODE + tag_id
        else:
            print HEAD_MD + tag_id
            print source_string.rstrip('\n')
            print TAIL_MD + tag_id


def show_all(js_ipynb):
    for cell in js_ipynb['cells']:
        show_cell(cell)


def get_sourcestring(cell):
    return reduce(lambda a, b: a + b, cell['source'])


def controller(cells):
    id_current_cell = 0
    mode = MODE_SHOWCELL
    while id_current_cell < len(cells):
        current_cell = cells[id_current_cell]
        if mode == MODE_SHOWCELL:
            show_cell(current_cell, id_current_cell)
            if (current_cell['cell_type'] == 'code') and (current_cell['source'] != ''):
                mode = MODE0
            else:
                mode = MODE1
        elif mode == MODE0:
            input_ = raw_input('execute?[Y-es,n-ext,b-ack,e-dit,c-ommand]')
            if input_ in ['', 'y', 'Y']:
                mode = MODE_EXECCELL
            elif input_ in ['n']:
                id_current_cell += 1
                mode = MODE_SHOWCELL
            elif input_ in ['b']:
                id_current_cell -= 1
                mode = MODE_SHOWCELL
            elif input_ in ['e']:
                mode = MODE_EDIT
            elif input_ in ['c']:
                mode = MODE_COMMANDPROMPT

        elif mode == MODE1:
            input_ = raw_input('[N-ext,b-ack,e-dit,c-ommand]')
            if input_ in ['', 'n']:
                id_current_cell += 1
                mode = MODE_SHOWCELL
            elif input_ in ['b']:
                id_current_cell -= 1
                mode = MODE_SHOWCELL
            elif input_ in ['e']:
                mode = MODE_EDIT
            elif input_ in ['c']:
                mode = MODE_COMMANDPROMPT

        elif mode == MODE_EXECCELL:
            source_string = get_sourcestring(current_cell)
            try:
                print HEAD_EXEC
                success_command = False
                exec(source_string)
                success_command = True
                print TAIL_EXEC
            except:
                print HEAD_EXCEPTION
                print sys.exc_info()[0]
                print sys.exc_info()[1]
                print sys.exc_info()[2]
                print TAIL_EXCEPTION
                mode = MODE1
            if success_command:
                id_current_cell += 1
                mode = MODE_SHOWCELL

        elif mode == MODE_COMMANDPROMPT:
            command_ = raw_input(':')
            while command_ != '':
                try:
                    success_command = False
                    exec(command_)
                    success_command = True
                except:
                    print HEAD_EXCEPTION
                    print sys.exc_info()[0]
                    print sys.exc_info()[1]
                    print sys.exc_info()[2]
                    print TAIL_EXCEPTION
                if success_command:
                    try:
                        exec('print ' + command_)
                    except:
                        pass
            mode = MODE_SHOWCELL
        elif mode == MODE_EDIT:
            source_string = get_sourcestring(current_cell)
            with open('tmp.py', 'w') as fw:
                fw.write(source_string.encode('utf-8'))
            subprocess.check_call('vim ./tmp.py', shell=True)
            with open('tmp.py', 'r') as fr:
                source_string = fr.read().decode('utf-8').rstrip('\n')
                current_cell['source'] = [eachrow + '\n' for eachrow in source_string.split('\n')]
                current_cell['source'][-1].rstrip('\n')
                current_cell['source'][-1].rstrip('\n')
            mode = MODE_SHOWCELL


def exec_cell(cell):
    if cell['cell_type'] == 'code':
        source_string = reduce(lambda a, b: a + b, cell['source'])
        exec(source_string)
        # for line in cell['source']:
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
