"""HTML stubs for rendering templates."""

from lotek.lib.site_config import config


def html_stub_index(post):
    """Generate the HTML for a single post in the index page."""
    return f"""
    <li><span class="date">{post["date"]}</span>
        <a href="posts/{post["slug"]}.html">{post["title"]}</a>
    </li>\n
"""


def html_stub_feed_items(post, html):
    """Generate the HTML for a single post in the feed."""
    return f"""
    <item>
      <title>{post['title']}</title>
      <link>{config.site.url}/posts/{post['slug']}.html</link>
      <pubDate>{post['date']}</pubDate>
      <description><![CDATA[{html}]]></description>
    </item>\n"""
