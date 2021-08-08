-- DB and Schema creation.
create database postman;
create schema file_processor;

-- User creation.
CREATE USER large_file_processor_login WITH ENCRYPTED PASSWORD '9fXmCEnq';
ALTER USER large_file_processor_login WITH SUPERUSER;


-- sku_master
CREATE TABLE file_processor.sku_master
(
sku_id serial primary key,
sku varchar(50),
sku_description TEXT
);


-- raw_transaction_data
CREATE TABLE file_processor.raw_transaction_data
(
name varchar(50),
sku_id int , --fk
constraint fk_raw_transaction_data_sku_id foreign key (sku_id) references file_processor.sku_master(sku_id)
);


