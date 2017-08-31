# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from home.serializers import UserSerializer, GroupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from home.serializers import UserSerializer
from .models import TimeoutOption
from rest_framework.parsers import FormParser
from rest_framework.authtoken.models import Token

import pymongo
from pymongo import MongoClient

mongoserver_uri = "mongodb://Readuser:jbh4S3pCpTGCdIGGVOU6@10.8.0.2:27017/admin"
connection = MongoClient(host=mongoserver_uri)
db = connection['cc_accounts']
collection = db['LANDON_coinigy_account']
# values = collection.find_one()
cursor = collection.find({})
for document in cursor:
    print(document.keys())



class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows groups to be viewed or edited.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class TimeoutOptionView(APIView):
    parser_classes = (FormParser,)

    def post(self, request, format=None):
        token = Token.objects.get(key=request.auth)
        curr_user_id = token.user_id
        curr_timeout = request.data['timeout']
        if TimeoutOption.objects.all():
            if TimeoutOption.objects.get(user_id=token.user_id):
                timeout = TimeoutOption.objects.get(user_id=token.user_id)
                timeout.timeout = curr_timeout
            else:
                timeout = TimeoutOption(user_id=curr_user_id, timeout=curr_timeout)
        else:
            timeout = TimeoutOption(user_id=curr_user_id, timeout=curr_timeout)

        timeout.save()
        return Response('success', status=status.HTTP_200_OK)


# class RetrieveDataView(APIView):
#
#     def getdata(self, request, format=None):
#
#         mongoserver_uri = "mongodb://Readuser:jbh4S3pCpTGCdIGGVOU6@10.8.0.2:27017/admin"
#         connection = MongoClient(host=mongoserver_uri)
#         db = connection['cc_accounts']
#         # collection_names = db.collection_names()
#         # # collection_numbers = len(collection_names)
#         # for collection_name in collection_names:
#         #     collection = db[collection_name]
#         #     values = collection.find_one()
#         #     return values
#
#         collection = db['LANDON_coinigy_account']
#         values = collection.find_one()
#         return values















