# -*- config: utf-8 -*-

class SingletonType(type):
    '''シングルトン　メタクラス'''
    _instance = None
    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(SingletonType, cls).__call__(*args, **kwargs)
         
        return cls._instance


class Singleton(object):
    '''シングルトン　メタクラス'''
    __metaclass__ = SingletonType