from django.http import JsonResponse
import json
from Bot import ChatBot as bot
from time import gmtime, strftime
from app.models import Product,ChatDetals

def index(request):
    if request.method == 'POST':
        Product.objects.all()
        ChatDetals.objects.all()
        jsonData = json.loads(request.body.decode('utf-8'))
        msg = jsonData["msg"]
        res = bot.ChatBot.getBot().response(msg)
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        catagory = ChatDetals(User=msg,Bot=res,Chat_Time=time)
        catagory.save()
        return JsonResponse({
            "desc": "Success",
            "ques": msg,
            "res": res,
            "time": time
        })
    else:
        return JsonResponse({"desc": "Bad request"}, status=400)



