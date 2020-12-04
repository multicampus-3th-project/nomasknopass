from django.shortcuts import render
from django.views import View
from django.http import HttpResponse, JsonResponse


# class VideoView(View):
#     def get(self, request):
#         offset = int(request.GET.get('offset', 0))
#         limit = int(request.GET.get('limit', 12))
#         videos = Video.objects.select_related('category').order_by('id')[offset * limit: (offset + 1) * limit]
#         data = [{
#             'title': props.title,
#             'image_url': props.background_image,
#             'detail_id': props.id,
#         } for props in videos]
#         return JsonResponse(list(data), safe=False, status=200)

class IndexView(View):
    def get(self, request):
        dummy_data = {
            'name': '죠르디'
        }
        return JsonResponse(dummy_data)

    def post(self, request):
        return HttpResponse("POST 받았다")
