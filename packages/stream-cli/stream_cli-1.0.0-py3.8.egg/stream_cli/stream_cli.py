import stream
import click


StreamUser = {
    'api_key': None,
    'secret_key': None,
    'location': None
}


def _get_client():
    return stream.connect(
        StreamUser['api_key'],
        StreamUser['secret_key'],
        StreamUser['location']
    )


@click.group()
@click.option('-k', '--api-key', required=True, help='getstream.io api key')
@click.option('-s', '--secret-key', required=True, help='getstream.io secret key')
@click.option('-l', '--location', help='getstream.io hosted location')
def cli(api_key: str, secret_key: str):
    StreamUser['api_key'] = api_key
    StreamUser['secret_key'] = secret_key
    StreamUser['location'] = 'us-east'


@cli.command()
@click.option('-f', '--feed-name', required=True, help='name of the feed')
@click.option('-u', '--user', required=True, help='feed user name')
def get_followers(feed_name: str, user: str):
    client = _get_client()
    feed = client.feed(feed_name, user)
    followers = feed.followers()
    print(followers)


@cli.command()
@click.option('-id', '--newsfeed-id', required=True, help='newsfeed id')
def get_notification_by_id(newsfeed_id: str):
    client = _get_client()
    feed = client.feed('notification', newsfeed_id)
    t = feed.get()
    print(t)
    if t:
        for x in t['results']:
            for y in x['activities']:
                print(y['foreign_id'], "IS READ: %s" %
                      x['is_read'], "IS SEEN: %s" % x['is_seen'])


@cli.command()
@click.option('-f', '--feed-name', required=True, help='name of the feed')
@click.option('-u', '--user', required=True, help='feed user name')
@click.option('-id', '--notification_id', required=True, help='ID of the activity to remove from feed')
def remove_activity(feed_name: str, user: str, notification_id: str):
    client = _get_client()
    feed = client.feed(feed_name, user)
    feed.remove_acitivity(notification_id)


@cli.command()
@click.option('-f', '--feed-name', required=True, help='name of the feed')
@click.option('-u', '--user', required=True, help='feed user name')
@click.option('-id', '--notification_id', required=True, help='ID of the activity to remove from feed')
def update_mark_seen(feed_name: str, user: str, notification_id: str):
    client = _get_client()
    feed = client.feed(feed_name, user)
    response = feed.get(mark_seen=[notification_id],
                        mark_read=[notification_id])


@cli.command()
@click.option('-f', '--feed-name', required=True, help='name of the feed')
@click.option('-u', '--user', required=True, help='feed user name')
def delete_all_activity_from_feed(feed_name: str, user: str):
    client = _get_client()
    feed = client.feed(feed_name, user)

    for x in feed.get()['results']:
        print('Removing activity: {}'.format(x['foreign_id']))
        feed.remove_activity(foreign_id=x['foreign_id'])


@cli.command()
@click.option('-f', '--feed-name', required=True, help='name of the feed')
@click.option('-u', '--user', required=True, help='feed user name')
@click.option('-id', '--notification_id', required=True, help='ID of the activity to remove from feed')
def delete_activity_from_feed(feed_name: str, user: str, notification_id=str):
    client = _get_client()
    feed = client.feed(feed_name, user)
    feed.remove_activity(foreign_id=notification_id)


@cli.command()
@click.option('-f', '--feed-name', required=True, help='name of the feed')
@click.option('-u', '--user', required=True, help='feed user name')
def get_activities_from_feed(feed_name: str, user: str):
    client = _get_client()
    feed = client.feed(feed_name, user)
    t = feed.get()
    if t:
        for x in t['results']:
            print(x)


if __name__ == '__main__':
    cli()