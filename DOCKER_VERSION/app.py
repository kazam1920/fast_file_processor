from flask import Flask, jsonify, request
import pandas as pd
import time
import shutil
import constants , file_processor_manager
import threading
pd.set_option('display.max_colwidth', None)


app = Flask("__name_")

@app.route('/csv_to_db', methods=['POST'])
def csv_to_db():
    i = 1
    FILE_NAME = request.args.get("file_name")
    FILE_PATH = f'{constants.INPUT_FILE_PATH}{FILE_NAME}'
    SUCCESS_PATH = f'{constants.PROCESSED_FILE_PATH}{FILE_NAME}'
    FAILED_PATH = f'{constants.FAILED_FILE_PATH}{FILE_NAME}'
    start = time.perf_counter()
    file_processor = file_processor_manager.FastFileProcessor()
    conn = file_processor.connect(constants.PARAM_DICT)
    sku_master = file_processor.fetch_data(conn, constants.SKU_TABLE)
    sku_master.drop(['sku_description'], axis = 1, inplace=True)
    try:
        for data_chunk in pd.read_csv(FILE_PATH, chunksize=constants.CHUNKSIZE, iterator=True):
            cleaned_data = file_processor.data_preprocessing(data_chunk,sku_master)
            file_processor.bulk_insert_data(conn, cleaned_data, constants.RAW_TXN_TABLE)
            print(f'Batch : {i} uploaded')
            i+=1
        shutil.move(FILE_PATH,SUCCESS_PATH)
    except Exception as e:
        error = str(e.__dict__['orig'])
        print(error)
        shutil.move(FILE_PATH,FAILED_PATH)
        return f'Data insertion failed : {error}'
    finish = time.perf_counter()
    return f'Data insertion completed in {round(finish-start, 2)} second(s)'

@app.route('/get_sku_master', methods=['POST'])
def get_sku_master():
    start = time.perf_counter()
    FILE_NAME = request.args.get("op_file_name")
    TABLE = constants.SKU_TABLE if request.args.get("table_name") == 'sku_master' else constants.NAME_PRODUCT_AGG
    OUTPUT_PATH = f'{constants.OUPUT_FILE_PATH}{FILE_NAME}'
    file_processor = file_processor_manager.FastFileProcessor()
    conn = file_processor.connect(constants.PARAM_DICT)
    op_table = file_processor.fetch_data(conn, TABLE)
    op_table.to_csv(OUTPUT_PATH)
    finish = time.perf_counter()
    return f'Fetching {TABLE} completed in {round(finish-start, 2)} second(s) ,\n path : {OUTPUT_PATH}'


@app.route('/truncate_table', methods=['POST'])
def truncate_table():
    start = time.perf_counter()
    TABLE = request.args.get("table_name")
    file_processor = file_processor_manager.FastFileProcessor()
    conn = file_processor.connect(constants.PARAM_DICT)
    file_processor.truncate_table(conn,TABLE)
    finish = time.perf_counter()
    return f'{TABLE} Truncated in {round(finish-start, 2)} second(s)'

@app.route('/test', methods=['POST'])
def test():
    c = file_processor_manager.FastFileProcessor()
    file_processor = file_processor_manager.FastFileProcessor()
    return f'{type(c)}, {type(file_processor)}'

@app.route('/upsert_sku_master', methods=['POST'])
def upsert_sku_master():
    start = time.perf_counter()
    file_processor = file_processor_manager.FastFileProcessor()
    conn = file_processor.connect(constants.PARAM_DICT)
    TABLE = request.args.get("table_name")
    FILE_NAME = request.args.get("file_name")
    FILE_PATH = f'{constants.INPUT_FILE_PATH}{FILE_NAME}'
    SUCCESS_PATH = f'{constants.PROCESSED_FILE_PATH}{FILE_NAME}'
    FAILED_PATH = f'{constants.FAILED_FILE_PATH}{FILE_NAME}'
    col_list = ["sku", "sku_description"]
    threads = []
    try:
        for df in pd.read_csv(FILE_PATH,index_col = False,usecols=col_list ,chunksize=constants.CHUNKSIZE, iterator=True):
            t = threading.Thread(target=file_processor.execute_batch, args=[conn, df, TABLE])
            t.start()
            threads.append(t)
        for thread in threads:
            thread.join()
        shutil.move(FILE_PATH,SUCCESS_PATH)
    except Exception as e:
        error = str(e.__dict__['orig'])
        print(error)
        shutil.move(FILE_PATH,FAILED_PATH)
        return f'{TABLE} UPSERT failed : {error}'
    finish = time.perf_counter()
    return f'{TABLE} UPSERT completed in {round(finish-start, 2)} second(s)'



#if __name__ == '__main__':
#    app.run()
#   app.run(host='0.0.0.0', debug=True)
