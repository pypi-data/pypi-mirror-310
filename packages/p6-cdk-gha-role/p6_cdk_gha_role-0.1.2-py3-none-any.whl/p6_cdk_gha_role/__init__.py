r'''
DESC

# P6CDKGHARole

## LICENSE

[![License](https://img.shields.io/badge/License-Apache%202.0-yellowgreen.svg)](https://opensource.org/licenses/Apache-2.0)

## Other

![Gitpod ready-to-code](https://img.shields.io/badge/Gitpod-ready--to--code-blue?logo=gitpod) ![Sonarcloud Status](https://sonarcloud.io/api/project_badges/measure?project=p6m7g8_p6-cdk-gha-role&metric=alert_status) ![GitHub commit activity](https://img.shields.io/github/commit-activity/y/p6m7g8/p6-cdk-gha-role) ![GitHub commit activity](https://img.shields.io/github/commit-activity/m/p6m7g8/p6-cdk-gha-role)

## Usage

```python
...
import { P6CDKGHARole } from 'p6-cdk-gha-role';

new P6CDKGHARole(this, 'P6CDKGHARole', {
  principle: arn,
  repo: 'org/repo',
  policies: []
});
```

## Architecture

![./assets/diagram.png](./assets/diagram.png)

## Author

Philip M. Gollucci [pgollucci@p6m7g8.com](mailto:pgollucci@p6m7g8.com)
'''
from pkgutil import extend_path
__path__ = extend_path(__path__, __name__)

import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

import typeguard
from importlib.metadata import version as _metadata_package_version
TYPEGUARD_MAJOR_VERSION = int(_metadata_package_version('typeguard').split('.')[0])

def check_type(argname: str, value: object, expected_type: typing.Any) -> typing.Any:
    if TYPEGUARD_MAJOR_VERSION <= 2:
        return typeguard.check_type(argname=argname, value=value, expected_type=expected_type) # type:ignore
    else:
        if isinstance(value, jsii._reference_map.InterfaceDynamicProxy): # pyright: ignore [reportAttributeAccessIssue]
           pass
        else:
            if TYPEGUARD_MAJOR_VERSION == 3:
                typeguard.config.collection_check_strategy = typeguard.CollectionCheckStrategy.ALL_ITEMS # type:ignore
                typeguard.check_type(value=value, expected_type=expected_type) # type:ignore
            else:
                typeguard.check_type(value=value, expected_type=expected_type, collection_check_strategy=typeguard.CollectionCheckStrategy.ALL_ITEMS) # type:ignore

from ._jsii import *

import aws_cdk as _aws_cdk_ceddda9d
import aws_cdk.aws_iam as _aws_cdk_aws_iam_ceddda9d
import constructs as _constructs_77d1e7e8


@jsii.interface(jsii_type="p6-cdk-gha-role.IP6CDKGHARoleProps")
class IP6CDKGHARoleProps(typing_extensions.Protocol):
    @builtins.property
    @jsii.member(jsii_name="principle")
    def principle(self) -> _aws_cdk_ceddda9d.Arn:
        ...

    @builtins.property
    @jsii.member(jsii_name="repo")
    def repo(self) -> builtins.str:
        ...

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.IManagedPolicy]]:
        ...


class _IP6CDKGHARolePropsProxy:
    __jsii_type__: typing.ClassVar[str] = "p6-cdk-gha-role.IP6CDKGHARoleProps"

    @builtins.property
    @jsii.member(jsii_name="principle")
    def principle(self) -> _aws_cdk_ceddda9d.Arn:
        return typing.cast(_aws_cdk_ceddda9d.Arn, jsii.get(self, "principle"))

    @builtins.property
    @jsii.member(jsii_name="repo")
    def repo(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "repo"))

    @builtins.property
    @jsii.member(jsii_name="policies")
    def policies(
        self,
    ) -> typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.IManagedPolicy]]:
        return typing.cast(typing.Optional[typing.List[_aws_cdk_aws_iam_ceddda9d.IManagedPolicy]], jsii.get(self, "policies"))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the interface
typing.cast(typing.Any, IP6CDKGHARoleProps).__jsii_proxy_class__ = lambda : _IP6CDKGHARolePropsProxy


class P6CDKGHARole(
    _aws_cdk_ceddda9d.Resource,
    metaclass=jsii.JSIIMeta,
    jsii_type="p6-cdk-gha-role.P6CDKGHARole",
):
    def __init__(
        self,
        scope: _constructs_77d1e7e8.Construct,
        id: builtins.str,
        props: IP6CDKGHARoleProps,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param props: -
        '''
        if __debug__:
            type_hints = typing.get_type_hints(_typecheckingstub__2c57fd84d672e5dc91e2541b279959fcfcbb4573e6a6dab6caad9997f6c624af)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument props", value=props, expected_type=type_hints["props"])
        jsii.create(self.__class__, self, [scope, id, props])


__all__ = [
    "IP6CDKGHARoleProps",
    "P6CDKGHARole",
]

publication.publish()

def _typecheckingstub__2c57fd84d672e5dc91e2541b279959fcfcbb4573e6a6dab6caad9997f6c624af(
    scope: _constructs_77d1e7e8.Construct,
    id: builtins.str,
    props: IP6CDKGHARoleProps,
) -> None:
    """Type checking stubs"""
    pass
