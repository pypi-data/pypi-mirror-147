'''
# integ-tests

<!--BEGIN STABILITY BANNER-->---


![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

> The APIs of higher level constructs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

---
<!--END STABILITY BANNER-->

## Usage

Suppose you have a simple stack, that only encapsulates a Lambda function with a
certain handler:

```python
class StackUnderTest(Stack):
    def __init__(self, scope, id, *, functionProps=None, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, functionProps=functionProps, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        lambda_.Function(self, "Handler",
            runtime=lambda_.Runtime.NODEJS_12_X,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
            (SpreadAssignment ...props.functionProps
              function_props)
        )
```

You may want to test this stack under different conditions. For example, we want
this stack to be deployed correctly, regardless of the architecture we choose
for the Lambda function. In particular, it should work for both `ARM_64` and
`X86_64`. So you can create an `IntegTestCase` that exercises both scenarios:

```python
class StackUnderTest(Stack):
    def __init__(self, scope, id, *, architecture=None, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
        super().__init__(scope, id, architecture=architecture, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)

        lambda_.Function(self, "Handler",
            runtime=lambda_.Runtime.NODEJS_12_X,
            handler="index.handler",
            code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
            architecture=architecture
        )

# Beginning of the test suite
app = App()

stack = Stack(app, "stack")
IntegTestCase(stack, "DifferentArchitectures",
    stacks=[
        StackUnderTest(app, "Stack1",
            architecture=lambda_.Architecture.ARM_64
        ),
        StackUnderTest(app, "Stack2",
            architecture=lambda_.Architecture.X86_64
        )
    ]
)
```

This is all the instruction you need for the integration test runner to know
which stacks to synthesize, deploy and destroy. But you may also need to
customize the behavior of the runner by changing its parameters. For example:

```python
app = App()

stack_under_test = Stack(app, "StackUnderTest")

stack = Stack(app, "stack")

IntegTestCase(stack, "CustomizedDeploymentWorkflow",
    stacks=[stack_under_test],
    diff_assets=True,
    stack_update_workflow=True,
    cdk_command_options=CdkCommands(
        deploy=DeployCommand(
            args=DeployOptions(
                require_approval=RequireApproval.NEVER,
                json=True
            )
        ),
        destroy=DestroyCommand(
            args=DestroyOptions(
                force=True
            )
        )
    )
)
```
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from ._jsii import *

import aws_cdk.cloud_assembly_schema
import aws_cdk.core


class IntegTestCase(
    aws_cdk.core.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="@aws-cdk/integ-tests.IntegTestCase",
):
    '''(experimental) An integration test case.

    Allows the definition of test properties that
    apply to all stacks under this case.

    :stability: experimental
    :exampleMetadata: infused

    Example::

        class StackUnderTest(Stack):
            def __init__(self, scope, id, *, architecture=None, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
                super().__init__(scope, id, architecture=architecture, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
        
                lambda_.Function(self, "Handler",
                    runtime=lambda_.Runtime.NODEJS_12_X,
                    handler="index.handler",
                    code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
                    architecture=architecture
                )
        
        # Beginning of the test suite
        app = App()
        
        stack = Stack(app, "stack")
        IntegTestCase(stack, "DifferentArchitectures",
            stacks=[
                StackUnderTest(app, "Stack1",
                    architecture=lambda_.Architecture.ARM_64
                ),
                StackUnderTest(app, "Stack2",
                    architecture=lambda_.Architecture.X86_64
                )
            ]
        )
    '''

    def __init__(
        self,
        scope: aws_cdk.core.Construct,
        id: builtins.str,
        *,
        stacks: typing.Sequence[aws_cdk.core.Stack],
        allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_command_options: typing.Optional[aws_cdk.cloud_assembly_schema.CdkCommands] = None,
        diff_assets: typing.Optional[builtins.bool] = None,
        hooks: typing.Optional[aws_cdk.cloud_assembly_schema.Hooks] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_update_workflow: typing.Optional[builtins.bool] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param stacks: (experimental) Stacks to be deployed during the test.
        :param allow_destroy: List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test. This list should only include resources that for this specific integration test we are sure will not cause errors or an outage if destroyed. For example, maybe we know that a new resource will be created first before the old resource is destroyed which prevents any outage. e.g. ['AWS::IAM::Role'] Default: - do not allow destruction of any resources on update
        :param cdk_command_options: Additional options to use for each CDK command. Default: - runner default options
        :param diff_assets: Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included. For example any tests involving custom resources or bundling Default: false
        :param hooks: Additional commands to run at predefined points in the test workflow. e.g. { postDeploy: ['yarn', 'test'] } Default: - no hooks
        :param regions: Limit deployment to these regions. Default: - can run in any region
        :param stack_update_workflow: Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow. Default: true

        :stability: experimental
        '''
        props = IntegTestCaseProps(
            stacks=stacks,
            allow_destroy=allow_destroy,
            cdk_command_options=cdk_command_options,
            diff_assets=diff_assets,
            hooks=hooks,
            regions=regions,
            stack_update_workflow=stack_update_workflow,
        )

        jsii.create(self.__class__, self, [scope, id, props])


@jsii.data_type(
    jsii_type="@aws-cdk/integ-tests.IntegTestCaseProps",
    jsii_struct_bases=[aws_cdk.cloud_assembly_schema.TestOptions],
    name_mapping={
        "allow_destroy": "allowDestroy",
        "cdk_command_options": "cdkCommandOptions",
        "diff_assets": "diffAssets",
        "hooks": "hooks",
        "regions": "regions",
        "stack_update_workflow": "stackUpdateWorkflow",
        "stacks": "stacks",
    },
)
class IntegTestCaseProps(aws_cdk.cloud_assembly_schema.TestOptions):
    def __init__(
        self,
        *,
        allow_destroy: typing.Optional[typing.Sequence[builtins.str]] = None,
        cdk_command_options: typing.Optional[aws_cdk.cloud_assembly_schema.CdkCommands] = None,
        diff_assets: typing.Optional[builtins.bool] = None,
        hooks: typing.Optional[aws_cdk.cloud_assembly_schema.Hooks] = None,
        regions: typing.Optional[typing.Sequence[builtins.str]] = None,
        stack_update_workflow: typing.Optional[builtins.bool] = None,
        stacks: typing.Sequence[aws_cdk.core.Stack],
    ) -> None:
        '''(experimental) Properties of an integration test case.

        :param allow_destroy: List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test. This list should only include resources that for this specific integration test we are sure will not cause errors or an outage if destroyed. For example, maybe we know that a new resource will be created first before the old resource is destroyed which prevents any outage. e.g. ['AWS::IAM::Role'] Default: - do not allow destruction of any resources on update
        :param cdk_command_options: Additional options to use for each CDK command. Default: - runner default options
        :param diff_assets: Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included. For example any tests involving custom resources or bundling Default: false
        :param hooks: Additional commands to run at predefined points in the test workflow. e.g. { postDeploy: ['yarn', 'test'] } Default: - no hooks
        :param regions: Limit deployment to these regions. Default: - can run in any region
        :param stack_update_workflow: Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow. Default: true
        :param stacks: (experimental) Stacks to be deployed during the test.

        :stability: experimental
        :exampleMetadata: infused

        Example::

            class StackUnderTest(Stack):
                def __init__(self, scope, id, *, architecture=None, description=None, env=None, stackName=None, tags=None, synthesizer=None, terminationProtection=None, analyticsReporting=None):
                    super().__init__(scope, id, architecture=architecture, description=description, env=env, stackName=stackName, tags=tags, synthesizer=synthesizer, terminationProtection=terminationProtection, analyticsReporting=analyticsReporting)
            
                    lambda_.Function(self, "Handler",
                        runtime=lambda_.Runtime.NODEJS_12_X,
                        handler="index.handler",
                        code=lambda_.Code.from_asset(path.join(__dirname, "lambda-handler")),
                        architecture=architecture
                    )
            
            # Beginning of the test suite
            app = App()
            
            stack = Stack(app, "stack")
            IntegTestCase(stack, "DifferentArchitectures",
                stacks=[
                    StackUnderTest(app, "Stack1",
                        architecture=lambda_.Architecture.ARM_64
                    ),
                    StackUnderTest(app, "Stack2",
                        architecture=lambda_.Architecture.X86_64
                    )
                ]
            )
        '''
        if isinstance(cdk_command_options, dict):
            cdk_command_options = aws_cdk.cloud_assembly_schema.CdkCommands(**cdk_command_options)
        if isinstance(hooks, dict):
            hooks = aws_cdk.cloud_assembly_schema.Hooks(**hooks)
        self._values: typing.Dict[str, typing.Any] = {
            "stacks": stacks,
        }
        if allow_destroy is not None:
            self._values["allow_destroy"] = allow_destroy
        if cdk_command_options is not None:
            self._values["cdk_command_options"] = cdk_command_options
        if diff_assets is not None:
            self._values["diff_assets"] = diff_assets
        if hooks is not None:
            self._values["hooks"] = hooks
        if regions is not None:
            self._values["regions"] = regions
        if stack_update_workflow is not None:
            self._values["stack_update_workflow"] = stack_update_workflow

    @builtins.property
    def allow_destroy(self) -> typing.Optional[typing.List[builtins.str]]:
        '''List of CloudFormation resource types in this stack that can be destroyed as part of an update without failing the test.

        This list should only include resources that for this specific
        integration test we are sure will not cause errors or an outage if
        destroyed. For example, maybe we know that a new resource will be created
        first before the old resource is destroyed which prevents any outage.

        e.g. ['AWS::IAM::Role']

        :default: - do not allow destruction of any resources on update
        '''
        result = self._values.get("allow_destroy")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def cdk_command_options(
        self,
    ) -> typing.Optional[aws_cdk.cloud_assembly_schema.CdkCommands]:
        '''Additional options to use for each CDK command.

        :default: - runner default options
        '''
        result = self._values.get("cdk_command_options")
        return typing.cast(typing.Optional[aws_cdk.cloud_assembly_schema.CdkCommands], result)

    @builtins.property
    def diff_assets(self) -> typing.Optional[builtins.bool]:
        '''Whether or not to include asset hashes in the diff Asset hashes can introduces a lot of unneccessary noise into tests, but there are some cases where asset hashes *should* be included.

        For example
        any tests involving custom resources or bundling

        :default: false
        '''
        result = self._values.get("diff_assets")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def hooks(self) -> typing.Optional[aws_cdk.cloud_assembly_schema.Hooks]:
        '''Additional commands to run at predefined points in the test workflow.

        e.g. { postDeploy: ['yarn', 'test'] }

        :default: - no hooks
        '''
        result = self._values.get("hooks")
        return typing.cast(typing.Optional[aws_cdk.cloud_assembly_schema.Hooks], result)

    @builtins.property
    def regions(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Limit deployment to these regions.

        :default: - can run in any region
        '''
        result = self._values.get("regions")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def stack_update_workflow(self) -> typing.Optional[builtins.bool]:
        '''Run update workflow on this test case This should only be set to false to test scenarios that are not possible to test as part of the update workflow.

        :default: true
        '''
        result = self._values.get("stack_update_workflow")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def stacks(self) -> typing.List[aws_cdk.core.Stack]:
        '''(experimental) Stacks to be deployed during the test.

        :stability: experimental
        '''
        result = self._values.get("stacks")
        assert result is not None, "Required property 'stacks' is missing"
        return typing.cast(typing.List[aws_cdk.core.Stack], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IntegTestCaseProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "IntegTestCase",
    "IntegTestCaseProps",
]

publication.publish()
