import sys
sys.path.append(".")

import oss2
from config.ConfigLoader import config


def upload(file_path, oss_path):
    auth = oss2.Auth(config.ali_nls_key_id, config.ali_nls_key_secret)
    bucket = oss2.Bucket(auth, config.oss_endpoint, config.oss_bucket_name)

    # upload file

    bucket.put_object_from_file(oss_path, file_path)

    # get url
    url = bucket.sign_url('GET', oss_path,
                          expires=60,
                          slash_safe=True)

    print("successfully uploaded wav file to oss")

    return url