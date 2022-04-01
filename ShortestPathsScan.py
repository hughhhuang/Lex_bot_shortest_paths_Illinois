from pprint import pprint
import boto3
from boto3.dynamodb.conditions import Key


def scan_paths(source, dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('ShortestPaths')
    response = table.query(
        KeyConditionExpression=Key('source').eq(source)
    )
    return response['Items']

if __name__ == '__main__':
    paths = scan_paths("Lafayette")
    for path in paths:
        print(path['source'], " -> ", path['destination'], ":", path['distance'])
