from flask import Flask, jsonify, request
import pandas as pd
import time
import shutil
import constants , file_processor_manager
pd.set_option('display.max_colwidth', None)


app = Flask("__name_")

@app.route('/csv_to_db', methods=['POST'])
def csv_to_db():
    i = 1
    FILE_NAME = request.args.get("file_name")
    FILE_PATH = f'{constants.INPUT_FILE_PATH}{FILE_NAME}'
    SUCCESS_PATH = f'{constants.PROCESSED_FILE_PATH}{FILE_NAME}'
    FAILED_PATH = f'{constants.FAILED_FILE_PATH}{FILE_NAME}'
    file_processor = file_processor_manager.FastFileProcessor()
    conn = file_processor.connect(constants.PARAM_DICT)
    start = time.perf_counter()
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
    OUTPUT_PATH = f'{constants.OUPUT_FILE_PATH}{FILE_NAME}'
    file_processor = file_processor_manager.FastFileProcessor()
    conn = file_processor.connect(constants.PARAM_DICT)
    sku_master = file_processor.fetch_data(conn, constants.SKU_TABLE)
    sku_master.to_csv(OUTPUT_PATH)
    finish = time.perf_counter()
    return f'Fetching sku_master completed in {round(finish-start, 2)} second(s) ,\n path : {OUTPUT_PATH}'


@app.route('/truncate_table', methods=['POST'])
def truncate_table():
    start = time.perf_counter()
    TABLE = request.args.get("table_name")
    file_processor = file_processor_manager.FastFileProcessor()
    conn = file_processor.connect(constants.PARAM_DICT)
    file_processor.truncate_table(conn,TABLE)
    finish = time.perf_counter()
    return f'{TABLE} Truncated in {round(finish-start, 2)} second(s)'


@app.route('/upsert_sku_master', methods=['POST'])
def upsert_sku_master():
    file_processor_manager = file_processor_manager.FastFileProcessor()
    conn = file_processor_manager.connect(constants.PARAM_DICT)
    start = time.perf_counter()
    sku_master = file_processor_manager.fetch_data(conn, constants.SKU_TABLE)
    return sku_master



if __name__ == '__main__':
#     app.run()
   app.run(host='127.0.0.1', port=5001,debug=True)
