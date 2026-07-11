"""rss feed generator plugin"""

from datetime import datetime
from zoneinfo import ZoneInfo
from lotek.lib.context import config
from ..lib.html_stubs import html_stub_feed_items
from ..lib.render import render, md_to_html

RFC822 = "%a, %d %b %Y %H:%M:%S %z"


def generate_rss(dirs, posts, out):
    from lotek.lib.context import config
    feed_items = ""
    for post in posts[: config.rss.limit]:
        # Use raw markdown body instead of HTML for RSS feed
        # md_to_html is expensive (pandoc subprocess) and RSS doesn't need styled HTML
        feed_items += html_stub_feed_items(post, post["body"])
    build_date = datetime.now(ZoneInfo(config.rss.timezone)).strftime(RFC822)
    feed = render(dirs,
        "feed.xml",
        {
            "SITE_TITLE": config.site.title,
            "SITE_URL": config.site.url,
            "SITE_DESC": config.site.description,
            "ITEMS": feed_items,
            "BUILD_DATE": build_date,
        },
    )
    (out / "feed.xml").write_text(feed)
