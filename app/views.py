from django.shortcuts import render
from django.http import JsonResponse
from django.views import View

from .models import ProcessedImage
from modules import eye_fundus, melanoma

# Create your views here.
class HomeView(View):
    def __init__(self):
        self.eyeFundus = eye_fundus.EyeFundus()
        self.melanoma = melanoma.Melanoma()

    def get(self, request, *args, **kwargs):
        return render(request,'index.html')

    def post(self, request, *args, **kwargs):
        processType = request.POST.get('process-type', None)
        image = request.FILES.get('source-image', None)

        # return JsonResponse({'process-type':processType, 'image':image})
        context = {}

        if processType and image:
            if processType == 'eye-fundus':
                upload = ProcessedImage.objects.create(
                    input = image
                )

                inputPath = upload.input.path
                output = self.eyeFundus.process(inputPath)

                upload.output = output
                upload.save()
                
                context.update({'input':upload.input.url,'output':upload.output.url,"success":True})

            elif processType == 'melanoma':
                upload = ProcessedImage.objects.create(
                    input = image
                )

                inputPath = upload.input.path
                output = self.melanoma.process(inputPath)

                upload.output = output
                upload.save()
                
                context.update({'input':upload.input.url,'output':upload.output.url,"success":True})
               
            else:
                context['success'] = False
                context['error'] = "Unknown image processing type"
        else:
            context['success'] = False
            context['error'] = "Missing required parameters"

        return JsonResponse(context)
