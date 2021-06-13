from chalice import Chalice, Response, Rate, NotFoundError
from boto3.dynamodb.conditions import Key
import boto3
import string
import random

app = Chalice(app_name='url-shortener')
# app.debug = True

def get_dynamo_db_table():
    """
    Get the configured dynamodb db table.
    """
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table('url-shortener-table')
    return table


def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    """
    Generate a random ID of length 6.
    """
    return ''.join(random.choice(chars) for _ in range(size))


def get_base_url(current_request):
    """
    Get the base URL of the current request.
    """
    headers = current_request.headers
    return f"{headers['host']}/{current_request.context['stage']}"


def truncate_table(table):
    """
    Truncate the dynamodb table table.
    Source: https://stackoverflow.com/a/61641725
    """   
    #get the table keys
    tableKeyNames = [key.get("AttributeName") for key in table.key_schema]
    #Only retrieve the keys for each item in the table (minimize data transfer)
    ProjectionExpression = ", ".join(tableKeyNames)
    
    response = table.scan(ProjectionExpression=ProjectionExpression)
    data = response.get('Items')
    
    while 'LastEvaluatedKey' in response:
        response = table.scan(
            ProjectionExpression=ProjectionExpression, 
            ExclusiveStartKey=response['LastEvaluatedKey'])
        data.extend(response['Items'])

    with table.batch_writer() as batch:
        for each in data:
            batch.delete_item(
                Key={key: each[key] for key in tableKeyNames}
            )


@app.route('/')
def index():
    return {'message': 'This is a simple api shortener API using AWS Chalice python serverless framework.'}

@app.route('/shorten-me', methods=['POST'])
def generate_shortened_url():
    data = app.current_request.json_body
    try:
        id = id_generator()
        get_dynamo_db_table().put_item(Item={
            'id': id,
            'originalurl': data['original-url']
        })
        base_url = get_base_url(app.current_request)
        short_url = 'https://'+base_url+'/'+id
        return {'short url': short_url}
    except Exception as e:
        return Response(body=str(e),
                    headers={'Content-Type': 'text/plain'},
                    status_code=500)
        

@app.route('/{id}', methods=['GET'])
def redirect(id):
    try:
        response = get_dynamo_db_table().query(
            KeyConditionExpression=Key("id").eq(id)
        )
        data = response.get('Items', None)
    except Exception as e:
        raise NotFoundError(id)    
    redirect_url = data[0]['originalurl']
    return Response(status_code=301,
                    headers={'Location': redirect_url},
                    body='')

@app.schedule(Rate(24, unit=Rate.HOURS))
def periodic_db_clean_up(event):
    '''
    Automatically clean up the dynamo db table every 24 Hours.
    '''
    table = get_dynamo_db_table()
    truncate_table(table)
    print('url-shortener db cleaned up.')
    return {"message": "url-shortener table cleaned up."}        