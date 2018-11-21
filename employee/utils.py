import re
import datetime
import logging
from django.conf import settings
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

from phonenumber_field.phonenumber import PhoneNumber
from company.models import Company


def validate_email_add(email):
    if not email:
        logging.info("Email address not found")
        raise ValidationError('Email is mandatory')

    try:
        validate_email(email)
        return email
    except ValidationError as e:
        raise ValidationError(e)


def validate_name(name):
    """
    :param name: Name to be validated
    :return: name if it is valid else False
    """
    # Name should be only alphabetic and can have only single space between
    # adjacent words
    reg_exp = re.compile(r"^([A-Za-z]){1}( ?[A-Za-z]){1,}$", re.IGNORECASE)
    match = reg_exp.match(name)
    if match is not None:
        return name
    else:
        return False


def generate_employee_uid(company_id, emp_num):
    company = Company.objects.filter(id=company_id)

    if not company:
        logging.info("No company details found for the given id")
        raise ValidationError('Invalid company id')

    company = company.first()

    emp_prefix = company.emp_prefix

    uid = emp_prefix + '-' + str(emp_num)

    # return {'uid': uid, 'company': company}
    return uid


def validate_phone_number(phone_number):
    """
    Validation Rule for the phone number used are as below:
        - Phone number should be of exactly 10 digits
        - If the phone number starts with 0 then it should immidiately be followed by a
          non-zero digit and then any digit between 0 to 9 else it will result into error
        - If the phone number starts with non-zero digit then it can be
          followed by any digit including zero
    """
    print("This is the phone number ==== ", phone_number)
    phn_exp = re.compile(r"^(([0]{1})([1-9]{1})|([1-9]{1})([0-9]{1}))(\d{8})$")
    match = phn_exp.match(phone_number)
    if match is not None:
        phone_number = PhoneNumber(
            settings.DEFAULT_COUNTRY.get('isd_code'), phone_number)
        return phone_number
    else:
        raise ValidationError("Please enter a valid ten digit number")


def validate_employee_data(params):
    """
        Validating the requested data and raising error(if any).
    """
    response = {'error': '', 'success': False, 'data': {}}

    print("This is the params inside the validation of the data ==== ", params)

    # To check if the requested dictionary is not empty
    if not params:
        logging.info("employee details not found")
        response["error"] = "employee details not found"
        return response

    # To validate the email of the employee
    try:
        validate_email_add(params.get('email', ''))
    except ValidationError as e:
        logging.info(
            "Error while validating the employee phone number : %s " % e)
        response['error'] = str(e.args[0])
        return response

    # To validate the phone number of the employee
    try:
        params['phone'] = validate_phone_number(params.get('phone', ''))
    except ValidationError as e:
        logging.info(
            "Error while validating the employee phone number : %s " % e)
        response['error'] = str(e.args[0])
        return response

    # To check if employee number is present or not
    if not params.get('emp_number', ''):
        logging.info("No Employee Number was found")
        response['error'] = 'Please Enter a valid Employee Number'
        return response

    # To validate the company of the employee
    if not params.get('company_id'):
        logging.info("No company details found")
        response['error'] = 'Please enter the valid company details of the employee'
        return response
    else:
        try:
            params['uid'] = generate_employee_uid(
                params['company_id'], params['emp_number'])
            params['company'] = params.pop('company_id')
        except ValidationError as e:
            logging.info(
                "Error while generating the employee uid : %s " % e)
            response['error'] = str(e.args[0])
            return response

    # To validate the first name of the employee
    if not validate_name(params.get('fname', '')):
        logging.info("Please Enter a valid first name")
        response['error'] = 'Please Enter a valid first name'
        return response

    # To validate the last name of the employee
    if not validate_name(params.get('lname', '')):
        logging.info("Please Enter a valid last name")
        response['error'] = 'Please Enter a valid last name'
        return response

    response['success'] = True
    response['data'] = params
    return response


def get_updation_data(params, employee):
    response = {'error': '', 'success': False, 'data': {}}

    if not all(val for val in list(params.values())):
        logging.info("Some keys were having empty/null value")
        response['error'] = 'No Empty/Null value is allowed'
        return response

    data = {
        'company_id': params['company_id']
        if params.get('company_id') else employee.company_id,
        'fname': params['fname']
        if params.get('fname') else employee.fname,
        'lname': params['lname']
        if params.get('lname') else employee.lname,
        'phone': params['phone']
        if params.get('phone') else str(employee.phone.national_number).zfill(10),
        'email': params['email']
        if params.get('email') else employee.email,
        'role': params['role']
        if params.get('role') else employee.role,
        'emp_number': params['emp_number']
        if params.get('emp_number') else employee.emp_number,
    }
    print("This is the data for the updation of the employee ===== ", data)

    return validate_employee_data(params=data)
