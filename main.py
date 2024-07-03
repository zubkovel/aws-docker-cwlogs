import click
import logging
import docker

from libs.cwlogs import CloudWatchLogs

log = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)


def _get_cwlogs(
    aws_cloudwatch_group,
    aws_cloudwatch_stream,
    aws_access_key_id,
    aws_secret_access_key,
    aws_region,
):
    cwlogs = CloudWatchLogs(
        region=aws_region,
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
    )

    cwlogs.create_log_group(aws_cloudwatch_group)
    cwlogs.create_log_stream(aws_cloudwatch_group, aws_cloudwatch_stream)

    return cwlogs


@click.command()
@click.option("--docker-image", help="A name of a Docker image.")
@click.option("--bash-command", help="A bash command (to run inside the Docker image).")
@click.option("--aws-cloudwatch-group", help="A name of an AWS CloudWatch group.")
@click.option("--aws-cloudwatch-stream", help="A name of an AWS CloudWatch stream.")
@click.option("--aws-access-key-id", help="AWS access key id.")
@click.option("--aws-secret-access-key", help="AWS secret access key.")
@click.option("--aws-region", help="A name of an AWS region.")
def _main(
    docker_image,
    bash_command,
    aws_cloudwatch_group,
    aws_cloudwatch_stream,
    aws_access_key_id,
    aws_secret_access_key,
    aws_region,
):
    # print(docker_image, bash_command, aws_cloudwatch_group, aws_cloudwatch_stream, aws_access_key_id, aws_secret_access_key, aws_region)
    client = docker.from_env()

    container = client.containers.run(docker_image, bash_command, detach=True)
    streamer = container.logs(stream=True)

    cwlogs = _get_cwlogs(
        aws_cloudwatch_group,
        aws_cloudwatch_stream,
        aws_access_key_id,
        aws_secret_access_key,
        aws_region,
    )

    for msg in streamer:

        cwlogs.send_log_event(aws_cloudwatch_group, aws_cloudwatch_stream, str(msg))


if __name__ == "__main__":
    _main()
