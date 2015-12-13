#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import json
import subprocess
import itertools


LENGTH_BARS = 50
HEAD_CODE = '===============' + LENGTH_BARS * '='
TAIL_CODE = '---------------' + LENGTH_BARS * '-'
HEAD_MD = '=====Markdown==' + LENGTH_BARS * '='
TAIL_MD = '-----Markdown--' + LENGTH_BARS * '-'
HEAD_EXEC = '=====Out=======' + LENGTH_BARS * '='
TAIL_EXEC = '---------------' + LENGTH_BARS * '-'
HEAD_EXCEPTION = '=====Exception=' + LENGTH_BARS * '='
TAIL_EXCEPTION = '-----Exception-' + LENGTH_BARS * '-'
EDITOR = 'pyvim'
FILETMP = '__tmp.py'


count_ = itertools.count()
MODE_SHOWCELL = count_.next()
MODE_INPUT0 = count_.next()
MODE_INPUT1 = count_.next()
MODE_INPUT2 = count_.next()
MODE_EXECCELL = count_.next()
MODE_EDIT = count_.next()
MODE_COMMANDPROMPT = count_.next()
MODE_INSERT = count_.next()
MODE_DELETE = count_.next()
MODE_LIST = count_.next()
MODE_EXIT = count_.next()


def get_sourcestring(cell):
    if cell['source'] == []:
        return ''
    elif len(cell['source']) == 1:
        return cell['source'][0]
    else:
        return reduce(lambda a, b: a + b, cell['source'])


def string_to_cell(source_string):
    cell_source = [eachrow + '\n' for eachrow in source_string.split('\n')]
    cell_source[-1].rstrip('\n')
    cell_source[-1].rstrip('\n')
    return cell_source


def show_cell(cell, id_current_cell):
    tag_id = ': ' + str(id_current_cell)
    source_string = get_sourcestring(cell)
    if cell['cell_type'] == 'code':
        print HEAD_CODE + tag_id
        print source_string.rstrip('\n')
        print TAIL_CODE + tag_id
    else:
        print HEAD_MD + tag_id
        print source_string.rstrip('\n')
        print TAIL_MD + tag_id


def print_exception(info):
    print HEAD_EXCEPTION
    print info[0]
    print info[1]
    print info[2]
    print TAIL_EXCEPTION


def parse_cells(cells):
    id_current_cell = 0
    mode = MODE_SHOWCELL
    while (id_current_cell < len(cells)) and (-1 < id_current_cell) and (mode != MODE_EXIT):
        current_cell = cells[id_current_cell]
        if mode == MODE_SHOWCELL:
            show_cell(current_cell, id_current_cell)
            if (current_cell['cell_type'] == 'code') and (current_cell['source'] != ''):
                mode = MODE_INPUT0
            else:
                mode = MODE_INPUT1

        elif mode == MODE_INPUT0:
            input_ = raw_input('execute?[Y-es,n-ext,b-ack,e-dit,c-ommand,i-nsert,d-elete,l-ist,eXit]')
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
            elif input_ in ['i']:
                mode = MODE_INSERT
            elif input_ in ['d']:
                mode = MODE_DELETE
            elif input_ in ['l']:
                mode = MODE_LIST
            elif input_ in ['x','X','exit']:
                mode = MODE_EXIT

        elif mode == MODE_INPUT1:
            input_ = raw_input('[N-ext,b-ack,e-dit,c-ommand,i-nsert,d-elete,l-ist,eXit]')
            if input_ in ['', 'n','N']:
                id_current_cell += 1
                mode = MODE_SHOWCELL
            elif input_ in ['b','back']:
                id_current_cell -= 1
                mode = MODE_SHOWCELL
            elif input_ in ['e','edit']:
                mode = MODE_EDIT
            elif input_ in ['c','command']:
                mode = MODE_COMMANDPROMPT
            elif input_ in ['i','insert']:
                mode = MODE_INSERT
            elif input_ in ['d','delte']:
                mode = MODE_DELETE
            elif input_ in ['l','list']:
                mode = MODE_LIST
            elif input_ in ['x','X','exit']:
                mode = MODE_EXIT

        elif mode == MODE_INPUT2:
            input_ = raw_input('[N-ext,b-ack,e-dit,c-ommand,p-rint]')
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
            elif input_ in ['p']:
                exec('print ' + current_cell['source'][-1])

        elif mode == MODE_EXECCELL:
            source_string = get_sourcestring(current_cell)
            try:
                success_command = False
                print HEAD_EXEC
                exec(source_string)
                print TAIL_EXEC
                success_command = True
            except:
                print_exception(sys.exc_info())
                mode = MODE_SHOWCELL
            if success_command:
                mode = MODE_INPUT2

        elif mode == MODE_COMMANDPROMPT:
            command_ = raw_input(':')
            while command_ != '':
                try:
                    success_command = False
                    exec(command_)
                    success_command = True
                except:
                    print_exception(sys.exc_info())
                if success_command:
                    try:
                        exec('print ' + command_)
                    except:
                        pass
                command_ = raw_input(':')
            mode = MODE_SHOWCELL

        elif mode == MODE_EDIT:
            source_string = get_sourcestring(current_cell)
            with open(FILETMP, 'w') as fw:
                fw.write(source_string.encode('utf-8'))
            subprocess.check_call(EDITOR + ' ' + FILETMP, shell=True)
            with open(FILETMP, 'r') as fr:
                source_string = fr.read().decode('utf-8').rstrip('\n')
                current_cell['source'] = string_to_cell(source_string)
            mode = MODE_SHOWCELL

        elif mode == MODE_INSERT:
            cells_new0 = cells[:id_current_cell]
            cell_insert = {'cell_type': 'code', 'execution_count': None, 'metadata': {'collapsed': False}, 'outputs': [], 'source': []}
            cells_new1 = cells[id_current_cell:]
            cells = cells_new0 + [cell_insert] + cells_new1
            id_current_cell += 1
            mode = MODE_EDIT

        elif mode == MODE_DELETE:
            input_ = raw_input('Do you reall want to delete this cell?[N-o,yes]')
            if input_ == 'yes':
                cells_new0 = cells[:id_current_cell]
                cells_new1 = cells[id_current_cell+1:]
                cells = cells_new0 + cells_new1
            else:
                pass
            mode = MODE_SHOWCELL

        elif mode == MODE_LIST:
            for i, cell in enumerate(cells):
                show_cell(cell, i)
            mode = MODE_SHOWCELL

    return cells


def load_ipynb(filename):
    with open(filename) as f:
        js_ipynb = json.load(f)
        return js_ipynb


def main():
    if len(sys.argv) < 2:
        print 'usage: python ' + sys.argv[0] + ' [input filename(xxx.ipynb)]'
        quit()

    filename = str(sys.argv[1])
    ipynb = load_ipynb(filename)
    cells = ipynb['cells']

    ipynb['cells'] = parse_cells(cells)

    with open(filename, 'w') as fw:
        json.dump(ipynb, fw)

if __name__ == '__main__':
    main()
