from constructs import Construct
import aws_cdk as cdk


class NetworkStack(cdk.Stack):

    def __init__(self, scope: Construct, id: str, cidr="10.10.0.0/16", subnet_mask=24, nat_gatways=1, db_port=5432, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # So far, the VPC construct only supports FLSM 
        # see https://github.com/aws/aws-cdk/issues/3931

        self.vpc = cdk.aws_ec2.Vpc(self, "VPC",
                           max_azs              = 6,
                           cidr                 = cidr,
                           subnet_configuration = [cdk.aws_ec2.SubnetConfiguration(
                               subnet_type      = cdk.aws_ec2.SubnetType.PUBLIC,
                               name             = "Public",
                               cidr_mask        = subnet_mask
                           ), 
                            cdk.aws_ec2.SubnetConfiguration(
                               subnet_type      = cdk.aws_ec2.SubnetType.PRIVATE_WITH_NAT,
                               name             = "Private",
                               cidr_mask        = subnet_mask
                           ), 
                            cdk.aws_ec2.SubnetConfiguration(
                               subnet_type      = cdk.aws_ec2.SubnetType.PRIVATE_ISOLATED,
                               name             = "DB",
                               cidr_mask        = subnet_mask
                           )
                           ],
                           nat_gateways=nat_gatways
                           )
                           
        
        private_subnets = self.vpc.private_subnets
        isolated_subnets = self.vpc.isolated_subnets
        
        isolated_nacl = cdk.aws_ec2.NetworkAcl(self, "DBNacl", 
                                        vpc              = self.vpc, 
                                        subnet_selection = cdk.aws_ec2.SubnetSelection(subnets=isolated_subnets))

        for id, subnet in enumerate(private_subnets, start=1):
            isolated_nacl.add_entry("DbNACLIngress{}".format(id*100), 
                                        rule_number = id*100,
                                        cidr        = cdk.aws_ec2.AclCidr.ipv4(subnet.node.default_child.cidr_block),
                                        traffic     = cdk.aws_ec2.AclTraffic.tcp_port_range(0,65535), # As per RFC 6056
                                        direction   = cdk.aws_ec2.TrafficDirection.INGRESS,
                                        rule_action = cdk.aws_ec2.Action.ALLOW)
                                    
        for id, subnet in enumerate(private_subnets, start=1):
            isolated_nacl.add_entry("DbNACLEgress{}".format(id*100), 
                                    rule_number = id*100,
                                    cidr        = cdk.aws_ec2.AclCidr.ipv4(subnet.node.default_child.cidr_block),
                                    traffic     = cdk.aws_ec2.AclTraffic.tcp_port_range(1024,65535), # As per RFC 6056
                                    direction   = cdk.aws_ec2.TrafficDirection.EGRESS,
                                    rule_action = cdk.aws_ec2.Action.ALLOW)

        
        
        cdk.CfnOutput(self, "Output",
                       value=self.vpc.vpc_id)
