"""robots.txt and sitemap.xml generation"""

from pathlib import Path


def sitemap_url(posts: list, output: Path):
    """ """
    from lotek.lib.context import config

    sitemap_urls = [f"  <url><loc>{config.site.url}/</loc></url>"]
    for post in posts:
        sitemap_urls.append(
            f'  <url><loc>{config.site.url}/posts/{post.get("slug")}.html</loc>'
            f'<lastmod>{post["date"]}</lastmod></url>'
        )
    (output / "sitemap.xml").write_text(
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
        + "\n".join(sitemap_urls)
        + "\n</urlset>\n"
    )


def generate_robots(posts: list, output: Path):
    """write a robots.txt file to the output directory

    also generates the sitemap.xml file since it's halfway related to robots"""
    from lotek.lib.context import config

    (output / "robots.txt").write_text(
        f"User-agent: *\nAllow: /\nSitemap: {config.site.url}/sitemap.xml\n"
    )

    sitemap_url(posts, output)
