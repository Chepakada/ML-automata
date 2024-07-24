import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from file_runner import run_new_delete_old, readable_table
from ml_algos import distinct_type
from flask import jsonify
import base64
from celery import shared_task
from flask import current_app
from ml_algos import set_column_name
# from celery_init import celery



@shared_task()
def results(file_path, column_name):
    with os.fdopen(os.open("loggor/log.txt", os.O_WRONLY | os.O_CREAT | os.O_APPEND), 'a') as f:
            f.write("testingm, reached test function\n")
            print("Reached the results function")
    try:
        print(column_name)
        set_column_name(column_name)
        print("Reached the results function")
        file = run_new_delete_old(file_path)
        
        table = readable_table(file)
        output = distinct_type(table)
        if output[0] == "RNN":
            return {"type": output[0], "output": output[1], "metrics":output[2],"image": base64.b64encode(output[3].getvalue()).decode('utf-8') }
        if output[0] == "classification":
            return {"type": output[0], "metrics":output[2],"image": base64.b64encode(output[3].getvalue()).decode('utf-8') }
        if output[0] == "linear_reg":
            return {"type": output[0], "metrics":output[2],"images": {"metric_image":base64.b64encode(output[3].getvalue()).decode('utf-8'), "scatter_image":base64.b64encode(output[4].getvalue()).decode('utf-8') }}
    except Exception as e:
        raise e 


