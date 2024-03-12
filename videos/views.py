from django.shortcuts import render
from django.http import HttpResponseRedirect
from .serializers import ResumeSerializer
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response

class ResumeView(APIView):
    @swagger_auto_schema(request_body=ResumeSerializer)
    def post(self, request):
        serializer = ResumeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return HttpResponseRedirect("/")
        return Response(serializer.errors, status=400)
