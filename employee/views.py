import json
import logging

from django import db

from rest_framework import views, status
from rest_framework.response import Response
from rest_framework.decorators import permission_classes
from rest_framework.permissions import AllowAny

from employee.models import Employee
from employee.serializers import EmployeeSerializer
from employee.utils import validate_employee_data, get_updation_data


class EmployeeList(views.APIView):
    """
    List all Employee, or create a new Employee.
    """

    permission_classes = (AllowAny,)

    def get(self, request):
        """
        For fetching the existing employee records

        :param request: The request param for fetching all the employee records
        :return: All the employee records
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
        For creating a new employee.

        :param request: The request parameters for creating a new Employee.
                        The request body should be as below format:

                         {
                            "fname": First name of the employee,
                            "lname": Last name of the employee,
                            "phone": Phone number of the employee,
                            "email": Email of the employee,
                            "role": The role of the employee in the company, it
                                    can either be regular or admin,
                            "emp_number": The current enrollment count of the
                                          employee in the company,
                            "company_id": The id of the company to which the
                                          employee belong
                         }
        :return: Raise error if invalid request else return response as:

                 {
                    "employee": {
                        "id": The id of the newly created employee,
                        "uid": Unique id of the employee generated using the
                               company's employee prefix and the employee number,
                        "fname": First name of the employee,
                        "lname": Last name of the employee,
                        "phone": Phone number of the employee,
                        "email": Email of the employee,
                        "role": The role of the employee in the company,
                        "emp_number": The current enrollment count of the
                                          employee in the company,
                        "company": The id of the company of the employee
                    }
                 }
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
    Retrieve, update or delete a Employee instance.
    """

    permission_classes = (AllowAny,)

    def get(self, request, pk, format=None):
        """

        :param request:
        :param pk: Primary Key (integer) of the employee
        :param format:
        :return: If the pk is valid then return the employee details as:
                 {
                    "result": [
                        {
                            "id": The id of the newly created employee,
                            "uid": Unique id of the employee generated using the
                               company's employee prefix and the employee number,
                            "fname": First name of the employee,
                            "lname": Last name of the employee,
                            "phone": Phone number of the employee,
                            "email": Email of the employee,
                            "role": The role of the employee in the company,
                            "emp_number": The current enrollment count of the
                                          employee in the company,
                            "company": The id of the company of the employee
                        }
                    ]
                 }
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

        :param request: The request parameters for updating the existing
                        Employee. The request body should be as below format:

                        {
                            "fname": First name of the employee,
                            "lname": Last name of the employee,
                            "phone": Phone number of the employee,
                            "email": Email of the employee,
                            "role": The role of the employee in the company, it
                                    can either be regular or admin,
                            "emp_number": The current enrollment count of the
                                          employee in the company,
                            "company_id": The id of the company to which the
                                          employee belong
                        }

                        ** All the fields are optional. Request params should
                        have only those fields which are to be updated
        :param pk: The id of th employee which has to be updated
        :param format:
        :return: If the company with corresponding id exists and the request
                 parameters are correct then return the updated company record
                 as:

                 {
                    "employee": ID of the employee updated
                 }

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
        """

        :param request:
        :param pk: Id of the company which has to be deleted
        :param format:
        :return: Error if company doesn't exists else return nothing
        """
        try:
            employee = Employee.objects.get(id=pk)
        except Employee.DoesNotExist:
            logging.info("Invalid employee ID")
            return Response(data="Employee does not exist",
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type='text/html; charset=utf-8')

        employee.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
