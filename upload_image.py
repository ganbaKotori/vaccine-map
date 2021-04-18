import boto3
from secrets import secret_access_key, access_key
import uuid
BUCKET='lbp-resume-builder'

def uploadImage(directory,imageFileName):
    id = str(uuid.uuid1()) #using UUID to generate a random number to use as the id
    client = boto3.client('s3', aws_access_key_id = access_key, aws_secret_access_key = secret_access_key)
    upload_file_bucket = BUCKET #S3 bucket name
    #file key will be the location where the file is stored in s3
    image_upload_file_key = 'images/' + id + '/' + imageFileName #each location should be unique hence why I use UUID
    #upload image
    client.upload_file(directory + imageFileName, upload_file_bucket, image_upload_file_key)
    print('file uploaded successfully')
    #image download link
    imageDownloadLink = 'https://' + BUCKET + '.s3.amazonaws.com/images/' + id + '/' + imageFileName
    print('image url: ' + imageDownloadLink)
    return imageDownloadLink