import requests
from requests_toolbelt import MultipartEncoder
import json
from dotenv import load_dotenv
import os
import time

load_dotenv()
api_key = os.getenv('API_KEY')
user_email = os.getenv('USER_EMAIL')
account_ID = os.getenv('ACCOUNT_ID')

class Encode_Metadata:
    def __init__(self, *args):
        self.formated_meta = args



    def direct_request_encoder(self):

        mutipart_data = MultipartEncoder(fields={
            'metadata': json.dumps(self.formated_meta),
            'requireSignedURLs': 'false'

        })
        return mutipart_data

    def upload_request_encoder(self, img_file):
        mutipart_data = MultipartEncoder(fields={
            'metadata': json.dumps(self.formated_meta),
            'requireSignedURLs': 'false',
            'file': (img_file, open(img_file, 'rb'), 'image/jpeg')
        })
        return mutipart_data

    def update_request_encoder(self):
        mutipart_data = MultipartEncoder(fields={

            #'id': img_name,
            #'metadata': json.dumps(metadata),
            #'requireSignedURLs': is_private,
            #'file': 'null'
            #'file': (img_file, open(img_file, 'rb'), 'image/jpeg')
        })
#--------------------------------------------------------------------------------------------------------------#
# Test for class Encode_Metadata:
#listed = [{'height': 5}, {'hair color': "brown"}]

#start = Encode_Metadata(*listed)

#--------------------------------------------------------------------------------------------------------------#

class APICall:

    def __int__(self):
        super().__init__()

    def auth_direct_upload(self, encoded_data, ):
        url = f'https://api.cloudflare.com/client/v4/accounts/{account_ID}/images/v2/direct_upload'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-type': encoded_data.content_type,
            'X-Auth-Email': user_email
        }
        response = requests.post(url, headers=headers, data=encoded_data)
        print(response.text)
        cloudflare_id = response.json()["result"]["id"]
        print('id ', cloudflare_id)
        return cloudflare_id

    def front_end_upoload(self, encoded_data, cloudflare_id, metadata, img_file):

        url = 'https://upload.imagedelivery.net/4_y5kVkw2ENjgzV454LjcQ/' + cloudflare_id
        print(url)
        meta_list = metadata
        headers = {
            'Content-type': encoded_data.content_type,
        }
        response = requests.post(url, headers=headers, data=meta_list)
        print(response.text)

    def back_end_upoload(self, meta_passed, img_file):
        print('made it')
        title, author, meta_tag, client, category, private, group = meta_passed
        metadata_packed = {
            'title': title,
            'author': author,
            'meta_tag': meta_tag,
            'client': client,
            'category': category,
            'group': group
        }
        print('encoding')
        # when encoding a mulitpart/form-data

        encoded_data = MultipartEncoder(fields={
            'metadata': json.dumps(metadata_packed),
            'requireSignedURLs': 'false',
            'file': (img_file, open(img_file, 'rb'), 'image/jpeg')

        })
        url = f'https://api.cloudflare.com/client/v4/accounts/{account_ID}/images/v1'
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-type': encoded_data.content_type,
            'X-Auth-Email': user_email
        }

        print('responding')
        time.sleep(10)
        response = requests.post(url, headers=headers, data=encoded_data)
        print(response.text)


    def get_image_usage(self, meta_passed):
        pass

    def list_images(self, meta_passed):
        pass

    def delete_image(self, meta_passed):
        pass

    def image_details(self, meta_passed):
        pass

    def image_download(self, meta_passed):
        pass

    def image_update(self, meta_passed, cloudflare_id):
        print(meta_passed, cloudflare_id)

        title, author, meta_tag, client, category, private, group = meta_passed

        metadata_packed = {
           'title': title,
           'author': author,
           'meta_tag': meta_tag,
           'client': client,
           'category': category,
           'group': group
        }

        url = f'https://api.cloudflare.com/client/v4/accounts/{account_ID}/images/v1/{cloudflare_id}'
        print(url)

        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-type': 'application/json',
            'X-Auth-Email': user_email
        }
        data = {
            'metadata': metadata_packed,
            'requireSignedURLs': private
        }
        print(data, headers)
        time.sleep(15)
        response = requests.patch(url, headers=headers, json=data)
        print(requests.patch(url, headers=headers, data=data))
        print(response.text)