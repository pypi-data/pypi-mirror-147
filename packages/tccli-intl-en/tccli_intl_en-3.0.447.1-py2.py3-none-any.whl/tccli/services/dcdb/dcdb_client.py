# -*- coding: utf-8 -*-
import os
import sys
import six
import json
import tccli.options_define as OptionsDefine
import tccli.format_output as FormatOutput
from tccli import __version__
from tccli.utils import Utils
from tccli.exceptions import ConfigurationError, ParamError
from tencentcloud.common import credential
from tencentcloud.common.profile.http_profile import HttpProfile
from tencentcloud.common.profile.client_profile import ClientProfile
from tencentcloud.dcdb.v20180411 import dcdb_client as dcdb_client_v20180411
from tencentcloud.dcdb.v20180411 import models as models_v20180411


def doDescribeDCDBInstances(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeDCDBInstancesRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.DescribeDCDBInstances(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDescribeFileDownloadUrl(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeFileDownloadUrlRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.DescribeFileDownloadUrl(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doResetAccountPassword(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.ResetAccountPasswordRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.ResetAccountPassword(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDescribeFlow(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeFlowRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.DescribeFlow(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doSwitchDBInstanceHA(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.SwitchDBInstanceHARequest()
    model.from_json_string(json.dumps(args))
    rsp = client.SwitchDBInstanceHA(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doGrantAccountPrivileges(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.GrantAccountPrivilegesRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.GrantAccountPrivileges(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDeleteAccount(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DeleteAccountRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.DeleteAccount(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doModifyDBInstancesProject(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.ModifyDBInstancesProjectRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.ModifyDBInstancesProject(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDescribeDBLogFiles(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeDBLogFilesRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.DescribeDBLogFiles(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDescribeDBSyncMode(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeDBSyncModeRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.DescribeDBSyncMode(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDescribeProjectSecurityGroups(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeProjectSecurityGroupsRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.DescribeProjectSecurityGroups(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doAssociateSecurityGroups(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.AssociateSecurityGroupsRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.AssociateSecurityGroups(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doCreateAccount(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.CreateAccountRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.CreateAccount(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDestroyDCDBInstance(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DestroyDCDBInstanceRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.DestroyDCDBInstance(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDescribeDCDBInstanceNodeInfo(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeDCDBInstanceNodeInfoRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.DescribeDCDBInstanceNodeInfo(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDescribeProjects(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeProjectsRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.DescribeProjects(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doCloseDBExtranetAccess(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.CloseDBExtranetAccessRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.CloseDBExtranetAccess(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doModifyAccountDescription(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.ModifyAccountDescriptionRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.ModifyAccountDescription(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDescribeDcnDetail(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeDcnDetailRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.DescribeDcnDetail(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doCopyAccountPrivileges(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.CopyAccountPrivilegesRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.CopyAccountPrivileges(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDestroyHourDCDBInstance(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DestroyHourDCDBInstanceRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.DestroyHourDCDBInstance(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDescribeDBSecurityGroups(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DescribeDBSecurityGroupsRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.DescribeDBSecurityGroups(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doCancelDcnJob(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.CancelDcnJobRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.CancelDcnJob(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doCreateHourDCDBInstance(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.CreateHourDCDBInstanceRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.CreateHourDCDBInstance(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doDisassociateSecurityGroups(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.DisassociateSecurityGroupsRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.DisassociateSecurityGroups(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


def doModifyDBInstanceSecurityGroups(args, parsed_globals):
    g_param = parse_global_arg(parsed_globals)

    cred = credential.Credential(
        g_param[OptionsDefine.SecretId], g_param[OptionsDefine.SecretKey], g_param[OptionsDefine.Token]
    )
    http_profile = HttpProfile(
        reqTimeout=60 if g_param[OptionsDefine.Timeout] is None else int(g_param[OptionsDefine.Timeout]),
        reqMethod="POST",
        endpoint=g_param[OptionsDefine.Endpoint]
    )
    profile = ClientProfile(httpProfile=http_profile, signMethod="HmacSHA256")
    mod = CLIENT_MAP[g_param[OptionsDefine.Version]]
    client = mod.DcdbClient(cred, g_param[OptionsDefine.Region], profile)
    client._sdkVersion += ("_CLI_" + __version__)
    models = MODELS_MAP[g_param[OptionsDefine.Version]]
    model = models.ModifyDBInstanceSecurityGroupsRequest()
    model.from_json_string(json.dumps(args))
    rsp = client.ModifyDBInstanceSecurityGroups(model)
    result = rsp.to_json_string()
    try:
        json_obj = json.loads(result)
    except TypeError as e:
        json_obj = json.loads(result.decode('utf-8'))  # python3.3
    FormatOutput.output("action", json_obj, g_param[OptionsDefine.Output], g_param[OptionsDefine.Filter])


CLIENT_MAP = {
    "v20180411": dcdb_client_v20180411,

}

MODELS_MAP = {
    "v20180411": models_v20180411,

}

ACTION_MAP = {
    "DescribeDCDBInstances": doDescribeDCDBInstances,
    "DescribeFileDownloadUrl": doDescribeFileDownloadUrl,
    "ResetAccountPassword": doResetAccountPassword,
    "DescribeFlow": doDescribeFlow,
    "SwitchDBInstanceHA": doSwitchDBInstanceHA,
    "GrantAccountPrivileges": doGrantAccountPrivileges,
    "DeleteAccount": doDeleteAccount,
    "ModifyDBInstancesProject": doModifyDBInstancesProject,
    "DescribeDBLogFiles": doDescribeDBLogFiles,
    "DescribeDBSyncMode": doDescribeDBSyncMode,
    "DescribeProjectSecurityGroups": doDescribeProjectSecurityGroups,
    "AssociateSecurityGroups": doAssociateSecurityGroups,
    "CreateAccount": doCreateAccount,
    "DestroyDCDBInstance": doDestroyDCDBInstance,
    "DescribeDCDBInstanceNodeInfo": doDescribeDCDBInstanceNodeInfo,
    "DescribeProjects": doDescribeProjects,
    "CloseDBExtranetAccess": doCloseDBExtranetAccess,
    "ModifyAccountDescription": doModifyAccountDescription,
    "DescribeDcnDetail": doDescribeDcnDetail,
    "CopyAccountPrivileges": doCopyAccountPrivileges,
    "DestroyHourDCDBInstance": doDestroyHourDCDBInstance,
    "DescribeDBSecurityGroups": doDescribeDBSecurityGroups,
    "CancelDcnJob": doCancelDcnJob,
    "CreateHourDCDBInstance": doCreateHourDCDBInstance,
    "DisassociateSecurityGroups": doDisassociateSecurityGroups,
    "ModifyDBInstanceSecurityGroups": doModifyDBInstanceSecurityGroups,

}

AVAILABLE_VERSION_LIST = [
    "v20180411",

]


def action_caller():
    return ACTION_MAP


def parse_global_arg(parsed_globals):
    g_param = parsed_globals

    is_exist_profile = True
    if not parsed_globals["profile"]:
        is_exist_profile = False
        g_param["profile"] = "default"

    configure_path = os.path.join(os.path.expanduser("~"), ".tccli")
    is_conf_exist, conf_path = Utils.file_existed(configure_path, g_param["profile"] + ".configure")
    is_cred_exist, cred_path = Utils.file_existed(configure_path, g_param["profile"] + ".credential")

    conf = {}
    cred = {}

    if is_conf_exist:
        conf = Utils.load_json_msg(conf_path)
    if is_cred_exist:
        cred = Utils.load_json_msg(cred_path)

    if not (isinstance(conf, dict) and isinstance(cred, dict)):
        raise ConfigurationError(
            "file: %s or %s is not json format"
            % (g_param["profile"] + ".configure", g_param["profile"] + ".credential"))

    if OptionsDefine.Token not in cred:
        cred[OptionsDefine.Token] = None

    if not is_exist_profile:
        if os.environ.get(OptionsDefine.ENV_SECRET_ID) and os.environ.get(OptionsDefine.ENV_SECRET_KEY):
            cred[OptionsDefine.SecretId] = os.environ.get(OptionsDefine.ENV_SECRET_ID)
            cred[OptionsDefine.SecretKey] = os.environ.get(OptionsDefine.ENV_SECRET_KEY)
            cred[OptionsDefine.Token] = os.environ.get(OptionsDefine.ENV_TOKEN)

        if os.environ.get(OptionsDefine.ENV_REGION):
            conf[OptionsDefine.Region] = os.environ.get(OptionsDefine.ENV_REGION)

    for param in g_param.keys():
        if g_param[param] is None:
            if param in [OptionsDefine.SecretKey, OptionsDefine.SecretId, OptionsDefine.Token]:
                if param in cred:
                    g_param[param] = cred[param]
                else:
                    raise ConfigurationError("%s is invalid" % param)
            elif param in [OptionsDefine.Region, OptionsDefine.Output]:
                if param in conf:
                    g_param[param] = conf[param]
                else:
                    raise ConfigurationError("%s is invalid" % param)

    try:
        if g_param[OptionsDefine.ServiceVersion]:
            g_param[OptionsDefine.Version] = "v" + g_param[OptionsDefine.ServiceVersion].replace('-', '')
        else:
            version = conf["dcdb"][OptionsDefine.Version]
            g_param[OptionsDefine.Version] = "v" + version.replace('-', '')

        if g_param[OptionsDefine.Endpoint] is None:
            g_param[OptionsDefine.Endpoint] = conf["dcdb"][OptionsDefine.Endpoint]
    except Exception as err:
        raise ConfigurationError("config file:%s error, %s" % (conf_path, str(err)))

    if g_param[OptionsDefine.Version] not in AVAILABLE_VERSION_LIST:
        raise Exception("available versions: %s" % " ".join(AVAILABLE_VERSION_LIST))

    if six.PY2:
        for key, value in g_param.items():
            if isinstance(value, six.text_type):
                g_param[key] = value.encode('utf-8')
    return g_param

