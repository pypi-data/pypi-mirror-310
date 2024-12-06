# function.py

import pulumi
import pulumi_aws as aws
from cloud_foundry.utils.logger import logger

log = logger(__name__)


class Function(pulumi.ComponentResource):
    lambda_: aws.lambda_.Function

    def __init__(
        self,
        name,
        *,
        archive_location: str = None,
        hash: str = None,
        runtime: str = None,
        handler: str = None,
        timeout: int = None,
        memory_size: int = None,
        environment: dict[str, str] = None,
        policy_statements: list = [],
        vpc_config: dict = None,
        opts=None,
    ):
        super().__init__("cloud_forge:lambda:Function", name, {}, opts)
        self.name = name
        self.archive_location = archive_location
        self.hash = hash
        self.runtime = runtime
        self.handler = handler
        self.environment = environment or {}
        self.memory_size = memory_size
        self.timeout = timeout
        self.policy_statements = policy_statements
        self.vpc_config = vpc_config or {}
        self._function_name = f"{pulumi.get_project()}-{pulumi.get_stack()}-{self.name}"

        # Check if we should import an existing Lambda function
        if not archive_location and not hash and not runtime and not handler:
            log.info(f"Importing existing Lambda function: {self._function_name}")
            self.lambda_ = aws.lambda_.Function.get(
                f"{self.name}-lambda",
                self.name,
                opts=pulumi.ResourceOptions(parent=self),
            )
        else:
            self._create_lambda_function()

    @property
    def invoke_arn(self) -> pulumi.Output[str]:
        return self.lambda_.invoke_arn

    @property
    def function_name(self) -> pulumi.Output[str]:
        return self.lambda_.name

    def _create_lambda_function(self) -> aws.lambda_.Function:
        log.debug("Creating lambda function")

        execution_role = self.create_execution_role()

        # Define VPC configuration if provided
        vpc_config_args = None
        if self.vpc_config:
            vpc_config_args = aws.lambda_.FunctionVpcConfigArgs(
                subnet_ids=self.vpc_config.get("subnet_ids", []),
                security_group_ids=self.vpc_config.get("security_group_ids", []),
            )

        self.lambda_ = aws.lambda_.Function(
            f"{self.name}-function",
            code=pulumi.FileArchive(self.archive_location),
            name=self._function_name,
            role=execution_role.arn,
            memory_size=self.memory_size,
            timeout=self.timeout,
            handler=self.handler or "app.handler",
            source_code_hash=self.hash,
            runtime=self.runtime or aws.lambda_.Runtime.PYTHON3D9,
            environment=aws.lambda_.FunctionEnvironmentArgs(variables=self.environment),
            vpc_config=vpc_config_args,  # Pass VPC config to Lambda
            opts=pulumi.ResourceOptions(depends_on=[execution_role], parent=self),
        )
        pulumi.export(f"{self.name}-invoke-arn", self.lambda_.invoke_arn)
        pulumi.export(f"{self.name}-name", self._function_name)
        self.register_outputs(
            {
                "invoke-arn": self.lambda_.invoke_arn,
                "function_name": self._function_name,
            }
        )

    def create_execution_role(self) -> aws.iam.Role:
        log.debug("Creating execution role")
        assume_role_policy = aws.iam.get_policy_document(
            statements=[
                aws.iam.GetPolicyDocumentStatementArgs(
                    effect="Allow",
                    principals=[
                        aws.iam.GetPolicyDocumentStatementPrincipalArgs(
                            type="Service",
                            identifiers=["lambda.amazonaws.com"],
                        )
                    ],
                    actions=["sts:AssumeRole"],
                )
            ]
        )

        log.info(f"Assume role policy: {assume_role_policy}")
        role = aws.iam.Role(
            f"{self.name}-role",
            assume_role_policy=assume_role_policy.json,
            name=f"{pulumi.get_project()}-{pulumi.get_stack()}-{self.name}-lambda",
            opts=pulumi.ResourceOptions(parent=self),
        )

        policy_statements = self.policy_statements
        if self.vpc_config:
            policy_statements.append(
                aws.iam.GetPolicyDocumentStatementArgs(
                    effect="Allow",
                    actions=[
                        "ec2:CreateNetworkInterface",
                        "ec2:DescribeNetworkInterfaces",
                        "ec2:DeleteNetworkInterface",
                        "ec2:AssignPrivateIpAddresses",
                        "ec2:UnassignPrivateIpAddresses",
                    ],
                    resources="*",
                )
            )
            policy_statements.append(
                aws.iam.GetPolicyDocumentStatementArgs(
                    effect="Allow",
                    actions=[
                        "ec2:DescribeSubnets",
                        "ec2:DescribeSecurityGroups",
                        "ec2:DescribeVpcEndpoints",
                    ],
                    resources="*",
                )
            )

        policy_document = aws.iam.get_policy_document(
            statements=[
                *policy_statements,
                aws.iam.GetPolicyDocumentStatementArgs(
                    effect="Allow",
                    actions=[
                        "logs:CreateLogGroup",
                        "logs:CreateLogStream",
                        "logs:PutLogEvents",
                    ],
                    resources=["*"],
                ),
            ]
        )

        log.info(f"Policy document: {policy_document.json}")
        aws.iam.RolePolicy(
            f"{self.name}-role-policy",
            role=role.id,
            policy=policy_document.json,
            opts=pulumi.ResourceOptions(depends_on=[role], parent=self),
        )

        return role


def import_function(name: str) -> Function:
    return Function(name)


def function(
    name,
    *,
    archive_location: str = None,
    hash: str = None,
    runtime: str = None,
    handler: str = None,
    timeout: int = None,
    memory_size: int = None,
    environment: dict[str, str] = None,
    actions: list[str] = None,
    vpc_config: dict = None,  # New argument for VPC configuration
    opts=None,
) -> Function:
    return Function(
        name,
        archive_location=archive_location,
        hash=hash,
        runtime=runtime,
        handler=handler,
        timeout=timeout,
        memory_size=memory_size,
        environment=environment,
        actions=actions,
        vpc_config=vpc_config,
        opts=opts,
    )
