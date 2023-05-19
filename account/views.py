from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse, HttpResponseNotFound,HttpResponseRedirect
from django.core import serializers
from rest_framework.decorators import api_view
from account.models import account
import json,datetime

# Create your views here.
@api_view(["POST"])
def createUser(request):
    try:
        # if request.method == 'POST':
        res = json.loads(request.body)

        username=res["username"]
        if len(username)<3:
            return JsonResponse({'success':False,"reason":"Username is too short"},status=400)
        elif len(username)>32:
            return JsonResponse({'success':False,"reason":"Username is too long"},status=400)

        password=res["password"]
        if len(password)<8:
            return JsonResponse({'success':False,"reason":"password is too short"},status=400)
        elif len(password)>32:
            return JsonResponse({'success':False,"reason":"password is too long"},status=400)

        uppercase=0
        lowercase=0
        num=0
        for i in password:
            if i.isupper():
                uppercase+=1
            if i.islower():
                lowercase+=1
            if i.isdigit():
                num+=1

        if uppercase<1:
            return JsonResponse({'success':False,"reason":"password must have at least 1 uppercase letter"},status=400)

        if lowercase<1:
            return JsonResponse({'success':False,"reason":"password must have at least 1 lowercase letter"},status=400)

        if num<1:
            return JsonResponse({'success':False,"reason":"password must have at least 1 number"},status=400)

        account_list=account.objects.all()
        account_list=serializers.serialize("json", account_list)
        account_list = json.loads(account_list)
        for usr in account_list:
            if username==usr["fields"]["username"]:
                return JsonResponse({'success':False,"reason":"Username already exists"},status=400)

        account.objects.create(username=username,password=password)

        return JsonResponse({'success':True,"reason":"Account create success"},status=201)

    except Exception as e:
        return HttpResponseBadRequest(str(e))

@api_view(["POST"])
def verifyUser(request):
    try:
        # if request.method == 'POST':
        now=datetime.datetime.now()
        res = json.loads(request.body)

        username=res["username"]
        password=res["password"]
        # print(username,password)

        usr=account.objects.filter(username=username).first()
        if usr is None:
            return JsonResponse({'success':False,"reason":"You may have entered the wrong username or password"},status=401)

        if usr.lock:
            total_seconds = (now-usr.unlock_time).total_seconds()
            if total_seconds<60:
                return JsonResponse({'success':False,"reason":"This account has been locked, Please try again after one minute"},status=423)
            else:
                usr.lock=False
                usr.pass_fail_num=0
                usr.unlock_time=None
                usr.save()

        # a=account.objects.all()
        # a=serializers.serialize("json", a)
        # a=json.loads(a)
        # for i in a:
        #     print(i)

        # usr=account.objects.filter(username=username,password=password).first()
        if usr.password==password:
            usr.pass_fail_num=0
            usr.save()
            return JsonResponse({'success':True,"reason":"Account verify success"},status=200)
        else:
            usr.pass_fail_num+=1
            if usr.pass_fail_num>=5:
                usr.lock=True
                usr.unlock_time=now
            usr.save()
            # temp=account.objects.filter(username=username).first()
            # if temp is not None:
            #     temp.pass_fail_num+=1
            #     if temp.pass_fail_num>=5:
            #         temp.lock=True
            #         temp.unlock_time=now
            #     temp.save()

            return JsonResponse({'success':False,"reason":"You may have entered the wrong username or password"},status=401)

    except Exception as e:
        return HttpResponseBadRequest(str(e))