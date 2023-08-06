# Google Imports
from google.cloud import firestore
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
# Other imports
import datetime, os


def Connect_Firestore(project_id):
    return firestore.Client(project=project_id)


def Debug_Connect_Firestore():
    service_account_file = os.path.dirname(os.path.realpath(__file__)) + '/service-account-info.json'
    cred = credentials.Certificate(service_account_file)
    firebase_admin.initialize_app(cred)
    return firestore.client()


def Get_Task(client, task_id):
    task = client.collection(u'jobs').document(task_id).get()
    return task()


def Get_Task_As_Dict(client, task_id):
    task = client.collection(u'jobs').document(task_id).get()
    return task.to_dict()


def Block_Task(client, task_id):
    doc = client.collection(u'jobs').document(task_id)
    doc.update({
        "status": "RUNNING"
    })


def Update_Task(task, status:str, extraction:str, extracted_campaigns:int, extracted_rows:int, start_date:str, end_date:str):
    task_dict = task.to_dict()
    next_schedule = task_dict['schedule']['next_schedule']

    if extraction == 'LOAD':
        delay = task_dict['schedule']['on_load']
    elif extraction == 'UPDATE':
        delay = task_dict['schedule']['on_update']
    else: print('Extraction was neither LOAD nor UPDATE')
    if status == "FAILED":
        delay = task_dict['schedule']['on_fail']

    task.update({
        "status": "SCHEDULED",
        "last_status": status,
        "scheduled": next_schedule + datetime.timedelta(0, delay),
    })

    task.update({
        "history": firestore.ArrayUnion([{
            "date": datetime.datetime.now(),
            "extracted_campaigns": extracted_campaigns,
            "extracted_rows": extracted_rows,
            "start_date": start_date,
            "end_date": end_date,
            "status": status
        }]) 
    })

def Get_Last_History_Entry(task):
    task_dict = task.to_dict()
    history = task_dict['history']
    history_count = len(history)
    return history[history_count - 1]