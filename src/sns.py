import requests
import json
import boto3

AWSAccessKeyId="AKIAY2SPKZA2MGVRNXHM"
AWSSecretKey="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"

class NotificationMiddlewareHandler:
    sns_client = None

    def __init__(self):
        pass

    @classmethod
    def get_sns_client(cls):

        if NotificationMiddlewareHandler.sns_client is None:
            NotificationMiddlewareHandler.sns_client = sns = boto3.client("sns",
                                                                          aws_access_key_id=AWSAccessKeyId,
                                                                          aws_secret_access_key=AWSSecretKey,
                                                                          region_name = "us-east-1"
                                                                          )
        return NotificationMiddlewareHandler.sns_client

    @classmethod
    def get_sns_topics(cls):
        s_client = NotificationMiddlewareHandler.get_sns_client()
        result = response = s_client.list_topics()
        topics = result["Topics"]
        return topics

    @classmethod
    def send_sns_message(cls, sns_topic, message):
        import json
        import boto3

        s_client = NotificationMiddlewareHandler.get_sns_client()
        response = s_client.publish(
            TargetArn=sns_topic,
            Message=json.dumps({'default': json.dumps(message)}),
            MessageStructure='json'
        )
        print("Publish response = ", json.dumps(response, indent=2))
