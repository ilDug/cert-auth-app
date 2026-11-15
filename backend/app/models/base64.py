import base64
from typing import Annotated

from fastapi import Path
from pydantic import AfterValidator


def decoded_base64_param(b64):
    try:
        # check if the string is a valid base64 string
        # and return the decoded string
        return base64.urlsafe_b64decode(b64).decode("utf-8")
    except Exception as e:
        raise ValueError(f"Invalid base64 param: {e}")


def validate_base64_param(b64):
    try:
        # check if the string is a valid base64 string
        # and return the raw string
        base64.urlsafe_b64decode(b64)
        return b64
    except Exception as e:
        raise ValueError(f"Invalid base64 param: {e}")


############################################################################

# This parameter automatically decodes the base64 string to a normal string
# Use this when you need the decoded string directly.
Base64Param = Annotated[
    str,
    AfterValidator(decoded_base64_param),
    Path(..., title="the base64 encoded path/filename"),
]

# This parameter returns the raw base64 string when used in the endpoint functions.
# Use this when you need to handle the base64 string directly.
Base64ParamRaw = Annotated[
    str,
    AfterValidator(validate_base64_param),
    Path(..., title="the base64 encoded path/filename"),
]
