# employee_management
A simple employee management system for the company

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

Below mentioned are the 

* It will be better to have a virtual environment created for the project in the same folder where the project resides.
For creating the virtual environment refer:
    * [How to install virtual environment ](https://gist.github.com/Geoyi/d9fab4f609e9f75941946be45000632b)
* Install Mysql on your system if not already present and create a database for the project. Follow the steps to do the same:
    * [Install MySQL](https://dev.mysql.com/doc/mysql-apt-repo-quick-guide/en/)
    * [Creating Database](https://dev.mysql.com/doc/refman/8.0/en/creating-database.html)

### Installing
To clone and run this application, run the below mentioned from your command line:

##### Clone this repository
```commandline
$ git clone https://github.com/pratikgupta222/employee_management.git
```

##### Go into the repository
```commandline
$ cd employee_management/
```

##### Install dependencies
```commandline
$ pip install -r requirements.txt
```

#####Setting Django up to use your MySQL database
Go to the **settings** file and in the _DATABASE_ dictionary shown below, replace **DB_NAME** with the database you created and **DB_USER** and **DB_PASSWORD** with your MySQL username and password respectively.

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', 
        'NAME': 'DB_NAME',
        'USER': 'DB_USER',
        'PASSWORD': 'DB_PASSWORD',
        'HOST': 'localhost',   # Or an IP Address that your DB is hosted on
        'PORT': '',
    }
}
```

## Test the Project
Below are the example curl commands for the APIs
* For adding a company
    ```rest
     curl -X POST http://127.0.0.1:8000/company/companies -H 'Content-Type: application/json' -H 'cache-control: no-cache' -d ' {"name": "Instahyre","emp_prefix": "IH" }'
    ``` 
* For fetching the list of the companies
    ```rest
    curl -X GET http://127.0.0.1:8000/company/companies -H 'Content-Type: application/json' -H 'cache-control: no-cache'
    ```
* For fetching the details of a specific company
    ```rest
    curl -X GET http://127.0.0.1:8000/company/companies/1/ -H 'Content-Type: application/json' -H 'cache-control: no-cache'
    ```
* For updating the details of a company
    ```rest
    curl -X PUT http://127.0.0.1:8000/company/companies/1/ -H 'Content-Type: application/json' -H 'cache-control: no-cache' -d '{
	    "name": "Comp_Name",
	    "emp_prefix": "CN"
    }'
    ```
***
* For adding a employee
    ```rest
    curl -X POST http://127.0.0.1:8000/employee/employees -H 'Content-Type: application/json' -H 'cache-control: no-cache' -d '{
	    "fname": "Ram",
	    "lname": "Lal",
	    "phone": "9089098908",
	    "email": "ramlal@gmail.com",
	    "role": "admin",
	    "emp_number": 1,
	    "company_id": 3
    }'
    ``` 

* For fetching the list of the employees
    ```rest
    curl -X GET http://127.0.0.1:8000/employee/employees -H 'cache-control: no-cache'
    ```
* For fetching the details of a specific employee
    ```rest
    curl -X GET http://127.0.0.1:8000/employee/employees/3/ -H 'cache-control: no-cache'
    ```
* For updating the details of a company
    ```rest
    curl -X PUT http://127.0.0.1:8000/employee/employees/2/ -H 'Content-Type: application/json' -H 'cache-control: no-cache' -d '{
	    "email": "ramlala@gmail.com"
    }'
    ```
* For deleting a employee record
     ```rest
     curl -X DELETE http://127.0.0.1:8000/employee/employees/7/ -H 'cache-control: no-cache'
     ```