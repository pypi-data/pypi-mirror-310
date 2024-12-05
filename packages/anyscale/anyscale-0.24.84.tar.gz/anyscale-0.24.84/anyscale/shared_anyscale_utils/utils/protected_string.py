# AUTOGENERATED - modify shared_anyscale_util in root directory to make changes
#### Testing notes
# To avoid blowing up on the printing of a string value, place the following at the beginning of imports:
# import anyscale.utils.protected_string
# anyscale.utils.protected_string.FAIL_ON_MISUSE = False
#
# When testing routers, please pass in a JSON object with the string & let pydantic construct the ProtectedString
# See test_users_router.py::test_login_user for some examples.

import copy
import hashlib
from typing import Any, Dict, List, Type, Union
import warnings

from anyscale.shared_anyscale_utils.conf import ANYSCALE_ENV


# Whether to hard fail on serializing
FAIL_ON_MISUSE = ANYSCALE_ENV != "production"


class FastApiMixIn:
    @classmethod
    def __get_validators__(cls) -> Any:
        yield cls.validate

    @classmethod
    def __modify_schema__(cls, field_schema: Any) -> Any:
        # __modify_schema__ should mutate the dict it receives in place, the
        # returned value will be ignored
        field_schema.update({"type": "string"})

    @classmethod
    def validate(cls, v: Any) -> Any:
        if not isinstance(v, str):
            raise TypeError("string required")
        return cls(v)  # type: ignore


class ProtectedString(FastApiMixIn):
    def __init__(self, s: Union[str, "ProtectedString"]):
        if isinstance(s, ProtectedString):
            self._UNSAFE_DO_NOT_USE: str = s._UNSAFE_DO_NOT_USE  # noqa: SLF001
        elif isinstance(s, str):
            self._UNSAFE_DO_NOT_USE = s
        else:
            raise ValueError(
                f"{type(s)}:'{s!r}' is not a valid type for ProtectedString"
            )

    def __eq__(self, other: Any) -> bool:
        if isinstance(other, ProtectedString):
            return self._UNSAFE_DO_NOT_USE == other._UNSAFE_DO_NOT_USE  # noqa: SLF001
        return False

    def __str__(self) -> str:
        # This will collide like crazy (~1% chance of collision in 3000 guesses), but since the goal here is human debuggability, that is probably fine.
        m = hashlib.blake2b(self._UNSAFE_DO_NOT_USE.encode("utf-8"), digest_size=4)

        error_msg = "ProtectedStrings should not be serialized directly."
        if FAIL_ON_MISUSE:
            raise RuntimeError(error_msg)
        else:
            warnings.warn(error_msg)
        return f"<{self.__class__.__name__} digest={m.hexdigest()}>"

    def __repr__(self) -> str:
        return str(self)


def protect_strings(
    input_dictionary: Dict[str, Any],
    keys: Union[List[str], str],
    protected_string_type: Type[ProtectedString],  # Callable[[str], ProtectedString]
    allow_optional_strings: bool = False,
) -> Dict[str, Any]:
    result_dict = copy.deepcopy(input_dictionary)
    if isinstance(keys, str):
        keys = [keys]
    for key in keys:
        old_string = result_dict[key]
        if isinstance(old_string, str):
            result_dict[key] = protected_string_type(old_string)
        elif allow_optional_strings and old_string is None:
            result_dict[key] = None
        else:
            raise ValueError("Tried to protect a non-string")

    return result_dict
