from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse
from . import models
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


class UploadImage(View):
    def post(self, request):
        pass



def getimage(request):
    try:
        page = int(request.GET.get('page', 1))
    except:
        print('页码错误')
        page = 1

    img_url = models.Image.objects.values('url').order_by('id')

    pagent = Paginator(img_url, 5, orphans=4)

    try:
        info = pagent.page(page)
    except Exception as e:
        print(e)
        info = pagent.page(pagent.num_pages)

    # print(info)

    url_list = list(info)
    print(url_list)
    final_url = []
    for i in url_list:
        final_url.append('http://127.0.0.1:8000/media/image/1/'+ i['url'] +'/')

    print(final_url)

    return JsonResponse(data=final_url, safe=False)
