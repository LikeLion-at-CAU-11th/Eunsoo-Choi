from django.shortcuts import render
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
# Create your views here.

def introduction(request):
    if request.method=='GET':
        return JsonResponse({
            'status':200,
            'succes':True,
            'message':'메세지 전달 성공!',
            'data':[
                {
                    "name":"최은수",
                    "id":20211833,
                    "major":"sociology"
                },
                {
                    "name":"나상현",
                    "id":20201876,
                    "major":"Computer Science and Engineering",
                }
                    ]
        })