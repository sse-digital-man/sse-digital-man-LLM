import sys
sys.path.append('.')

import oss2
from config.api_config import Api_config

OBJECT_NAME = 'voice_input/voice_input.wav'

api_config = Api_config()

auth = oss2.Auth(api_config.ali_nls_key_id, api_config.ali_nls_key_secret)
bucket = oss2.Bucket(auth, api_config.oss_endpoint, api_config.oss_bucket_name)

# upload file

bucket.put_object_from_file(OBJECT_NAME, './test/voice_input/test_audio_recorder.wav')

# get url
url = bucket.sign_url('GET', OBJECT_NAME,
                      expires = 60,
                      slash_safe= True)

print(url)