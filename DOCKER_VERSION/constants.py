# Here you want to change your database, username & password according to your own values
PARAM_DICT = {
    "host"      : "52.204.30.149",
    "database"  : "postman",
    "user"      : "large_file_processor_login",
    "password"  : "9fXmCEnq",
    "options"     : "-c search_path=file_processor"
}


#PATH = ~/Desktop/Azam_codes/project_codes/Postman/fast_processor

CHUNKSIZE = 120000
NAME_PRODUCT_AGG = "name_product_agg()"
SKU_TABLE = "sku_master"
RAW_TXN_TABLE = 'raw_transaction_data'
INPUT_FILE_PATH = '/app/to_be_processed/'
PROCESSED_FILE_PATH = '/app/processed/'
FAILED_FILE_PATH = '/app/failed/'
OUPUT_FILE_PATH = '/app/output/'
