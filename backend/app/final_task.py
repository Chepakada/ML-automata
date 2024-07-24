import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from file_runner import run_new_delete_old, readable_table
from ml_algos import distinct_type
from flask import jsonify
import base64
from celery import shared_task
from flask import current_app
# from celery_init import celery



@shared_task()
def results(file_path):
    try:
        print("Reached the results function")
        file = run_new_delete_old(file_path)
        
        table = readable_table(file)
        output = distinct_type(table)
        if output[0] == "RNN":
            return jsonify({"type": output[0], "output": output[1], "metrics":output[2],"image": base64.b64encode(output[3].getvalue()).decode('utf-8') }) 
        if output[0] == "classification":
            return jsonify({"type": output[0], "metrics":output[2],"image": base64.b64encode(output[3].getvalue()).decode('utf-8') }) 
        if output[0] == "linear_reg":
            return jsonify({"type": output[0], "metrics":output[2],"images": {"metric_image":base64.b64encode(output[3].getvalue()).decode('utf-8'), "scatter_image":base64.b64encode(output[4].getvalue()).decode('utf-8') }})  
    except Exception as e:
        raise e 


