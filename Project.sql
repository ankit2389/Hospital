 CREATE TABLE patient_details (
        Name  varchar(220) NOT NULL,
        Gender varchar(220),
        Age   int NOT NULL,
        Address varchar(220),
        Doctor_recommended varchar(220)
);
CREATE TABLE doctor_details (
        Name varchar(220) primary key,
        Specialisation varchar(220),
        Age int,
        Address varchar(220),
        Contact varchar(220),
        Fees int,
        Monthly_Salary int
         
);
CREATE TABLE nurse_details (
        name varchar(220) primary key,
        age int,
        address varchar(220),
        contact varchar(220),
        monthly_salary int
        
);
CREATE TABLE other_workers_details (
        name varchar(220) primary key,
        age int,
        address varchar(220),
        contact varchar(220),
        monthly_salary int
        
);
CREATE TABLE user_data (
        username varchar(220) primary key,
        password varchar(220) default'000'
);