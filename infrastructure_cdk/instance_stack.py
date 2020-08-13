from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_elasticloadbalancingv2 as elb
import aws_cdk.aws_autoscaling as autoscaling
import aws_cdk.aws_iam as iam
import boto3

linux_ami = ec2.AmazonLinuxImage(generation=ec2.AmazonLinuxGeneration.AMAZON_LINUX_2,
                                 edition=ec2.AmazonLinuxEdition.STANDARD,
                                 virtualization=ec2.AmazonLinuxVirt.HVM,
                                 storage=ec2.AmazonLinuxStorage.GENERAL_PURPOSE
                                 )  # Indicate your AMI, no need a specific id in the region
with open("./user_data/user_data.sh") as f:
    user_data = f.read()


class InstanceStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, vpc, use_ssm=True, key_name=None, asg_min=2, asg_max=5, ec2_type="t3.micro", **kwargs) -> None:
        super().__init__(scope, id, **kwargs)
        
        if key_name:
            # Create key-pair Note: Must be done with boto3 since there is no support for this yet in CFN or CDK
            try:
               ec2_resource = boto3.resource('ec2')
               key_pair = ec2_resource.KeyPair(key_name).load()
            except:
               ec2_client = boto3.client('ec2')
               print(ec2_client.create_key_pair(KeyName=key_name)['KeyMaterial'])
        else:
            use_ssm = True

        # Create Bastion that can be connected to only via SSM
        bastion = ec2.BastionHostLinux(self, "Bastion",
                                       vpc=vpc,
                                       subnet_selection=ec2.SubnetSelection(
                                           subnet_type=ec2.SubnetType.PRIVATE),
                                       instance_name="Bastion Host",
                                       instance_type=ec2.InstanceType(instance_type_identifier=ec2_type))
        if not use_ssm:
            bastion.connections.allow_from_any_ipv4(ec2.Port.tcp(22), 
                                                    "Internet access SSH")
            bastion.instance.instance.add_property_override("KeyName", 
                                                            key_name)
                                                            
        ssm_policy = iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=["*"],
            actions=["ssmmessages:*", "ssm:UpdateInstanceInformation", "ec2messages:*"]
        )

        
        # Create ALB
        alb = elb.ApplicationLoadBalancer(self, "ALB",
                                          vpc=vpc,
                                          internet_facing=True,
                                          load_balancer_name="myALB"
                                          )
                                          
        alb.connections.allow_from_any_ipv4(ec2.Port.tcp(80), 
                                            "Internet access ALB 80")
        
        listener = alb.add_listener("Web",
                                    port=80,
                                    open=True)

        # Create Autoscaling Group with fixed 2*EC2 hosts
        self.asg = autoscaling.AutoScalingGroup(self, "Globomantics-Web",
                                                vpc=vpc,
                                                vpc_subnets=ec2.SubnetSelection(subnet_type=ec2.SubnetType.PRIVATE),
                                                instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                                machine_image=linux_ami,
                                                key_name=key_name,
                                                user_data=ec2.UserData.custom(user_data),
                                                desired_capacity=asg_min,
                                                min_capacity=asg_min,
                                                max_capacity=asg_max,
                                                )
        if use_ssm:                                        
            self.asg.add_to_role_policy(ssm_policy)

        self.asg.connections.allow_from(alb, ec2.Port.tcp(80), "ALB access 80 port of EC2 in Autoscaling Group")
        listener.add_targets("addTargetGroup",
                             port=80,
                             targets=[self.asg])

        core.CfnOutput(self, "Output",
                       value=alb.load_balancer_dns_name)
