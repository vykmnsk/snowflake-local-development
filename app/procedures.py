from __future__ import annotations

import sys

from snowflake.snowpark import Session


def hello_procedure(session: Session, name: str) -> str:
    return f'Hello procedural {name}!'


# For local debugging
# Beware you may need to type-convert arguments if you add input parameters
if __name__ == "__main__":
    # Create a local Snowpark session
    with Session.builder.config("local_testing", True).getOrCreate() as session:
        print(hello_procedure(session, *sys.argv[1:]))  # type: ignore
