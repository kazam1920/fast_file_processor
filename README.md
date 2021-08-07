# fast_file_processor

### Steps to run your code. As less steps we are to run, better for you (Hint: Docker)


### Details of all the tables and their schema, [with commands to recreate them]
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
    postman=# select * from file_processor.sku_master limit 5;

         sku_id |         sku         |                                                                                             sku_description                                                                                             
--------+---------------------+---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
      1 | a-ability-see-gun   | According member fine program. Concern single too ahead my. Loss onto which include listen later present.        Election sport quite notice why. Find system writer might. Sing prevent compare black.
      2 | a-above-its-focus   | Go audience old. Law main federal area myself.   Leave various leave discover consumer hotel. Safe fall up compare plant affect stuff.
      3 | a-act-cut-either    | Data tell enter. Because stock along continue follow respond off value. Trial try exactly type simply full.
      4 | a-activity          | Discussion itself those stand beat Mr. Any from event.   Training cultural avoid artist quite say figure. Play fill cultural know education arm rate reflect. Me investment pull star.
      5 | a-act-spring-camera | Difference compare society best structure democratic team machine. Administration item light among.      Each when capital condition election miss defense. Left after treat listen law girl.
(5 rows)



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
                              name       | sku_id 
                        -----------------+--------
                         Bryce Jones     | 211773
                         John Robinson   |  92587
                         Theresa Taylor  | 384663
                         Roger Huerta    |  74265
                         John Buckley    | 403219
                         Tiffany Johnson | 108981
                         Roy Golden DDS  | 175567
                         David Wright    | 220305
                         Anthony Burch   |  22452
                         Lauren Smith    | 167266
                        (10 rows)
### What is done from “Points to achieve” and number of entries in all your tables with sample 10 rows from each

### What is not done from “Points to achieve”. If not achieved, write the possible reasons and current workarounds.

### What would you improve if given more days
