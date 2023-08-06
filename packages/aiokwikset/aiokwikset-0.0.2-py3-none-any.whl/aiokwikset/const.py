"""Constants used by RinnaiWaterHeater"""

import logging

LOGGER = logging.getLogger('aiorinnai')

POOL_ID = 'cognito-idp.us-east-1.amazonaws.com/us-east-1_6B3uo6uKN'
CLIENT_ID = '5eu1cdkjp1itd1fi7b91m6g79s'
POOL_REGION = 'us-east-1'

GET_USER_URL = 'https://ynk95r1v52.execute-api.us-east-1.amazonaws.com/prod_v1/users/me'
GET_HOMES_URL = 'https://ynk95r1v52.execute-api.us-east-1.amazonaws.com/prod_v1/users/me/homes?top=200'
GET_HOME_DEVICES_URL = 'https://ynk95r1v52.execute-api.us-east-1.amazonaws.com/prod_v1/homes/%s/devices'
GET_DEVICE_URL = 'https://ynk95r1v52.execute-api.us-east-1.amazonaws.com/prod_v1/devices_v2/%s'

COMMAND_URL = 'https://ynk95r1v52.execute-api.us-east-1.amazonaws.com/prod_v1/devices/%s/status'

USER_AGENT = 'okhttp/4.8.1'
ACCEPT_ENCODING = 'gzip'
CONTENT_TYPE = 'application/json'