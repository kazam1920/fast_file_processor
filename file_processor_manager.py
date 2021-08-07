import os
import psycopg2
import psycopg2.extras as extras
import pandas as pd


class FastFileProcessor(object):
    def connect(self, params_dic):
        """ Connect to the PostgreSQL database server """
        conn = None
        try:
            # connect to the PostgreSQL server
            print('Connecting to the PostgreSQL database...')
            conn = psycopg2.connect(**params_dic)
        except (Exception, psycopg2.DatabaseError) as error:
            print(error)
            sys.exit(1) 
        print("Connection successful")
        return conn

    def bulk_insert_data(self, conn, df, table, truncate=False):
        """
        Here we are going save the dataframe on disk as 
        a csv file, load the csv file  
        and use copy_from() to copy it to the table
        """
        # Save the dataframe to disk
        tmp_df = "./tmp_dataframe.csv"
        df.to_csv(tmp_df, index_label='id', header=False)
        f = open(tmp_df, 'r')
        cursor = conn.cursor()
        try:
            if truncate==True:
                print('truncating')
                cursor.execute(f'Truncate table {table} CASCADE')
                print('truncated')
            print('Inserting')
            cursor.copy_from(f, f'{table}', sep=",")
            print('inserted')
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            os.remove(tmp_df)
            print("Error: %s" % error)
            conn.rollback()
            cursor.close()
            return 1
        print("bulk_insert_data completed")
        cursor.close()
        os.remove(tmp_df)

    def fetch_data(self, conn, table):
        """
        Here we are going read the database table
        as DataFrame
        """
        try:
            cursor = conn.cursor()
            sku_master = pd.read_sql(f"select * from {table}", conn);
        except Exception as e:
            error = str(e.__dict__['orig'])
            print(error)
            conn.rollback()
            cursor.close()
        cursor.close()
        return sku_master

    def data_preprocessing(self, data_chunk,sku_master):
        """
        We will map sku with sku_id ,
        Keep only name, sku_id column and drop rest of columns
        """
        data_chunk.drop(['description'], axis = 1, inplace=True)
        cleaned_data = pd.merge(data_chunk,sku_master,on='sku' , how = 'inner')
        cleaned_data.drop(['sku'], axis = 1, inplace=True)
        cleaned_data.set_index('name', inplace=True)
        return cleaned_data
    
    def truncate_table(self, conn, table):
        """
        Here we are giving option to truncate any table, 
        incase we want to clear existing table and insert fresh record
        """
        cursor = conn.cursor()
        try:
            cursor.execute(f'Truncate table {table} CASCADE')
            conn.commit()
        except (Exception, psycopg2.DatabaseError) as error:
            print("Error: %s" % error)
            conn.rollback()
            cursor.close()
            return 1
        print("bulk_insert_data completed")
        cursor.close()

