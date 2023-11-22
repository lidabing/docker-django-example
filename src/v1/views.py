import json
from django.shortcuts import render
import redis
from django.http import JsonResponse
from django.http import HttpResponse
from v1.redis_manager import redis_manager

# Create your views here.
def hello(request):
    r = redis.Redis(host='convertible_bond-redis-1', port=6379, db=0)
     # 读取一个键的值
    value = r.get('downloaded_data')
    if value:
        value = json.loads(value)  # Convert the string back to a dict
    #value = 'hello world'
    return JsonResponse(value)

def realtime_bond_market(request):
    # 实现实时债券市场逻辑
    return JsonResponse({'message': 'Realtime bond market data'})

def basic_bonds(request):
    # 实现转债的基础信息逻辑
    data = redis_manager.get_data('basic_bonds')
    response_data = {
        "code": 200,  # 你的状态码
        "msg": "Success",  # 你的消息
        "data": data
    }
    response_data = json.dumps(response_data, ensure_ascii=False)
    response = HttpResponse(response_data, content_type='text/plain; charset=utf-8')
    return response

def upcoming_bonds(request):
    # 实现即将发行的转债逻辑
    data = redis_manager.get_data('upcoming_bonds')
    response_data = {
        "code": 200,  # 你的状态码
        "msg": "Success",  # 你的消息
        "data": data
    }
    response_data = json.dumps(response_data, ensure_ascii=False)
    response = HttpResponse(response_data, content_type='text/plain; charset=utf-8')
    return response


def upcoming_adjust_bonds(request):
    # upcoming_adjust_bonds
    data = redis_manager.get_data('upcoming_adjust_bonds')
    response_data = {
        "code": 200,  # 你的状态码
        "msg": "Success",  # 你的消息
        "data": data
    }
    response_data = json.dumps(response_data, ensure_ascii=False)
    response = HttpResponse(response_data, content_type='text/plain; charset=utf-8')
    return response

def proposed_adjust_bonds(request):
    # 实现已经提议下修但还未完成下修过程的转债逻辑
    # upcoming_adjust_bonds
    data = redis_manager.get_data('proposed_adjust_bonds')
    response_data = {
        "code": 200,  # 你的状态码
        "msg": "Success",  # 你的消息
        "data": data
    }
    response_data = json.dumps(response_data, ensure_ascii=False)
    response = HttpResponse(response_data, content_type='text/plain; charset=utf-8')
    return response
def upcoming_adjust_condition_bonds(request):
    # 实现获取即将符合下修条件的转债列表逻辑
    # key = 'upcoming_adjust_condition_bonds'
    data = redis_manager.get_data('upcoming_adjust_condition_bonds')
    response_data = {
        "code": 200,  # 你的状态码
        "msg": "Success",  # 你的消息
        "data": data
    }
    response_data = json.dumps(response_data, ensure_ascii=False)
    response = HttpResponse(response_data, content_type='text/plain; charset=utf-8')
    return response

def upcoming_mandatory_redeem_bonds(request):
    # 实现即将达到强制赎回条件的转债逻辑
    return JsonResponse({'message': 'Upcoming mandatory redeem bonds data'})

def mandatory_redeem_condition_bonds(request):
    # 实现已经满足强赎回条件的转债列表逻辑
    return JsonResponse({'message': 'Mandatory redeem condition bonds data'})

def redeem_announced_bonds(request):
    # 实现已经发出强赎公告的转债列表逻辑
    return JsonResponse({'message': 'Redeem announced bonds data'})

def upcoming_natural_expire_bonds(request):
    # 实现转债即将自然到期，不是强赎的转债列表逻辑
    return JsonResponse({'message': 'Upcoming natural expire bonds data'})
