import boto3
import datetime
import time

# AWS credentials and region
aws_access_key = 'YOUR_AWS_ACCESS_KEY'
aws_secret_key = 'YOUR_AWS_SECRET_KEY'
aws_region = 'YOUR_REGION'

# EC2 instance settings
instance_type = 't2.micro'  # You can change this to your desired instance type
ami_id = 'YOUR_AMI_ID'  # Replace with the desired AMI ID
instance_name = 'MyEC2Instance'
security_group_ids = ['YOUR_SECURITY_GROUP_ID']  # Replace with your security group IDs
subnet_id = 'YOUR_SUBNET_ID'  # Replace with your subnet ID
key_pair_name = 'YOUR_KEY_PAIR_NAME'  # Replace with your key pair name
weekday_to_run = [0, 2, 4, 6]  # 0=Monday, 2=Wednesday, 4=Friday, 6=Sunday
start_time = '09:00'
end_time = '11:30'


def create_ec2_instance():
    ec2 = boto3.resource('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key,
                         region_name=aws_region)

    # Create EC2 instance
    instance = ec2.create_instances(
        ImageId=ami_id,
        InstanceType=instance_type,
        MinCount=1,
        MaxCount=1,
        SecurityGroupIds=security_group_ids,
        SubnetId=subnet_id,
        KeyName=key_pair_name,
        InstanceInitiatedShutdownBehavior='stop',  # Stop the instance when it's terminated
        TagSpecifications=[{
            'ResourceType': 'instance',
            'Tags': [{'Key': 'Name', 'Value': instance_name}]
        }]
    )[0]

    instance.wait_until_running()
    print(f'EC2 instance {instance.id} created with public IP: {instance.public_ip_address}')


def start_ec2_instance(instance_id):
    ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key,
                       region_name=aws_region)
    ec2.start_instances(InstanceIds=[instance_id])
    print(f'EC2 instance {instance_id} started')


def stop_ec2_instance(instance_id):
    ec2 = boto3.client('ec2', aws_access_key_id=aws_access_key, aws_secret_access_key=aws_secret_key,
                       region_name=aws_region)
    ec2.stop_instances(InstanceIds=[instance_id])
    print(f'EC2 instance {instance_id} stopped')


def is_weekday_to_run():
    today = datetime.datetime.now()
    return today.weekday() in weekday_to_run


def is_time_to_run():
    now = datetime.datetime.now().time()
    start = datetime.datetime.strptime(start_time, '%H:%M').time()
    end = datetime.datetime.strptime(end_time, '%H:%M').time()
    return start <= now <= end


if __name__ == '__main__':
    create_ec2_instance()
    while True:
        if is_weekday_to_run() and is_time_to_run():
            start_ec2_instance(instance_id='YOUR_INSTANCE_ID')  # Replace with your instance ID
        else:
            stop_ec2_instance(instance_id='YOUR_INSTANCE_ID')  # Replace with your instance ID
        time.sleep(3600)  # Check the conditions every hour
