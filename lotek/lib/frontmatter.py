"""frontmatter parsing for markdown files"""


def parse_frontmatter(text):
    """parse the frontmatter from a markdown file, returning a dict of metadata and the body text"""
    if not text.startswith("---\n"):
        return {}, text
    try:
        end = text.index("\n---\n", 4)
    except ValueError:
        return {}, text
    meta = {}
    for line in text[4:end].splitlines():
        if ":" in line:
            k, _, v = line.partition(":")
            meta[k.strip()] = v.strip().strip('"')
    return meta, text[end + 5 :]
