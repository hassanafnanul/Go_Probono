from django.http.response import JsonResponse
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Q

from API.Law.serializers import Law, LawSerializer
from API.KnowYourLaw.serializers import KnowYourLaw, KylSerializer
from API.Lawyer.serializers import Lawyer, LawyerSerializer
from API.Event.serializers import Event, EventSerializer
from API.TeamMember.serializers import TeamMember, TeamMemberSerializer




class GlobalSearch(APIView):
    def get(self, request, search):
        searchResult = {}

        # Law -----
        laws = Law.objects.filter(is_archived = False).filter(name__icontains = search).order_by("order")
        searchResult['laws'] = LawSerializer(laws, many=True).data

        # Law -----
        kyls = KnowYourLaw.objects.filter(is_archived = False).filter(Q(question__icontains = search) | Q(tags__icontains = search)).order_by("-created_at")
        searchResult['kyls'] = KylSerializer(kyls, many=True).data

        # Lawyers -----
        lawyers = Lawyer.objects.filter(is_archived = False).filter(name__icontains = search).order_by("-created_at")
        searchResult['lawyers'] = LawyerSerializer(lawyers, many=True).data

        # Events -----
        events = Event.objects.filter(is_archived = False).filter(name__icontains = search).order_by("order")
        searchResult['events'] = EventSerializer(events, many=True).data

        # Teams -----
        teams = TeamMember.objects.filter(is_archived = False).filter(name__icontains = search).order_by("order")
        searchResult['teams'] = TeamMemberSerializer(teams, many=True).data
        
        return Response(searchResult, status=status.HTTP_200_OK)
    




