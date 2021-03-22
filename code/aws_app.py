import boto3
import uuid

client = boto3.resource(
    's3',
    aws_access_key_id='AKIA44KNG4E7HWKSP4UV',
    aws_secret_access_key='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',
)

# Create Bucket - Aim of this function is to create s3 bucket.


def create_bucket(bucket_prefix, s3_connection):
    bucket_name = bucket_prefix
    bucket_response = s3_connection.create_bucket(
        Bucket=bucket_name,
        CreateBucketConfiguration={
            'LocationConstraint': 'eu-west-2'})

    return bucket_name, bucket_response

# Create Model - Aim of this function is to create the model that would accept users input for reminder.


def create_note():
    print('enter your reminder below:\n')
    reminder = input()

    return reminder

# Upload File and Create Temp File Functions - Aim of these functions is to upload file containing all data and store also as temp.


def upload_file(bucket_name, file_name):

    client.Object(bucket_name, file_name).upload_file(Filename=file_name)


def create_temp_file(file_name):
    file_content = create_note()

    with open(file_name, 'w') as f:
        f.write(str(file_content))
    return file_name

# Upload Reminder  - Aim of this function is to upload reminders.


def upload_reminder():
    tmp_file = create_temp_file("test3")

    upload_file("firstpybucket", tmp_file)

# Delete Reminders - Aim of this function is to remove existing reminders.


def delete_reminder(from_bucket, file_name):
    client.Object(from_bucket, file_name).delete()

# Delete All Reminders - Aim of this function is to remove existing reminder notifications.


def delete_all_reminders(from_bucket):
    for obj in client.Bucket(from_bucket).objects.all():
        client.Object(from_bucket, obj.key).delete()

# Display All Reminders - Aim of this function is to prompt user regarding upcoming reminders.


def display_all_reminders(from_bucket):
    for obj in client.Bucket(from_bucket).objects.all():
        print(obj.key)
