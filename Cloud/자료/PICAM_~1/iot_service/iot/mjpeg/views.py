# 처음 나오는 응답을 하는과정

from django.views.generic.base import TemplateView
from django.http import HttpResponse, StreamingHttpResponse
from mysite.usbcam import MJpegStreamCam
# from mysite.picam import MJpegStreamCam

mjpegstream = MJpegStreamCam()
class CamView(TemplateView):
    template_name = "cam.html"

    def get_context_data(self):
        context = super().get_context_data()
        context["mode"] = self.request.GET.get("mode","#")
        return context

def snapshot(request):
    image = mjpegstream.snapshot()
    return HttpResponse(image, content_type = "image/jpeg")

def mjpeg_stream(request):
    return StreamingHttpResponse(mjpegstream,
                content_type = 'multipart/x-mixed-replace;boundary=--myboundary')

# Create your views here.
