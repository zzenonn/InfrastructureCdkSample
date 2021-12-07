from constructs import Construct
import aws_cdk as cdk

class DatabaseStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, 
                vpc, 
                backend_security_groups, 
                storage             = 100, 
                storage_type        = cdk.aws_rds.StorageType.GP2,
                ec2_type            = "t3.micro", 
                multi_az            = False, 
                deletion_protection = False,
                backup_retention    = 7,
                **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        db_engine = cdk.aws_rds.DatabaseInstanceEngine.postgres(version=cdk.aws_rds.PostgresEngineVersion.VER_13_4)

        db = cdk.aws_rds.DatabaseInstance(self, "Database",
                                             engine=db_engine,
                                             instance_type=cdk.aws_ec2.InstanceType(instance_type_identifier=ec2_type),
                                             credentials=cdk.aws_rds.Credentials.from_username(username="dba"),
                                             vpc=vpc,
                                             multi_az=multi_az,
                                             allocated_storage=storage,
                                             storage_type=storage_type,
                                             cloudwatch_logs_exports=["postgresql", "upgrade"],
                                             deletion_protection=deletion_protection,
                                             backup_retention=cdk.Duration.days(backup_retention),
                                             removal_policy=cdk.RemovalPolicy.DESTROY
                                             )
        for asg_sg in backend_security_groups:
            db.connections.allow_default_port_from(asg_sg, "From backend instances to databases")
