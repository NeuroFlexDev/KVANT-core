# -*- coding: utf-8 -*-
import click
from settings import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, DB_PORT


@click.command()
def sqitch_uri():
    print(f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}")


if __name__ == "__main__":
    sqitch_uri()
