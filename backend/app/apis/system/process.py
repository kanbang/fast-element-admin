'''
Descripttion: 
version: 0.x
Author: zhai
Date: 2023-05-31 09:38:40
LastEditors: zhai
LastEditTime: 2023-05-31 17:24:58
'''
import os
import signal
import subprocess
from fastapi import APIRouter

from app.corelibs.http_response import partner_success

router = APIRouter()


# 全局变量用于存储进程对象
process_dict = dict()

# 启动进程的函数
def start_process(params):
    # 获取当前进程的路径
    file = params.lower()
    current_dir = os.getcwd()
    fullpath = current_dir+'/process/{}.py'.format(file)

    if not os.path.isfile(fullpath):
        return None

    # 启动进程，执行另一个Python脚本
    if file in process_dict:
        process = process_dict[file]
        if process:
            process.terminate()

    process = subprocess.Popen(['python', fullpath], shell=False, cwd=current_dir+'/process')
    process_dict[file] = process
    return process


@router.post('/startup', description="启动进程")
async def process_startup(params: str):
    if start_process(params):
        return partner_success({
            'name': params,
            'result': 'ok',
        })
    else:
        return partner_success({
            'name': params,
            'result': 'error',
        })


@router.post('/shutdown', description="停止进程")
async def process_shutdown(params: str):
    # global process
    file = params.lower()
    if file in process_dict:
        process = process_dict[file]

        process.terminate()
        del process_dict[file]

        return partner_success({
            'name': params,
            'result': 'ok',
        })
    return partner_success(-{
        'name': params,
        'result': 'error',
    })


@router.post('/status', description="进程状态")
async def process_status(params: str):
    # global process
    file = params.lower()
    if file in process_dict:
        process = process_dict[file]
        if process and process.poll() is None:
            return partner_success({
                'name': params,
                'result': 'ok',
            })

    return partner_success({
        'name': params,
        'result': 'error',
    })
