#!/usr/bin/env python3


import sys


sys.path.insert(1, '/home/user/python_lab_4/project_makarov_b24-505/project_func/scripts')


from database import *


def database_main():
    help()
    while True:
	command = input('Введите команду: ').split()
        match command[0]:
	    case 'create':
                status = create(command[1], command[2:])
                print(f'Таблица {command[1]} успешно создана' if status == 0 else \
                    f'Не удалось создать таблицу {command[1]}')
	    case 'check':
                status = check(command[1])
                print(f'Таблица с названием {command[1]} существует' if status == 0 else \
                    f'Таблица с названием {command[1]} НЕ существует')
	    case 'delete':
                status = delete(command[1])
                print(f'Таблица {command[1]} успешно удалена' if status == 0 else \
                    f'Таблица с названием {command[1]} НЕ существует')
	    case 'exit':
                break
	    case 'help':
                help()
	    case _:
	        print(f'Функции {command[0]} нет. Попробуйте снова')


if __name__ == '__main__':
    main()
