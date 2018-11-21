import json
import logging
import datetime

from django import db
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from employee.models import Employee
from employee.serializers import EmployeeSerializer
from employee.utils import validate_employee_data, get_updation_data
# from employee.constants import UPDATION_KEY_NAMES


# Create your views here.


class EmployeeList(views.APIView):
    """
        List all the filtered employee records or create a new record
    """
    permission_classes = (AllowAny, )

    def get(self, request):
        """
            For fetching all the employees for the given city
        """
        data = {}

        employee_queryset = Employee.objects.all()

        if employee_queryset:
            employee_list = EmployeeSerializer(employee_queryset, many=True)
            data["result"] = employee_list.data
            return Response(status=status.HTTP_200_OK,
                            data=data)

        else:
            return Response(
                status=status.HTTP_404_NOT_FOUND,
                data='No employee found')

    def post(self, request):
        """
            For creating a new employee
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

        validated_data = validate_employee_data(params=data)

        if not validated_data.get('success'):
            response_dict["message"] = validated_data.get('error')
            return Response(data=response_dict,
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type='text/html; charset=utf-8')

        print("This is the validated data ========= ", validated_data)

        with db.transaction.atomic():
            serializer = EmployeeSerializer(data=validated_data.get('data'))

            if serializer.is_valid():
                serializer.save()
                response_dict = {'employee': serializer.data}
                return Response(status=status.HTTP_201_CREATED,
                                data=response_dict)
            else:
                logging.info("This is the serializer error : %s",
                             serializer.errors)
                return Response(data=serializer.errors,
                                status=status.HTTP_400_BAD_REQUEST)


class EmployeeDetails(views.APIView):
    """
        Retrieve or update the employee instance
    """
    permission_classes = (AllowAny, )

    def get(self, request, pk, format=None):
        """
            Returns the employee data corresponding to the employee id
        """
        data = {}

        employee_queryset = Employee.objects.filter(id=pk)

        if not employee_queryset:
            logging.info("Invalid employee ID")
            return Response(data="Employee ID does not exist",
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type='text/html; charset=utf-8')

        employee_list = EmployeeSerializer(employee_queryset, many=True)
        data["result"] = employee_list.data
        return Response(status=status.HTTP_200_OK,
                        data=data)

    def put(self, request, pk, format=None):
        """
            For updating the record of the employee corresponding to the id
        """
        employee_queryset = Employee.objects.filter(id=pk)

        if not employee_queryset:
            logging.info("Invalid employee ID")
            return Response(data="Employee does not exist",
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type='text/html; charset=utf-8')

        employee = employee_queryset.first()
        logging.info(
            "employee for which the updation is needed : %s" % str(employee))

        try:
            data = json.loads(request.body)
            logging.info("Request from the app : " + str(request.body))
        except:
            data = request.data.dict()
            data = json.loads(data)
            logging.info(
                "Request from the app dict : " + str(request.data.dict()))

        response_dict = {'status': False, "message": ''}

        updation_data = get_updation_data(params=data, employee=employee)

        if not updation_data.get('success'):
            response_dict["message"] = updation_data.get('error')
            return Response(data=response_dict,
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type='text/html; charset=utf-8')

        serializer = EmployeeSerializer(
            data=updation_data.get('data'), instance=employee)

        if serializer.is_valid():
            employee = serializer.save()
            response_dict = {'employee': employee.id}
            return Response(status=status.HTTP_200_OK,
                            data=response_dict)
        else:
            logging.info("This is the serializer error : %s",
                         serializer.errors)
            return Response(data=serializer.errors,
                            status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
    	try:
    		employee = Employee.objects.get(id=pk)
    	except Employee.DoesNotExist:
    		logging.info("Invalid employee ID")
    		return Response(data="Employee does not exist",
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type='text/html; charset=utf-8')

    	employee.delete()
    	return Response(status=status.HTTP_204_NO_CONTENT)
