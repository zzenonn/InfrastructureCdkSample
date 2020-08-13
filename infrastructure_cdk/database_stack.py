from aws_cdk import core
import aws_cdk.aws_ec2 as ec2
import aws_cdk.aws_rds as rds


class DatabaseStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, 
                vpc, 
                backend_security_groups, 
                storage             = 100, 
                storage_type        = rds.StorageType.GP2,
                ec2_type            = "t3.micro", 
                multi_az            = False, 
                deletion_protection = False,
                backup_retention    = 7,
                **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        db = rds.DatabaseInstance(self, "Database",
                                             engine=rds.DatabaseInstanceEngine.POSTGRES,
                                             instance_type=ec2.InstanceType(instance_type_identifier=ec2_type),
                                             master_username="dba",
                                             vpc=vpc,
                                             multi_az=multi_az,
                                             allocated_storage=storage,
                                             storage_type=storage_type,
                                             cloudwatch_logs_exports=["postgresql", "upgrade"],
                                             deletion_protection=deletion_protection,
                                             backup_retention=core.Duration.days(backup_retention),
                                             removal_policy=core.RemovalPolicy.DESTROY
                                             )
        for asg_sg in backend_security_groups:
            db.connections.allow_default_port_from(asg_sg, "From backend instances to databases")
