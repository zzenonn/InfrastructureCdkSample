from aws_cdk import core
import aws_cdk.aws_ec2 as ec2


class NetworkStack(core.Stack):

    def __init__(self, scope: core.Construct, id: str, cidr="10.10.0.0/16", subnet_mask=24, nat_gatways=1, db_port=5432, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # The code that defines your stack goes here

        self.vpc = ec2.Vpc(self, "VPC",
                           max_azs              = 6,
                           cidr                 = cidr,
                           subnet_configuration = [ec2.SubnetConfiguration(
                               subnet_type      = ec2.SubnetType.PUBLIC,
                               name             = "Public",
                               cidr_mask        = subnet_mask
                           ), 
                            ec2.SubnetConfiguration(
                               subnet_type      = ec2.SubnetType.PRIVATE,
                               name             = "Private",
                               cidr_mask        = subnet_mask
                           ), 
                            ec2.SubnetConfiguration(
                               subnet_type      = ec2.SubnetType.ISOLATED,
                               name             = "DB",
                               cidr_mask        = subnet_mask
                           )
                           ],
                           nat_gateways=nat_gatways
                           )
                           
                           
        
        
        private_subnets = self.vpc.private_subnets
        isolated_subnets = self.vpc.isolated_subnets
        
        isolated_nacl = ec2.NetworkAcl(self, "DBNacl", 
                                        vpc              = self.vpc, 
                                        subnet_selection = ec2.SubnetSelection(subnets=isolated_subnets))
        
        # Note: Ideally, especially if we're talking about DB subnets, NACL rules 
        # be added to allow traffic only from private to Isolated. This will not
        # be implemented until https://github.com/aws/aws-cdk/issues/3931
        # is closed.
        
        # for id, subnet in enumerate(isolated_subnets):
        #     isolated_nacl.add_entry("DbNACLIngress{}".format(id*100), 
        #                             <private_Cidr>, 
        #                             ec2.AclTraffic.tcp_port(3306), 
        #                             ec2.TrafficDirection.INGRESS,
        #                             ec2.Action.ALLOW)
        
        isolated_nacl.add_entry("DbNACLIngressAll", 
                                    rule_number = 100,
                                    cidr        = ec2.AclCidr.any_ipv4(),
                                    traffic     = ec2.AclTraffic.tcp_port_range(0,65535), # As per RFC 6056
                                    direction   = ec2.TrafficDirection.INGRESS,
                                    rule_action = ec2.Action.ALLOW)
        
        for id, subnet in enumerate(isolated_subnets, start=1):
            isolated_nacl.add_entry("DbNACLEgress{}".format(id*100), 
                                    rule_number = id*100,
                                    cidr        = ec2.AclCidr.any_ipv4(),
                                    traffic     = ec2.AclTraffic.tcp_port_range(1024,65535), # As per RFC 6056
                                    direction   = ec2.TrafficDirection.EGRESS,
                                    rule_action = ec2.Action.ALLOW)

        
        
        core.CfnOutput(self, "Output",
                       value=self.vpc.vpc_id)
