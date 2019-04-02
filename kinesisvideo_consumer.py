import boto3
from _datetime import datetime, timedelta

video_client = boto3.client('kinesisvideo', region_name='us-east-1',
                      aws_access_key_id='ACCESS_KEY',
                      aws_secret_access_key='SECRET_KEY',
                      )

response = video_client.get_data_endpoint(
    StreamARN='Stream_ARN',
    APIName='LIST_FRAGMENTS'
)

fragment_list_endpoint = response['DataEndpoint']

session = boto3.session.Session()

client = session.client(
    service_name='kinesis-video-archived-media',
    endpoint_url=fragment_list_endpoint
)

paginator = client.get_paginator('list_fragments')

response = client.list_fragments(
    StreamName='Sample-Stream',
    MaxResults=10,
    FragmentSelector={
        'FragmentSelectorType': 'SERVER_TIMESTAMP',
        'TimestampRange': {
            'StartTimestamp': datetime.utcnow() - timedelta(hours=2),
            'EndTimestamp': datetime.utcnow() + timedelta(hours=2)
        }
    }
)

fragment_numbers = [fragment['FragmentNumber'] for fragment in response['Fragments']]
if len(fragment_numbers) > 0:
    next_token = response['NextToken']

    while next_token is not None:
        response = client.get_media_for_fragment_list(
            StreamName='Sample-Stream',
            Fragments=fragment_numbers
        )
        fragments = response['Payload']
        # do something with fragments

        response = client.list_fragments(
            StreamName='Sample-Stream',
            NextToken=next_token
        )
        fragment_numbers = [fragment['FragmentNumber'] for fragment in response['Fragments']]
        next_token = response['NextToken']
        break
