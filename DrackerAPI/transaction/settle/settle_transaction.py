import boto3

def lambda_handler(event, context):
    transaction_id = event['transaction_id']
    payer_uid = event['payer_uid']
    payee_uid = event['payee_uid']
    time = event['time']
    #Get client and tables
    client = boto3.resource('dynamodb')
    payee_table = client.Table(payee_uid)
    payer_table = client.Table(payer_uid)
    #Update payee table
    response = payee_table.get_item(
        Key={
            'transaction_id' : transaction_id
        }
    )
    item = response['Item']
    #update time
    item['settelement_time'] = time
    #remove unnecessary info
    item.pop('notification_identifier', None)
    item.pop('tagged_image', None)
    item.pop('time', None)
    payee_table.put_item(Item=item)
    #Update payer table
    response = payer_table.get_item(
        Key={
            'transaction_id' : transaction_id
        }
    )
    item = response['Item']
    #update time
    item['settelement_time'] = time
    #remove unnecessary info
    item.pop('notification_identifier', None)
    item.pop('tagged_image', None)
    item.pop('time', None)
    payer_table.put_item(Item=item)
    return 200