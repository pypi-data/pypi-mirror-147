from __future__ import annotations

from typing import Any
from typing import Callable

import click
from pytask import hookimpl


@hookimpl
def pytask_extend_command_line_interface(cli: click.Group) -> None:
    """Extend the cli."""
    cli.commands["build"].params.append(
        click.Option(
            ["--update-environment"],
            is_flag=True,
            default=None,
            help="Update the information on the environment stored in the database.",
        )
    )


@hookimpl
def pytask_parse_config(
    config: dict[str, Any],
    config_from_file: dict[str, Any],
    config_from_cli: dict[str, Any],
) -> None:
    """Parse the configuration."""
    config["check_python_version"] = _get_first_non_none_value(
        config_from_file,
        key="check_python_version",
        default=True,
        callback=_convert_truthy_or_falsy_to_bool,
    )

    config["check_environment"] = _get_first_non_none_value(
        config_from_file,
        key="check_environment",
        default=True,
        callback=_convert_truthy_or_falsy_to_bool,
    )

    config["update_environment"] = _get_first_non_none_value(
        config_from_cli,
        key="update_environment",
        default=False,
        callback=_convert_truthy_or_falsy_to_bool,
    )


def _get_first_non_none_value(
    *configs: dict[str, Any],
    key: str,
    default: Any | None = None,
    callback: Callable[..., Any] | None = None,
) -> Any:
    """Get the first non-None value for a key from a list of dictionaries.

    This function allows to prioritize information from many configurations by changing
    the order of the inputs while also providing a default.

    """
    callback = (lambda x: x) if callback is None else callback  # noqa: E731
    processed_values = (callback(config.get(key)) for config in configs)
    return next((value for value in processed_values if value is not None), default)


def _convert_truthy_or_falsy_to_bool(x: bool | str | None) -> bool:
    """Convert truthy or falsy value in .ini to Python boolean."""
    if x in [True, "True", "true", "1"]:
        out = True
    elif x in [False, "False", "false", "0"]:
        out = False
    elif x in [None, "None", "none"]:
        out = None
    else:
        raise ValueError(
            f"Input {x!r} is neither truthy (True, true, 1) or falsy (False, false, 0)."
        )
    return out
