import click
from .sync_to_redis import sync_all_features
from datetime import datetime

@click.command()
@click.option('--date', default=datetime.today().strftime('%Y-%m-%d'), help='Date to sync')
def cli(date):
    print(f"Syncing features for date: {date}")
    sync_all_features(date)
    print("Done")

if __name__ == '__main__':
    cli()
