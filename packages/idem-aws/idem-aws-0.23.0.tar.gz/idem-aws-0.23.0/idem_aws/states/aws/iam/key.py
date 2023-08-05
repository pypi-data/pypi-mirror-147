import copy
from typing import Any
from typing import Dict

SERVICE = "iam"
RESOURCE = "Key"

__contracts__ = ["resource"]


async def present(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    user_name: str = None,
    access_key_id: str = None,
    status: str = "Active",
    pgp_key: str = None,
    secret_access_key: str = None,
) -> Dict[str, Any]:
    r"""
    Ensures an AWS key has the assigned status.

    This will create a new access key for a user if no access_key_id is passed for this state, either via
    access_key_id or resource_id.

    If a new access key is created, the secret access key will also be returned. This can optionally be encrypted
    with a base 64 encoded PGP public key.

    Args:
        name(Text): An Idem name describing the resource.
        user_name(Text, optional): The name of the IAM user the key belongs to or will belong to.
        access_key_id(Text, optional): The identifier of the key to manage.
        resource_id(Text, optional): An identifier of the resource in the provider.
        status(Text, optional): "Active" or "Inactive"; Active keys are valid for API calls. Defaults to "Active".
        pgp_key(Text, optional): A base 64 encode PGP public key, used to encrypt the secret access key if a new key is created.
        secret_access_key(Text, optional): Used internally to make sure the secret_access_key isn't lost after the 1st present run.
    Returns:
        Dict[str, Any]
    Examples:
        .. code-block:: sls
            name_describing_key:
              aws.iam.access_key.present:
                - user_name: aws_user
                - status: Active
    """
    result = {
        "name": name,
        "old_state": None,
        "new_state": None,
        "comment": (),
        "result": True,
    }

    if resource_id:
        parts = resource_id.rsplit("-", 1)
        user_name, access_key_id = parts

    if not user_name:
        result["result"] = False
        result["comment"] += (f"Cannot determine username for aws.iam.key {name}",)
        return result

    # ----- look up key
    if access_key_id:
        list_ret = await hub.exec.aws.iam.key.list(
            ctx, access_key_id=access_key_id, user_name=user_name
        )
        if not list_ret["result"]:
            result["result"] = False
            result["comment"] += (f"Error listing access keys",) + list_ret["comment"]
            return result
        elif len(list_ret["ret"]) == 0:
            # Note: To my knowledge, data returned from present is not re-written to the state file.
            #  This means that even though we could create a new key and return the new resource_id,
            #  the state file itself could say "access_key_id=ORIGINAL_KEY", while the resource_id
            #  points to REPLACEMENT_KEY. This would be very confusing, so we return an error.
            message = (
                f"The specified access_key_id in aws.iam.key {name} does not exist, and keys "
                "cannot be recreated by id. Remove the access_key_id and re-run. "
                "If the access_key_id came via resource_id, you may need to run the "
                "absent state to fully purge the key."
            )
            result["comment"] += (message,) + list_ret["comment"]
            result["result"] = False
            return result

        before = list_ret["ret"][0] if len(list_ret["ret"]) else None
        if before and secret_access_key:
            before["secret_access_key"] = secret_access_key
        result[
            "old_state"
        ] = hub.tool.aws.iam.conversion_utils.convert_access_key_to_present(
            before, name
        )
    else:
        before = None

    # ----- create/update
    # Usually present states do the following:
    #  - read before
    #  - create or update if necessary
    #  - read after
    #
    # This doesn't work for keys, because reads do not return the secret key.
    #  The secret key is only returned by create.
    # Also, create can't set status.
    # This means that create and update may both be necessary
    # On the plus side, only status is assignable by us so no post-read is needed -
    #  after a successful update we take `before` or `create_ret["ret"]` data
    #  and set the status to whatever was passed in.
    #
    # Note that ctx["test"] is handled by create and update
    #  So we run through the code, then add a comment at the very end
    #  saying it didn't really happen.
    if before and before["status"] == status:
        result["comment"] += (f"No changes necessary for aws.iam.key {name}",)
        result["new_state"] = result["old_state"]
    elif before:
        # only update is necessary
        update_ret = await hub.exec.aws.iam.key.update(
            ctx, user_name=user_name, access_key_id=access_key_id, status=status
        )
        if not update_ret["result"]:
            result["comment"] += update_ret["comment"]
            result["result"] = False
        else:
            after = copy.copy(before)
            after["status"] = status
            result[
                "new_state"
            ] = hub.tool.aws.iam.conversion_utils.convert_access_key_to_present(
                after, name
            )
            result["comment"] += (f"Updated aws.iam.key {name} to {status}",)
    elif status == "Active":
        # only create is necessary
        create_ret = await hub.exec.aws.iam.key.create(ctx, user_name, pgp_key)
        if not create_ret["result"]:
            result["result"] = False
            result["comment"] += create_ret["comment"]
        else:
            result["comment"] += (f"Created aws.iam.key {name} as {status}",)
            result[
                "new_state"
            ] = hub.tool.aws.iam.conversion_utils.convert_access_key_to_present(
                create_ret["ret"], name
            )
    else:
        # status = "Inactive", both create and update are necessary
        create_ret = await hub.exec.aws.iam.key.create(ctx, user_name, pgp_key)
        if not create_ret["result"]:
            result["result"] = False
            result["comment"] += create_ret["comment"]
        else:
            access_key_id = create_ret["ret"]["access_key_id"]
            update_ret = await hub.exec.aws.iam.key.update(
                ctx, user_name=user_name, access_key_id=access_key_id, status=status
            )
            if not update_ret["result"]:
                result["comment"] += update_ret["comment"]
                result["result"] = False
            else:
                create_ret["ret"]["status"] = status
                result[
                    "new_state"
                ] = hub.tool.aws.iam.conversion_utils.convert_access_key_to_present(
                    create_ret["ret"], name
                )
                result["comment"] += (f"Created aws.iam.key {name} as {status}",)

    if ctx.get("test"):
        result["comment"] = (f"In test mode, no changes occurred",) + result["comment"]

    return result


async def absent(
    hub,
    ctx,
    name: str,
    resource_id: str = None,
    user_name: str = None,
    access_key_id: str = None,
) -> Dict[str, Any]:
    r"""
    Ensure the specified access key does not exist.
    Either resource_id or both user_name and access_key_id must be passed in.

    Args:
        name(Text): An Idem name describing the resource.
        resource_id(Text): An identifier of the resource in the provider.
        user_name(Text, optional): The name of the user whose access key pair you want to delete.
        access_key_id(Text, optional): The access key ID for the access key ID and secret access key you want to delete.
    Returns:
        Dict[str, Any]
    Examples:
        .. code-block:: sls
            name_describing_key:
              aws.iam.access_key.absent:
                - user_name: value
                - access_key_id: value
    """
    result = {
        "name": name,
        "old_state": None,
        "new_state": None,
        "comment": (),
        "result": True,
    }

    if resource_id:
        parts = resource_id.rsplit("-", 1)
        user_name, access_key_id = parts

    if not user_name and access_key_id:
        result["result"] = False
        result["comment"] += (
            f"Cannot determine username and access_key_id for aws.iam.key {name}",
        )
        return result

    # ------ look up key
    list_ret = await hub.exec.aws.iam.key.list(
        ctx, access_key_id=access_key_id, user_name=user_name
    )
    if not list_ret["result"]:
        result["result"] = False
        result["comment"] += (f"Error listing access keys",) + list_ret["comment"]
        return result
    if len(list_ret["ret"]) == 0:
        result["comment"] += (f"aws.iam.key {name} is already absent",) + list_ret[
            "comment"
        ]
        return result

    access_key = list_ret["ret"][0]
    result[
        "old_state"
    ] = hub.tool.aws.iam.conversion_utils.convert_access_key_to_present(
        access_key, name
    )

    # ------ delete key
    # delete logic is handled inside exec's delete, including ctx["test"]
    delete_ret = await hub.exec.aws.iam.key.delete(
        ctx, access_key_id=access_key_id, user_name=user_name
    )
    result["comment"] += delete_ret["comment"]
    result["result"] = delete_ret["result"]

    if ctx["test"]:
        result["comment"] += (f"Would delete aws.iam.key {name}",)
        return result

    return result


async def describe(hub, ctx) -> Dict[str, Dict[str, Any]]:
    r"""
    Describe access keys and their current status in a way that can be managed via the "present" function.

    We describe all access keys for all users the logged in user can list.

    Returns:
        Dict[str, Any]
    Examples:
        .. code-block:: bash
            $ idem describe aws.iam.access_key
    """
    users_list = await hub.exec.aws.iam.user.list(ctx)
    if not users_list["result"]:
        hub.log.debug(f"Could not describe keys: {users_list['comment']}")
        return {}
    users = [u["user_name"] for u in users_list["ret"]]

    result = {}

    for user in users:
        result.update(await _describe_one_user(hub, ctx, user))
    # The above is pretty slow, if/when we add random exponential backoff on
    #  failures, switch to this code:
    # multi_result = await asyncio.gather(
    #     *[_describe_one_user(hub, ctx, u["user_name"]) for u in users]
    # )
    # for r in multi_result:
    #     result.update(r)

    return result


async def _describe_one_user(hub, ctx, user_name: str) -> Dict[str, Dict[str, Any]]:
    keys = await hub.exec.aws.iam.key.list(ctx, user_name=user_name)
    if not keys["result"]:
        hub.log.debug(
            f"Could not list aws.iam.key access keys for user {user_name}: {keys['comment']}"
        )
        return {}

    result = {}

    i = 0
    for access_key in keys["ret"]:
        # iterate every loop to give the user another indication if keys are skipped
        i += 1
        if "access_key_id" not in access_key or "status" not in access_key:
            # All values are "optionally" returned from AWS but managing a key
            #  without the id and status would be impossible.
            hub.log.debug(f"Can not describe an aws key without an id and status")
            continue

        if "create_date" in access_key:
            create_date = access_key["create_date"].strftime("%Y-%b-%d")
        else:
            create_date = "--"

        idem_name = f"{access_key['user_name']}-key-{i}-{create_date}"

        state = hub.tool.aws.iam.conversion_utils.convert_access_key_to_present(
            access_key, idem_name
        )

        result[idem_name] = {"aws.iam.key.present": [{k: v} for k, v in state.items()]}

    return result
