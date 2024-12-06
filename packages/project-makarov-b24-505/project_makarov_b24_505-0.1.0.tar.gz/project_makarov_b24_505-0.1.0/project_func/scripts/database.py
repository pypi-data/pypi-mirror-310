#!/usr/bin/env python3


def create(tables, table_name, col_names):
    tables[table_name] = col_names
    return 0


def check(tables, table_name):
    return (table_name in tables.keys())


def delete(tables, table_name):
    if (not (table_name in tables.keys())):
        return 1
    tables.pop(table_name)
    return 0


def help():
    print('Функции:')
    print('create table_name col_names - создать таблицу table_name  со следующими столбцами col_names')
    print('check table_name - проверить на наличие такой таблицы table')
    print('delete table_name - удалить таблицу table')
    print('exit - выход из программы')
    print('help - справочная информация')
