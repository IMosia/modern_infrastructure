"""
Module for uploading pictures to the AWS s3 bucket
"""

import requests
import boto3
from aiohttp import web
import os
import dotenv


dotenv.load_dotenv()
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
REGION_NAME = os.getenv('AWS_REGION')

async def request_handler(request):
    """
    Handler for requests
    """
    data = await request.json()
    link = data['link']
    picture_name = data['picture_name']
    bucket_name = data['bucket_name']
    response = requests.get(link)
    s3 = boto3.client('s3', region_name=REGION_NAME,
            aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    if response.status_code == 200:
        s3.put_object(Bucket=bucket_name, Key=picture_name, Body=response.content)
        print(f"Picture {picture_name} uploaded to S3, address: {bucket_name}/{picture_name}")
    else:
        print(f"Error while uploading picture to S3: {response.status_code} \n {response.text}")
    # somehow a bit different it should be TODO
    return web.json_response({'status': 'ok'})

def main():
    app = web.Application()
    app.router.add_post('/api/request', request_handler)
    web.run_app(app, port=5001)

if __name__ == '__main__':
    main()
