"""builds content/pages/*.md to output/*.html"""

import time
from concurrent.futures import ThreadPoolExecutor, as_completed
from lotek.lib.render import render, render_wrap, md_to_html
from lotek.lib.frontmatter import parse_frontmatter
from lotek.lib.logger import log
from lotek.lib.context import config

# Default batch size for parallel processing
DEFAULT_BATCH_SIZE = 10


def _render_single_page(args):
    """Render a single page. Wrapper for ThreadPoolExecutor."""
    dirs, path, out_dir, config = args
    meta, body = parse_frontmatter(path.read_text())
    if meta.get("publish", "").lower() == "false":
        log.info("skipping page %s as it is not published", path.stem)
        return None

    start = time.perf_counter()
    slug = path.stem
    title = meta.get("title", slug)
    html = md_to_html(dirs, body)
    content = render(
        dirs,
        "post.html",
        {
            "TITLE": title,
            "DATE": meta.get("date", ""),
            "CONTENT": html,
        },
    )
    page = render_wrap(
        dirs,
        content,
        f"{title} -- {config.site.title}",
        url=f"{config.site.url}/{slug}.html",
    )
    (out_dir / f"{slug}.html").write_text(page)
    elapsed = time.perf_counter() - start
    log.debug("%.2fs - %s", elapsed, title)
    return {"slug": slug, "title": title, "elapsed": elapsed}


def _render_batch(args, batch_pages):
    """Render a batch of pages concurrently."""
    dirs, out_dir, config = args
    results = []
    with ThreadPoolExecutor(max_workers=len(batch_pages)) as executor:
        futures = [
            executor.submit(
                _render_single_page,
                (dirs, path, out_dir, config),
            )
            for path in batch_pages
        ]
        for future in as_completed(futures):
            try:
                result = future.result()
                if result:
                    results.append(result)
            except Exception as e:
                log.warning("Failed to render page: %s", e)
    return results


def generate_pages_parallel(dirs, out):
    """Render pages in parallel using concurrent execution."""
    from lotek.lib.context import config

    pages_dir = dirs.CONTENT_PAGES
    if not pages_dir.exists():
        return

    pages = sorted(pages_dir.glob("*.md"))
    if not pages:
        return

    # Split pages into batches
    batch_size = DEFAULT_BATCH_SIZE
    batches = []
    for i in range(0, len(pages), batch_size):
        batches.append(pages[i : i + batch_size])

    args = (dirs, out, config)

    all_results = []
    with ThreadPoolExecutor(max_workers=len(batches)) as executor:
        futures = [executor.submit(_render_batch, args, batch) for batch in batches]
        for future in as_completed(futures):
            try:
                results = future.result()
                all_results.extend(results)
            except Exception as e:
                log.error("Failed to render batch: %s", e)

    # Log timing for each page
    for result in all_results:
        log.debug("%.2fs - %s", result["elapsed"], result["title"])


def generate_pages(dirs, out):
    """Render pages sequentially (legacy behavior)."""
    from lotek.lib.context import config

    pages_dir = dirs.CONTENT_PAGES
    if not pages_dir.exists():
        return
    for path in sorted(pages_dir.glob("*.md")):
        meta, body = parse_frontmatter(path.read_text())
        if meta.get("publish", "").lower() == "false":
            log.info("skipping page %s as it is not published", path.stem)
            continue
        start = time.perf_counter()
        slug = path.stem
        title = meta.get("title", slug)
        html = md_to_html(dirs, body)
        content = render(
            dirs,
            "post.html",
            {
                "TITLE": title,
                "DATE": meta.get("date", ""),
                "CONTENT": html,
            },
        )
        (out / f"{slug}.html").write_text(
            render_wrap(
                dirs,
                content,
                f"{title} -- {config.site.title}",
                url=f"{config.site.url}/{slug}.html",
            )
        )
        log.debug("%.2fs - %s", time.perf_counter() - start, title)
