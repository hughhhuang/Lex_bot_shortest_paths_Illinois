import boto3

def delete_shortest_paths_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.Table('ShortestPaths')
    table.delete()


if __name__ == '__main__':
    delete_shortest_paths_table()
    print("ShortestPaths table deleted.")
