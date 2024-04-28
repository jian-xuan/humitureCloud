from django.shortcuts import render, redirect

from index import models
import os
from django.http import JsonResponse
from django.contrib import auth

from index.self import dev

# Create your views here.
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def index(request):
    return render(request,"index.html")


def logout(request):
    auth.logout(request)
    return redirect('/')


def page_not_found(request):
    return render(request, '404.html')


def page_error(request):
    return render(request, '500.html')


def getDevData(request):
    # 从数据库中获取最新的传感器数据
    latest_data = models.DevInfo.objects.latest('receive_time')
    # 封装 JSON 数据
    data = {
        'timestamp': str(latest_data.receive_time)[5:16],
        'temperature': latest_data.tem,
        'humidity': latest_data.hum,
        'hOpen': latest_data.hOpen,
        'tOpen':latest_data.tOpen,
    }

    # 返回 JSON 数据
    return JsonResponse(data)


def get_History(request):
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')
    # 查询时间范围内的温湿度数据
    data = models.DevInfo.objects.filter(
        receive_time__date__range=[start_date, end_date]
    ).all()
    result = []
    for item in data:
        temp = {}
        temp['receive_time'] = item.receive_time
        temp['tem'] = item.tem
        temp['hum'] = item.hum
        temp['tOpen'] = item.tOpen
        temp['hOpen'] = item.hOpen
        result.append(temp)
    return JsonResponse(result, safe=False)


def tAuto(request):
    tg = request.GET.get('tg')
    dev.auto = True if tg >0 else False
    return JsonResponse("更改开关状态成功",safe=False)

def tOpen(request):
    tg = request.GET.get('tg')
    tg = str(tg)
    print("收到信息  tg="+tg)
    try:
        dev.conn.send(tg.encode())
        return JsonResponse("发送成功", safe=False)
    except Exception :
        return JsonResponse("发送失败", status=500,safe=False)

