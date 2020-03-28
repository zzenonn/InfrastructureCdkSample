
# Sample of Infrastructure in Cloud Development Kit

This project creates a VPC with associated NACLs, Instances (including a bastion host), and RDS. 
Attempts have been made parameterize both stacks as much as possible for use in
dev or production environments.

Make sure you properly configure your python virtualenv.

```
$ python3 -m venv .env
$ pip install -r requirements.txt
$ source .env/bin/activate
```



## Network

You have the option to input your own CIDR block and prefix length. 
The network ACLs are configured to block non-ephemeral ports outbound. Ideally,
it should also only allow the DB port inbound, but that functionality is still
not supported on CDK (see code comments for details).

## Instances

The instances stack allows you to choose whether you prefer SSM (default) or SSH.
If you choose SSH, you can specify a key with the `key_name` parameter. If the key
exists, it will select the key. If no such key exists, it will create one for you
and print out the private key.

## Database

You can customize the following parameters by passing it to the constructor.

```
storage             
storage_type        
ec2_type             
multi_az             
deletion_protection 
backup_retention    
```
Default values are provided and assumes a development environment.
## Useful commands

 * `cdk ls`          list all stacks in the app
 * `cdk synth`       emits the synthesized CloudFormation template
 * `cdk deploy`      deploy this stack to your default AWS account/region
 * `cdk diff`        compare deployed stack with current state
 * `cdk docs`        open CDK documentation

