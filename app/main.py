from fastapi import FastAPI, UploadFile, File,Form
from pandas_profiling import ProfileReport
import pandas as pd
from io import StringIO
import requests
import uuid
from torf import Torrent
from dotenv import load_dotenv 
import os
load_dotenv()

app = FastAPI(
    title="API",
    description="AI",
    version="1.0",
    docs_url='/docs',
    openapi_url='/openapi.json', # This line solved my issue, in my case it was a lambda function
    redoc_url='/redoc'
)

def upload_eueno(filename):
    headers = {
            'x-api-project-key': os.getenv('KEY_API_EUENO'),
            'Content-Type': 'application/json',
        }
    json_data = {
        'metadata': {
            'content_length': 440234,
            'content_type': 'text/html',
            'filename': filename,
            'action': 'write',
            'encryption': 'no',
        },
    }
    response = requests.post('https://developers.eueno.io/api/v2/api/project-file/auth-upload', headers=headers, json=json_data)
    url_upload_file = response.json()['data']['url_upload_file']
    
    
    # Upload file 
    headers = {
    'Content-Type': 'text/html',
    }
    with open(filename, 'rb') as f:
        data = f.read()
    requests.put(url_upload_file, headers=headers, data=data)


    # Gen file torrent
    t = Torrent(path=filename,
                trackers=['wss://tracker.eueno.io',
                        'https://tracker.eueno.io/announce'
                        ],
                comment= 'Pandas Profiling',
                webseeds= response.json()['data']['webseed']
                )
    t.private = True
    t.generate()
    t.write(filename + '.torrent')
    
    
    # Upload file torrent
    url_upload_torrent = response.json()['data']['url_upload_torrent']
    headers = {
    'Content-Type': 'application/x-bittorrent',
    }
    with open(filename+'.torrent', 'rb') as f:
        data_torrent = f.read()
    requests.put(url_upload_torrent, headers=headers, data=data_torrent)
    
    
    return response.json()

    
    
    
@app.get("//profiling")
async def ping():
    return 'profiling'


@app.post("//profiling")
async def profiling(file_csv: bytes  = File(...),
                ):
    s=str(file_csv,'utf-8')
    data = StringIO(s) 
    df=pd.read_csv(data)
    profile = ProfileReport(df, title="Pandas Profiling Report")
    profile.to_widgets()
    filename = str(uuid.uuid4())+'.html'
    profile.to_file(filename)
    res = upload_eueno(filename)
    try:
        os.remove(filename)
        os.remove(filename+'.torrent')
    except:
        print('No such file : '+filename+' / '+filename+'.torrent')
    return res