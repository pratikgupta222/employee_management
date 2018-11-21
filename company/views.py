import json
import logging

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
    List all Company, or create a new Company.
    """
    permission_classes = (AllowAny,)

    def get(self, request):
        """
        For fetching the existing company records

        :param request: The request param for fetching all the company records
        :return: All the company records
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
        For creating the new company record.

        :param request: The request parameters for creating a new Company.
                        The request body should be as below format:

                         {
                            "name": Name of the Company,
                            "emp_prefix": Prefix for the Employee ID
                         }

        :return: Raise error if invalid request else return response as:

                 {
                    "company": ID of the company created
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

        if not data.get('name'):
            response_dict["message"] = "Please provide the name of the company"

        if not data.get('emp_prefix'):
            if response_dict.get('message'):
                response_dict["message"] += ' and the prefix to be used'
            else:
                response_dict[
                    "message"] = "Please provide the prefix to be used"

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
        Retrieve, update or delete a Company instance.
    """
    permission_classes = (AllowAny,)

    def get(self, request, pk, format=None):
        """

        :param request:
        :param pk: Primary Key (integer) of the company
        :param format:
        :return: If the pk is valid then return the company details as:
                 {
                    "result": [
                        {
                            "id": ID of the company,
                            "name": Name of the company,
                            "emp_prefix": Prefix for the Employee ID
                        }
                    ]
                 }
        """
        data = {}

        company_queryset = Company.objects.filter(id=pk)

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

        :param request: The request parameters for updating the existing Company.
                        The request body should be as below format:

                         {
                            "name": Name of the Company,
                            "emp_prefix": Prefix for the Employee ID
                         }
        :param pk: The id of th company which has to be updated
        :param format:
        :return: If the company with corresponding id exists and the request
                 parameters are correct then return the updated company record
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

    def delete(self, request, pk, format=None):
        """

        :param request:
        :param pk: Id of the company which has to be deleted
        :param format:
        :return: Error if company doesn't exists else return nothing
        """
        try:
            company = Company.objects.get(id=pk)
        except Company.DoesNotExist:
            logging.info("Invalid company ID")
            return Response(data="Company does not exist",
                            status=status.HTTP_400_BAD_REQUEST,
                            content_type='text/html; charset=utf-8')

        company.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
