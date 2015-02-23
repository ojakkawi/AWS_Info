#!/bin/bash
#
# A simple script to pull information from AWS. Is reliant on the AWS CLI 
#  tools.


# Store the AWS access ID and key. We may wish to move this information into 
#  a separate file for security purposes in future versions
#
# THIS INFORMATION SHOULD ALWAYS REMAIN SECRET. DO NOT MAKE THIS FILE READABLE
#  BY ANYBODY WHO SHOULD NOT HAVE ACCESS TO THIS AWS ACCOUNT.
#

export AWS_ACCESS_KEY_ID=

export AWS_SECRET_ACCESS_KEY=

#
#
#

AWS_EXEC=/usr/local/bin/aws

AWS_REGION="us-east-1"


if [ $1 == "EC2" ]; then
    $AWS_EXEC --region $AWS_REGION --output json ec2 describe-instances
elif [ $1 == "RDS" ]; then
    $AWS_EXEC --region $AWS_REGION --output json rds describe-db-instances
elif [ $1 == "ELB" ]; then
    $AWS_EXEC --region $AWS_REGION --output json elb describe-load-balancers
elif [ $1 == "ECache" ]; then
    $AWS_EXEC --region $AWS_REGION --output json elasticache describe-cache-clusters --show-cache-node-info
elif [ $1 == "CF" ]; then
    $AWS_EXEC --region $AWS_REGION --output json cloudformation describe-stacks
fi