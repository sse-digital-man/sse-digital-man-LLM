import sys
sys.path.append(".")

import oss2
from config.api_config import Api_config

def upload(file_path, oss_path):


    api_config = Api_config()

    auth = oss2.Auth(api_config.ali_nls_key_id, api_config.ali_nls_key_secret)
    bucket = oss2.Bucket(auth, api_config.oss_endpoint, api_config.oss_bucket_name)

    # upload file

    bucket.put_object_from_file(oss_path, file_path)

    # get url
    url = bucket.sign_url('GET', oss_path,
                          expires=60,
                          slash_safe=True)

    print("successfully uploaded wav file to oss")

    return url