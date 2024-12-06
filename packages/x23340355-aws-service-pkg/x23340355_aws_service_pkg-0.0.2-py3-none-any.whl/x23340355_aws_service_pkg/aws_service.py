import boto3
import requests
import logging
import json

#Class for AWS Services interractions
class AWSService:
    
    #Initialize AWS services with boto3
    def __init__(self, api_gateway_url, notify_function_name):
        self.s3_client = boto3.client('s3')
        self.lambda_client = boto3.client('lambda')
        self.api_gateway_url = api_gateway_url
        self.notify_function_name = notify_function_name

    #AWS S3 - Uploads a file object to an S3 bucket and returns the object key
    def upload_image_to_s3(self, file, bucket_name, file_name):
        try:
            self.s3_client.upload_fileobj(file, bucket_name, file_name)
            logging.info(f"File uploaded to S3 bucket '{bucket_name}' with key '{file_name}'")
            return file_name 
        except self.s3_client.exceptions.NoSuchBucket as e:
            logging.error(f"Bucket does not exist: {bucket_name}. Error: {e}")
            return None
        except Exception as e:
            logging.error(f"Error uploading file to S3: {e}")
            return None

    #To get pre-signed URL for a private S3 object, that will display property images on website
    def get_presigned_url(self, bucket_name, file_name, expiration=3600):
        try:
            url = self.s3_client.generate_presigned_url(
                'get_object',
                Params={'Bucket': bucket_name, 'Key': file_name},
                ExpiresIn=expiration
            )
            logging.info(f"Generated presigned URL for file '{file_name}' in bucket '{bucket_name}'")
            return url
        except Exception as e:
            logging.error(f"Error generating presigned URL for {file_name}: {e}")
            return None
    
    #For image delete function from S3 bucket
    def delete_image_from_s3(self, bucket_name, file_name):
        try:
            self.s3_client.delete_object(Bucket=bucket_name, Key=file_name)
            logging.info(f"Successfully deleted file '{file_name}' from bucket '{bucket_name}'")
            return True
        except self.s3_client.exceptions.NoSuchKey:
            logging.error(f"File '{file_name}' does not exist in bucket '{bucket_name}'.")
            return False
        except Exception as e:
            logging.error(f"Error deleting file '{file_name}' from S3: {e}")
            return False

    # Email-sending method via API Gateway and will trigger Lambda to send email
    def send_email_via_lambda(self, to_email, subject, body):
        payload = {
            'to_email': to_email,
            'subject': subject,
            'body': body
        }
        headers = {'Content-Type': 'application/json'}

        try:
            logging.info(f"Sending email to {to_email} with subject '{subject}'")
            response = requests.post(self.api_gateway_url, json=payload, headers=headers)

            logging.info(f"API Gateway Response Status Code: {response.status_code}")
            logging.info(f"API Gateway Response Text: {response.text}")

            #This is to parse the response as JSON
            try:
                response_data = response.json()
            except json.JSONDecodeError:
                logging.error("Failed to parse JSON response from API Gateway")
                return "Error: Failed to parse response from email service"

            #Check function whether the response was successful or not
            if response.status_code == 200:
                return response_data.get('body', 'Email sent successfully')
            else:
                logging.error(f"Failed to send email: {response.status_code} - {response.text}")
                return f"Failed to send email: {response.status_code} - {response_data.get('body', response.text)}"
        except requests.exceptions.RequestException as e:
            logging.error(f"Request error sending email: {e}")
            return f"Request error sending email: {e}"
        except Exception as e:
            logging.error(f"Error sending email: {e}")
            return f"Error sending email: {e}"

    #Notify Admin for new property creation via AWS Lambda
    def notify_admin(self, property_details):
        if not self.notify_function_name:
            raise ValueError("Lambda function name for notify_admin is not set.")
        
        payload = {
            'property_title': property_details['property_title'],
            'property_description': property_details['property_description'],
            'property_contact_email': property_details['property_contact_email']
        }
        try:
            logging.info(f"Sending property notification to admin: {payload}")
            response = self.lambda_client.invoke(
                FunctionName=self.notify_function_name, 
                InvocationType='RequestResponse',
                Payload=json.dumps(payload)
            )
            response_payload = json.load(response['Payload'])
            logging.info(f"Lambda response: {response_payload}")
            return response_payload
        except Exception as e:
            logging.error(f"Error invoking Lambda function for admin notification: {e}")
            raise
