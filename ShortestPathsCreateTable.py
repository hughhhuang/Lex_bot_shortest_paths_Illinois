import boto3

# aws dynamodb list-tables --endpoint-url http://localhost:8000

def create_shortest_paths_table(dynamodb=None):
    if not dynamodb:
        dynamodb = boto3.resource('dynamodb', endpoint_url="http://localhost:8000")

    table = dynamodb.create_table(
        TableName='ShortestPaths',
        KeySchema=[
            {
                'AttributeName': 'source',
                'KeyType': 'HASH'  # Partition key
            },
            {
                'AttributeName': 'destination',
                'KeyType': 'RANGE'  # Sort key
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'source',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'destination',
                'AttributeType': 'S'
            },

        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 10,
            'WriteCapacityUnits': 10
        }
    )
    return table


if __name__ == '__main__':
    shortest_paths_table = create_shortest_paths_table()
    print("Table status:", shortest_paths_table.table_status)
