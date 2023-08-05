from __future__ import annotations

from pony import orm
from pytask import db


class Environment(db.Entity):
    """Collects all information of the environment which should be checked."""

    name = orm.PrimaryKey(str)
    version = orm.Required(str)
    path = orm.Required(str)
