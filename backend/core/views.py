# from django.shortcuts import render
from json import JSONDecodeError
from django.http import JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import views, status
from rest_framework.response import Response

# user module with user class
from .serializers import ContactSerializer
# Create your views here.

# but how does it know to invoke post method here? are we overriding a post method here?
class ContactAPIView(views.APIView):
    """
    A simple APIView for creating contact entries
    """
    serializer_class = ContactSerializer

    def get_serializer_context(self):
        return {
            'request':self.request,
            'format': self.format_kwarg,
            'view': self
        }
    
    def get_serializer(self, *args, **kwargs):
        kwargs['context'] = self.get_serializer_context()
        return self.serializer_class(*args, **kwargs)

    def post(self, request):
        try:
            data = JSONParser().parse(request)
            serializer = ContactSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                serializer.save() # what does this do?
                return Response(serializer.data)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except JSONDecodeError:
            return JsonResponse({"result": "error",
            "message": "Json decoding error"}, status= 400)