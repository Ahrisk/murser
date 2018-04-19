# -*- coding: utf-8 -*-
# ----------------------------
# Database.py
# provide the interface to SQL. Only mySQL is supported now.
# ----------------------------
import threading


class _Engine(object):
    def __init__(self, connect):
        self.__connect = connect

    @property
    def connect(self):
        return self.__connect

engine = None


class _DbCtx(threading.local):
    def __init__(self):
        self.connection = None
        self.transactions = 0

    def is_init(self):
        return not self.connection is None

    def init(self):
        self.connection = _LasyConnection()
        self.transactions = 0

    def cleanup(self):
        self.connection.cleanup()
        self.connection = None

    def cursor(self):
        return self.connection.cursor()

_db_ctx = _DbCtx()


class _ConnectionCtx(object):
    def __enter__(self):
        global _db_ctx
        self.should_cleanup = False
        if not _db_ctx.is_init():
            _db_ctx.init()
            self.should_cleanup = True
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        global  _db_ctx
        if self.should_cleanup:
            _db_ctx.cleanup()


def connection():
    return _ConnectionCtx()


def with_connection(func):
    def wrapper(*args, **kw):
        with connection():
            return func(*args, **kw)
    return wrapper


@with_connection
def select(sql, *args):
    pass


@with_connection
def update(sql, *args):
    pass


@with_connection
def delete(sql, *args):
    pass


@with_connection
def insert(sql, *args):
    pass
