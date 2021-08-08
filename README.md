# fast_file_processor

## Steps to run code (Locally).
  
**Need to host postgres Database and execute table creation.sql and also follow steps mentioned in one time activity file**

**Create a virtual environment inside the application**

```python
sudo apt install virtualenv  
virtualenv -p /usr/bin/python3 fast_processor  
source fast_processor/bin/activate
```

**Install Python modules**  

```python
   sudo apt-get install python3-pip  
   sudo apt install python3-dev libpq-dev  
   pip3 install -r LOCAL_VERSION/requirements.txt  
```


**Run the application using**  

```python
    python3 app.py
```

## Steps to run code (In Docker).

**Need to host postgres Database (Remote server) and execute table creation.sql and also follow steps mentioned in one time activity file**

**Install docker latest version on your system**  
for ubuntu 18.0.04 --> https://phoenixnap.com/kb/how-to-install-docker-on-ubuntu-18-04

**Build Docker Image** (This will take around 20 min)
```sh
cd DOCKER_VERSION
#docker build -t <imageName:version> dockerFilePath
docker build -t file-processor:latest .
```
**Run Docker Container in deamon mode**
```sh
#docker run -it -d -p <outsidePort>:<dockerInsidePort> <imageName:version>
docker run -it -d -p 5000:5000 file-processor:latest
```

**List of API's with parameter**  

1. csv_to_db  (Exec time: localDB --> ~12 Sec ,RemoteDB --> )
It takes csv file name `file_name` as input and dump csv (name,sku,description) file data in raw_transaction_table,  
Before calling API make sure you have .csv file on below PATH  
a. `fast_file_processor/LOCAL_VERSION/to_be_processed/<filename>` for LOCAL_VERSION  
b. `<container_name>:/app/to_be_processed/<filename>` for DOCKER_VERSION  
To copy file to docker path refer `docker cp products.csv <container_name>:app/to_be_processed/products.csv`  
After successfull insertion file will be moved to `processed` directory else in `failed` directory  

sample --> http://127.0.0.1:5000/csv_to_db?file_name=products.csv

2. upsert_sku_master  (Exec time: localDB --> ~40 Sec,RemoteDB --> )
It takes csv file name, table name `file_name , table_name` as input. it updates existing sku data and insert only new records (sku,description) file data in sku_master,  
Before calling API make sure you have .csv file on below PATH  
a. `fast_file_processor/LOCAL_VERSION/to_be_processed/<filename>` for LOCAL_VERSION  
b. `<container_name>:/app/to_be_processed/<filename>` for DOCKER_VERSION  
To copy file to docker path refer `docker cp sku_master.csv <container_name>:app/to_be_processed/sku_master.csv`  
After successfull insertion file will be moved to `processed` directory else in `failed` directory  

sample --> http://192.168.0.101:5000/upsert_sku_master?table_name=sku_master&file_name=sku_master.csv

3. get_sku_master  (Exec time: localDB --> ~3 Sec,RemoteDB --> )
It takes csv output file name, table name `op_file_name , table_name` as input. it directly hits select query against table/function name and returns the result as csv file in `output` directory,  
same API is used to get aggregated name, number of products value if we pass `name_product_agg` as table name.  

To get Agg result --> http://192.168.0.101:5000/get_sku_master?op_file_name=name_product_agg.csv&table_name=name_product_agg  
To get raw tables --> http://192.168.0.101:5000/get_sku_master?op_file_name=sku_master.csv&table_name=sku_master

4. truncate_table  (Exec time: localDB --> ~1 Sec,RemoteDB --> )
It takes table name `table_name` as input, and truncate particular table.  

sample --> http://192.168.0.101:5000/truncate_table?table_name=raw_transaction_data

  
## Details of all the tables and their schema, [with commands to recreate them]  
We have created a normalized data model to increase the insert performance,  

Data model:  

1. **sku_master**  (Records --> 466693)  
&nbsp;&nbsp;&nbsp;&nbsp;Columns:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sku_id --> primary key (auto incremented values)  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sku --> sku code  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sku_description --> actual description of skuas per products.csv file  

&nbsp;&nbsp;&nbsp;&nbsp;Script:  
```sql
CREATE TABLE file_processor.sku_master  
(  
sku_id serial primary key,  
sku varchar(50),  
sku_description TEXT  
);  
ALTER TABLE file_processor.sku_master ADD CONSTRAINT sku_master_un UNIQUE (sku);  
```        
&nbsp;&nbsp;&nbsp;&nbsp;Sample Data:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;postman=# select * from file_processor.sku_master limit 10;  
    
   ![Screenshot from 2021-08-07 13-47-47](https://user-images.githubusercontent.com/30022078/128593817-67b2f456-46f4-4e4f-a990-1089b9dcc340.png)


2. **raw_transaction_data**  (Records --> 500000)  
&nbsp;&nbsp;&nbsp;&nbsp;Columns:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;name --> actual name from product.csv  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;sku_id --> numeric sku value, foriegn key to sku_master  

&nbsp;&nbsp;&nbsp;&nbsp;Script:  
```sql
CREATE TABLE file_processor.raw_transaction_data  
(  
name varchar(50),  
sku_id int , --fk  
constraint fk_raw_transaction_data_sku_id foreign key (sku_id) references file_processor.sku_master(sku_id)  
);  
```
&nbsp;&nbsp;&nbsp;&nbsp;Sample Data:  
&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;postman=# select * from file_processor.raw_transaction_data limit 10;  

![Screenshot from 2021-08-07 13-49-17](https://user-images.githubusercontent.com/30022078/128593871-aec6f88d-04e0-43c8-b3d3-51b60351353b.png)

    
    
## What is done from “Points to achieve”    

1. Used OOPS Concepts  
2. File is processed within 10 seconds on local machine, and tested same on aws hosted instance it was completed in 40 seconds it usually depends on internet speed. (performance is already fast so didn't used multithreading)  
3. It Supports for updating existing products description in the sku_master, used UPSERT but to achieve incremental import (SCD-2) used multiThreading.  
4. All product details are ingested into a single table (raw_transactions_data).  
5. Used Postgres function to generate `name` and `no. of products` aggregated value, as a CSV file.  


## What is not done from “Points to achieve”. If not achieved, write the possible reasons and current workarounds.  

Covered all mentioned requirements as per my understanding, Although requirements are not much clear, so there is high possibility of change request once analysed by reviewer.  


## What would you improve if given more days  

1. Proper auditing and alerting mechanism in case of sucess or failure needs to be maintained.  
2. Instead of Docker , i'll host this application in AWS lambda and it will triggered automatically whenever csv file is uploaded to specified S3 path.
