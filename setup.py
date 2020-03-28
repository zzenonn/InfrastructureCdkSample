import setuptools


with open("README.md") as fp:
    long_description = fp.read()


setuptools.setup(
    name="InfrastructureCdkSample",
    version="1.0.0",

    description="Create new VPC, network ACL, AutoscalingGroup behind a load balancer, RDS instance, bastion host, as well as (almost) proper NACL configuration",
    long_description=long_description,
    long_description_content_type="text/markdown",

    author="Miguel Zenon Nicanor Lerias Saavedra (Zenon)",

    package_dir={"": "infrastructure_cdk"},
    packages=setuptools.find_packages(where="infrastructure_cdk"),

    install_requires=[
        "aws-cdk.core",
        "aws-cdk.aws-ec2",
        "aws-cdk.aws-elasticloadbalancingv2",
        "aws-cdk.aws-autoscaling",
        "aws-cdk.aws-rds",
        "boto3"
    ],

    python_requires=">=3.6",

    classifiers=[
        "Development Status :: 4 - Beta",

        "Intended Audience :: Developers",

        "License :: OSI Approved :: MIT License",

        "Programming Language :: JavaScript",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",

        "Topic :: Software Development :: Code Generators",
        "Topic :: Utilities",

        "Typing :: Typed",
    ],
)
