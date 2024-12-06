#!/usr/bin/env python3


import sys


sys.path.insert(1, '/home/user/python_lab_4/project_makarov_b24-505/project_func')


from cli import welcome


def main():
    print('Первая попытка запустить проект!')
    print('***')
    welcome()


if __name__ == '__main__':
    main()
