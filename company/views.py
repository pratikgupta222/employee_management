from django.shortcuts import render

import json
import logging
import datetime

from django import db
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from company.models import Company
from company.serializers import CompanySerializer
from company.constants import UPDATION_KEY_NAMES


# Create your views here.


class CompanyList(views.APIView):
    """
        List all the filtered driver records or create a new record
    """
    permission_classes = (AllowAny, )

    def get(self, request):
        """
            For fetching all the drivers for the given city
        """
        data = {}

        company_queryset = Company.objects.all()

        if company_queryset:
            company_list = CompanySerializer(company_queryset, many=True)
            data["result"] = company_list.data
            return Response(status=status.HTTP_200_OK,
                            data=data)

        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data='No Company found')

    def post(self, request):
        """
            For creating a new driver
        """

        try:
            data = json.loads(request.body)
            logging.info("Following is the request : " + str(request.body))
        except:
            data = request.data.dict()
            data = json.loads(data)
            logging.info(
                "Following is the request : " + str(request.data.dict()))

        response_dict = {'status': False, "message": None}

        if not data.get('name'):
            response_dict["message"] = "Please provide the name of the company"

        if not data.get('emp_prefix'):
            if response_dict.get('message'):
                response_dict["message"] += ' and the prefix to be used'
            else:
                response_dict["message"] = "Please provide the prefix to be used"

        if response_dict.get('message'):
            return Response(data=response_dict,
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type='text/html; charset=utf-8')

        serializer = CompanySerializer(data=data)

        if serializer.is_valid():
            company = serializer.save()
            response_dict = {'company': company.id}
            return Response(status=status.HTTP_200_OK,
                            data=response_dict)
        else:
            logging.info("This is the serializer error : %s",
                         serializer.errors)
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)


class CompanyDetails(views.APIView):
    """
        Retrieve or update the driver instance
    """
    permission_classes = (AllowAny, )

    def get(self, request, pk, format=None):
        """
            Returns the driver record data corresponding to the driver id
        """
        data = {}

        company_queryset = Company.objects.filter(id=pk)
        print('This is the queryset == ', company_queryset)

        if not company_queryset:
            logging.info("Invalid company ID")
            return Response(data="Company ID does not exist",
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type='text/html; charset=utf-8')

        company_list = CompanySerializer(company_queryset, many=True)
        data["result"] = company_list.data
        return Response(status=status.HTTP_200_OK,
                        data=data)

    def put(self, request, pk, format=None):
        """
            For updating the record of the driver corresponding to the id
        """
        company_queryset = Company.objects.filter(id=pk)

        if not company_queryset:
            logging.info("Invalid company ID")
            return Response(data="Company does not exist",
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type='text/html; charset=utf-8')

        company = company_queryset.first()
        logging.info(
            "Company for which the updation is needed : %s" % str(company))

        try:
            data = json.loads(request.body)
            logging.info("Request from the app : " + str(request.body))
        except:
            data = request.data.dict()
            data = json.loads(data)
            logging.info(
                "Request from the app dict : " + str(request.data.dict()))

        response_dict = {'status': False, "message": ''}

        if not set(data.keys()).issubset(set(UPDATION_KEY_NAMES)):
            response_dict["message"] = "Please provide the valid key name"
            return Response(data=response_dict,
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type='text/html; charset=utf-8')

        serializer = CompanySerializer(data=data, instance=company)

        if serializer.is_valid():
            company = serializer.save()
            response_dict = {'company': company.id}
            return Response(status=status.HTTP_200_OK,
                            data=response_dict)
        else:
            logging.info("This is the serializer error : %s",
                         serializer.errors)
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)
