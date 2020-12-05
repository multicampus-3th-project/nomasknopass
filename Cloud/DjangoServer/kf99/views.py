from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view


@api_view(['GET', 'POST'])
def mask(request):
    if request.method == 'GET':
        return HttpResponse("GET 요청 응답")
    elif request.method == 'POST':
        # file = request.FILES['file']
        filename = str(request.FILES['file'])
        print(filename)
        handle_uploaded_file(request.FILES['file'], filename)
        return HttpResponse("파일 받기")


def handle_uploaded_file(f, filename):
    with open('/home/ubuntu/' + filename, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
