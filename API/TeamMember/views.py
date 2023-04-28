from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import TeamMember, TeamMemberSerializer, TeamMemberDetailsSerializer
import json
from django.http import Http404, JsonResponse, HttpResponseForbidden
from rest_framework.decorators import api_view





class TeamMemberAPI(APIView):
    def get(self, request):
        teamMembers = TeamMember.objects.all().order_by("order").exclude(is_archived = True)
        serializer = TeamMemberSerializer(teamMembers, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)



class TeamMemberDetailsAPI(APIView):
    def get(self, request, slug):
        try: 
            teamMember = TeamMember.objects.get(slug = slug, is_archived = False)
            serializer = TeamMemberDetailsSerializer(teamMember)
        
            return Response(serializer.data, status=status.HTTP_200_OK)
        except:
            errorJson = {
                'success': False,
                'msg': 'Team Member not found'
            }
            return Response(errorJson, status=status.HTTP_404_NOT_FOUND)
        
        



