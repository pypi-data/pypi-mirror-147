"""Contains util methods."""
from typing import List

from .constraint import BinaryConstraint, Literal, MappedPlaceholder
from .types import SQL, Params


def constraint_list_to_sql(
    constraints: List[BinaryConstraint],
    *,
    paren: bool = True,
    joiner: str = " and ",
    offset: int = 0,
    handle_null: bool = True
) -> SQL:
    """Turns a list of constraints into a (sql, params) pair."""
    parts: List[str] = []
    params: Params = []
    placeholder_index = offset + 1

    for constraint in constraints:
        if constraint.value is None and handle_null:
            if constraint.operator in {"=", "is"}:
                operator = "is"
            elif constraint.operator in {"!=", "<>", "is not"}:
                operator = "is not"
            else:
                raise Exception(
                    "Invalid operator for null comparison: {}".format(
                        constraint.operator
                    )
                )

            parts.append("{} {} null".format(constraint.column, operator))
        elif isinstance(constraint.value, Literal):
            parts.append(
                "{} {} {}".format(
                    constraint.column, constraint.operator, constraint.value.value
                )
            )
        elif isinstance(constraint.value, MappedPlaceholder):
            placeholder = "${}".format(placeholder_index)
            placeholder_index += 1

            parts.append(
                "{} {} {}".format(
                    constraint.column,
                    constraint.operator,
                    constraint.value.get_mapped_placeholder(placeholder),
                )
            )
            params.append(constraint.value.value)
        elif isinstance(constraint.value, list):
            in_list = ", ".join(
                generate_placeholders(len(constraint.value), placeholder_index)
            )
            parts.append(
                "{} {} ({})".format(
                    constraint.column,
                    constraint.operator,
                    in_list,
                )
            )
            params.extend(constraint.value)
            placeholder_index += len(constraint.value)
        else:
            parts.append(
                "{} {} ${}".format(
                    constraint.column, constraint.operator, placeholder_index
                )
            )
            params.append(constraint.value)
            placeholder_index += 1

    if paren:
        sql = joiner.join("({})".format(p) for p in parts)
    else:
        sql = joiner.join(parts)

    return (sql, params)


def generate_placeholders(count: int, start_at: int = 1) -> List[str]:
    return ["${}".format(ph + start_at) for ph in range(count)]
