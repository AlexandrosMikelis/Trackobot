from django.http import JsonResponse
import json
from products.models import Product

def api_home(request, *args, **kwargs):
    model_data = Product.objects.all().order_by("?").first()
    data={}
    if model_data:
        data['ID'] = model_data.id
        data['title'] = model_data.title
        data['content'] = model_data.content
        data['price'] = model_data.price
    # body = request.body
    # data ={}
    # try:
    #     data = json.loads(body)
    # except:
    #     pass
    # print(data)
    # data['params'] = dict(request.GET)
    # data['headers'] = dict(request.headers)
    # data['content'] = request.content_type
    return JsonResponse(data)
