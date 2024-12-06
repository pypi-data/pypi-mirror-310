import time
import os
import pandas as pd 
import boto3


# Function to execute an Athena query and get results
def run_athena_query(query, database, output_bucket):
    # Initialize a session using Boto3
    session = boto3.Session()
    athena_client = session.client('athena')

    # Start the query execution
    response = athena_client.start_query_execution(
        QueryString=query,
        QueryExecutionContext={
            'Database': database
        },
        ResultConfiguration={
            'OutputLocation': f's3://{output_bucket}/athena_results/'
        }
    )

    # Get the query execution ID
    query_execution_id = response['QueryExecutionId']

    # Poll for the query execution status
    while True:
        response = athena_client.get_query_execution(QueryExecutionId=query_execution_id)
        status = response['QueryExecution']['Status']['State']

        if status in ['SUCCEEDED', 'FAILED', 'CANCELLED']:
            break
        time.sleep(2)

    # Check if the query succeeded
    if status == 'SUCCEEDED':
        # Get the results
        results = athena_client.get_query_results(QueryExecutionId=query_execution_id)
        output_location = response['QueryExecution']['ResultConfiguration']['OutputLocation']

        return results, response, output_location
    else:
        print(f'FAILED with status: {status}')
        return response, response, None

# Function to delete existing files in the specified S3 path
def download_then_delete_existing_files(bucket, prefix, local_path):
    s3_client = boto3.client('s3')
    response = s3_client.list_objects_v2(Bucket=bucket, Prefix=prefix)
    
    i = 0
    if 'Contents' in response:
        for obj in response['Contents']:
            print(f"File downloaded to {local_path}")
            s3_client.download_file(bucket, obj['Key'], local_path+str(i)+'.parquet')
            
            print(f"Deleting {obj['Key']}")
            s3_client.delete_object(Bucket=bucket, Key=obj['Key'])
            i += 1
    return i

# Function to convert the Athena results to a Pandas DataFrame
def athena_results_to_dataframe(results):
    # Extract column names
    column_info = results['ResultSet']['ResultSetMetadata']['ColumnInfo']
    column_names = [col['Name'] for col in column_info]

    # Extract rows
    rows = results['ResultSet']['Rows'][1:]  # Skip the header row
    data = [[col['VarCharValue'] for col in row['Data']] for row in rows]

    # Create a DataFrame
    df = pd.DataFrame(data, columns=column_names)
    return df

# Function to extract bucket name and key from an S3 path
def parse_s3_path(s3_path):
    path_parts = s3_path.replace("s3://", "").split("/", 1)
    bucket_name = path_parts[0]
    key = path_parts[1]
    return bucket_name, key

def query_and_clean_athena(query, athena_db='draftkings', output_bucket='cardcash-giftcards'):
    """
    This function will run the query and persist the output to an s3 bucket in Parquet,
    then it will copy the output from there to local computer, and then clean up the file
    from s3.

    Note: for now set the default output_bucket to cardcash-giftcards in case I accidentally 
        delete a folder or bucket somehow, then at least it is some unimportant bucket. 
    """
    query_wrapper = f"UNLOAD( {query} ) TO 's3://{output_bucket}/my_own_query_results/' WITH (format = 'parquet')"
    results, response, output_location = run_athena_query(query_wrapper, athena_db, output_bucket)
    _, s3_key = parse_s3_path(output_location)
    local_path = os.path.join(os.getcwd(), 'temp_athena')
    num_files = download_then_delete_existing_files(output_bucket, 'my_own_query_results/', local_path)
    l = []
    for file in os.listdir(os.getcwd()):
        if file.startswith('temp_athena'):
            fqdn = os.path.join(os.getcwd(), file)
            df = pd.read_parquet(fqdn)
            os.remove(fqdn)
            l.append(df)
    return pd.concat(l)