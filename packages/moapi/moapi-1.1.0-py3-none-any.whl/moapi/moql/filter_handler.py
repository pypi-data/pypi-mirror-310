from typing import Callable, Pattern

from moapi.moql.type_mapping import DEFAULT_CASTING_RULES
from moapi.moql.errors import (
    CustomCasterError,
    ListOperatorError,
    FilterError,
)
from moapi.moql.constants import EMPTY_STRING
from moapi.moql.operator_mapping import (
    MOQL_OPERATORS,
    MONGO_OPERATOR_MAPPING,
)


def find_operator(filter_item: str) -> str | None:
    for operator in MOQL_OPERATORS:
        if filter_item.find(operator) > -1:
            return operator
    return EMPTY_STRING


CASTING_RULE_TEMPLATE_PREFIX: str = "{rule}("
CASTING_RULE_TEMPLATE_SUFFIX: str = ")"
CUSTOM_CASTER_ERROR_TEMPLATE: str = (
    "Unable to apply {rule} custom cast on {value}"
)
LIST_OPERATOR_ERROR_TEMPLATE: str = "Invalid list operator {operator}"
FILTER_ERROR: str = "Failed to apply filter. Invalid operator"


# ---------------------------------------------------------
# FUNCTION DEFAULT CAST
# ---------------------------------------------------------
def default_cast(value: str):
    for regex, cast_operation in DEFAULT_CASTING_RULES.items():
        if isinstance(regex, Pattern):
            if regex.match(value):
                return cast_operation(value)
        elif regex == value.lower():
            return cast_operation(value)
    return value


# ---------------------------------------------------------
# FUNCTION CUSTOM CAST
# ---------------------------------------------------------
def custom_cast(
    casters: dict[str, Callable[[any], any]] | None, value: str
) -> any:
    if casters:
        for rule, cast_function in casters.items():
            if has_custom_rule_format(rule=rule, value=value):
                try:
                    return cast_function(
                        value.replace(
                            CASTING_RULE_TEMPLATE_PREFIX.format(rule=rule),
                            EMPTY_STRING,
                        )[:-1]
                    )
                except Exception as error:
                    handle_custom_cast_exception(
                        error=error, rule=rule, value=value
                    )
    return None


# ---------------------------------------------------------
# FUNCTION HAS CUSTOM RULE FORMAT
# ---------------------------------------------------------
def has_custom_rule_format(rule: any, value: str) -> bool:
    return value.startswith(
        CASTING_RULE_TEMPLATE_PREFIX.format(rule=rule)
    ) and value.endswith(CASTING_RULE_TEMPLATE_SUFFIX)


# ---------------------------------------------------------
# FUNCTION HANDLE CUSTOM CAST EXCEPTION
# ---------------------------------------------------------
def handle_custom_cast_exception(error: Exception, rule: str, value: str):
    raise CustomCasterError(
        CUSTOM_CASTER_ERROR_TEMPLATE.format(rule=rule, value=value)
    ) from error


# ---------------------------------------------------------
# FUNCTION CAST
# ---------------------------------------------------------
def cast(
    value: str, casters: dict[str, Callable[[any], any]] | None
) -> any:
    casted_value: any = custom_cast(casters=casters, value=value)
    if casted_value is None:
        casted_value = default_cast(value)
    return casted_value


# ---------------------------------------------------------
# FUNCTION IS_LIST
# ---------------------------------------------------------
def is_list(value: any) -> bool:
    return isinstance(value, list)


def is_not_list(value: any) -> bool:
    return not is_list(value)


# ---------------------------------------------------------
# FUNCTION BUILD QUERY
# ---------------------------------------------------------
def build_query(
    operator: str,
    key: str,
    value: any,
    casters: dict[str, Callable[[any], any]] | None,
) -> dict:
    # TODO move hard-coded values to constants here
    # TODO I'll probably refactor this function later
    # When operator is =
    if operator == "=" and is_not_list(value):
        return {key: value}

    # When operator is = or != but value is a list
    if is_list(value):
        casted_items: list[any] = [cast(item, casters) for item in value]
        if operator == "=":
            return {key: {"$in": casted_items}}
        elif operator == "!=":
            return {key: {"$nin": casted_items}}
        raise ListOperatorError(
            LIST_OPERATOR_ERROR_TEMPLATE.format(operator=operator)
        )

    # $exists operator
    if operator in ["", "!"]:
        return {
            value: {
                MONGO_OPERATOR_MAPPING[operator]: operator == EMPTY_STRING
            }
        }

    # $gt, $gte, $lt, $lte, $ne ...
    return {key: {MONGO_OPERATOR_MAPPING[operator]: value}}


# =========================================================
# CLASS HQL FILTER
# =========================================================
class MoQLFilter:

    """
    Builds mongo filters based on the filter parameters
    provided.

    Example input: status=DISCOVERED

    The property mongo_query provides the equivalent
    mongo filter element

    Example: {"status": "DISCOVERED"}
    """

    # -----------------------------------------------------
    # CONSTRUCTOR
    # -----------------------------------------------------
    def __init__(
        self,
        filter_parameter: str,
        custom_casters: dict[str, Callable[[any], any]] | None,
    ):
        self.filter_parameter: str = filter_parameter
        self.operator: str = find_operator(filter_item=filter_parameter)
        self.key: str = EMPTY_STRING
        self.value: any = None
        self.extract_key_value()
        self.casters: dict[
            str, Callable[[any], any]
        ] | None = custom_casters
        self.casted_value: any = self.cast_value()

    # -----------------------------------------------------
    # METHOD EXTRACT KEY VALUE
    # -----------------------------------------------------
    def extract_key_value(self):
        if self.operator != EMPTY_STRING:
            try:
                self.key, self.value = self.filter_parameter.split(
                    self.operator
                )
            except ValueError as error:
                raise FilterError(FILTER_ERROR) from error
        else:
            self.key, self.value = EMPTY_STRING, self.filter_parameter

    # -----------------------------------------------------
    # METHOD CAST VALUE
    # -----------------------------------------------------
    def cast_value(self) -> any:
        return cast(self.value, self.casters)

    # -----------------------------------------------------
    # PROPERTY FILTER
    # -----------------------------------------------------
    @property
    def filter(self) -> dict:
        return build_query(
            operator=self.operator,
            value=self.casted_value,
            key=self.key,
            casters=self.casters,
        )
