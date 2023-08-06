__all__ = [
    # 'sql_',
]

import bg_helper as bh
try:
    from sql_helper import SQL
except ImportError:
    # sql-helper not installed
    SQL = None
else:
    if not bh.tools.docker_ok():
        # Can't use docker
        SQL = None
