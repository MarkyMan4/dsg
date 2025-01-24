# TODO this needs to become actual unit tests, for now I'm using this to just mockup a duckdb database

import duckdb


def main():
    db = duckdb.connect("tests/sample_proj/test.duckdb")
    db.sql("""
        create or replace table test (
            x int,
            y int
        )
    """)

    db.sql("""
        insert into test (x, y) values 
        (1, 4),
        (2, 10),
        (3, 3),
        (4, 7),
        (5, 9)
    """)


if __name__ == "__main__":
    main()
