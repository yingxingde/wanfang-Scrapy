#coding: utf8

#切到 begin_main 所在目录下,运行
import os
import time

def main():
    os.system('python thread_proxy.py && scrapy crawl wanfang')

if __name__ == '__main__':
    main()