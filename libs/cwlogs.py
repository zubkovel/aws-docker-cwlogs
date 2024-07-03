import boto3
import logging
import boto3
import botocore
import json
import time
from datetime import datetime


log = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


class CloudWatchLogs(object):

    def __init__(self, region, aws_access_key_id=None, aws_secret_access_key=None):
        self.cwlogs = boto3.client(
            "logs",
            region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
        )

    def create_log_group(self, name):
        try:
            self.cwlogs.create_log_group(logGroupName=name)
            log.info("LogGroup created, log_group=%s" % name)
        except botocore.exceptions.ClientError as ex:
            if ex.response["Error"]["Code"] != "ResourceAlreadyExistsException":
                log.error("Unable to create LogGroup, log_group=%s" % name)
                raise ex
            else:
                log.info("LogGroup exists, log_group=%s" % name)

    def create_log_stream(self, group_name, stream_name):
        try:
            self.cwlogs.create_log_stream(
                logGroupName=group_name, logStreamName=stream_name
            )
            log.info(
                f"LogStream created, log_stream=%s log_group=%s"
                % (stream_name, group_name)
            )
        except botocore.exceptions.ClientError as ex:
            if ex.response["Error"]["Code"] != "ResourceAlreadyExistsException":
                log.error(
                    "Unable to create LogStream, log_stream=%s log_group=%s"
                    % stream_name,
                    group_name,
                )
                raise ex
            else:
                log.info(
                    "LogGroup exists, log_stream=%s log_group=%s"
                    % (stream_name, group_name)
                )

    def send_log_event(self, group_name, stream_name, msg, level="INFO"):

        structured_log = {
            "log_level": level,
            "message": msg,
        }
        serialised_msg = json.dumps(structured_log)

        try:
            resp = self.cwlogs.put_log_events(
                logGroupName=group_name,
                logStreamName=stream_name,
                logEvents=[
                    {
                        "timestamp": int(time.time() * 1000),  # milliseconds
                        "message": serialised_msg,
                    },
                ],
            )
            log.info("LogEvent sent successfully LogEvent=%s" % serialised_msg)

        except Exception as ex:
            log.error("Unable to send LogEvent= %s" % serialised_msg)
            raise ex
