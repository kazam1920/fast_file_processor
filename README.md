# fast_file_processor

#### Steps to run your code. As less steps we are to run, better for you (Hint: Docker)


#### Details of all the tables and their schema, [with commands to recreate them]
We have created a normalized data model to increase the insert performance,

Data model:

1. sku_master 
    Columns:
        sku_id --> primary key (auto incremented values) 
        sku --> sku code 
        sku_description --> actual description of skuas per products.csv file
    Script:
        CREATE TABLE file_processor.sku_master
        (
        sku_id serial primary key,
        sku varchar(50),
        sku_description TEXT
        );

    Sample Data:
    postman=# select * from file_processor.sku_master limit 10;
    
    ![Screenshot from 2021-08-07 13-47-47](https://user-images.githubusercontent.com/30022078/128593817-67b2f456-46f4-4e4f-a990-1089b9dcc340.png)


2. raw_transaction_data
    Columns:
        name --> actual name from product.csv
        sku_id --> numeric sku value, foriegn key to sku_master

    Script:
        CREATE TABLE file_processor.raw_transaction_data
        (
        name varchar(50),
        sku_id int , --fk
        constraint fk_raw_transaction_data_sku_id foreign key (sku_id) references file_processor.sku_master(sku_id)
        );

    Sample Data:
    postman=# select * from file_processor.raw_transaction_data limit 10;

![Screenshot from 2021-08-07 13-49-17](https://user-images.githubusercontent.com/30022078/128593871-aec6f88d-04e0-43c8-b3d3-51b60351353b.png)

    
    
#### What is done from “Points to achieve” and number of entries in all your tables with sample 10 rows from each

#### What is not done from “Points to achieve”. If not achieved, write the possible reasons and current workarounds.

#### What would you improve if given more days
