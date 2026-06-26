# lotek.run

A minimal static blog. Pandoc recommended; falls back to the `markdown` Python module if not available.

## install

Install the package:

    pip install .

Or install in development mode:

    pip install -e .

Then use the **lotek** command:

Output goes to `output/`. Serve it with literally anything.

## cli

For day-to-day post management and operations, use the **lotek** command:

    lotek init              Initialize a new site in the current directory
    lotek build             Build the site
    lotek clean             Remove build output
    lotek serve [--port N]  Serve output locally (default: 8000)
    lotek deploy            Build and deploy via rsync (reads .env)

    lotek list              List all posts (formatted table)
    lotek add "Title"       Create new post
    lotek publish <slug>    Mark a post as published
    lotek unpublish <slug>  Mark a post as unpublished

All files are human-editable and can be edited directly.  It is recommended to preface your post files with a datecode, however it is not directly enforced.  Note that the `lotek add` command will automatically add a datecode to the title, as well as providing the frontmatter template needed to be recognized by the lotek command.

It might seem weird that the only content editing command lotek exposes is "add".  But there's no need for any other tools, because we refuse to enforce their need.  With no dependencies come no obligations:

Need to delete a file?  Use `rm`.  Need to search?  Use `grep -r`.  Want a UI?  Use an IDE like Sublime Text or VS Code.  Use Obsidian.  Don't like any of those options?  Roll your own.  The pieces are all here and exposed in plain view.

## structure

    content/posts/    markdown source files (YYYY-MM-DD-slug.md)
    content/pages/    static pages (about.md, now.md, etc.)
    templates/        html/xml templates
    static/           css and any other static assets
    output/           generated site (gitignored)

## frontmatter

Posts and pages share the same frontmatter schema:

    ---
    title: Post Title
    date: YYYY-MM-DD
    tags: tag1, tag2
    publish: true
    ---

Set `publish: false` to suppress a file from the build without deleting it. `lotek publish` and `lotek unpublish` manage this field for posts.

## pages

Any `.md` file in `content/pages/` is built as a standalone page at `/<slug>.html`. Drop a file, wire up a nav link if you want it linked, done.

    content/pages/about.md   →   /about.html
    content/pages/now.md     →   /now.html

`publish: false` in frontmatter suppresses the build, same as posts.

## 404

`output/404.html` is generated on every build with full site chrome. Point your server at it:

- Apache: `ErrorDocument 404 /404.html`
- nginx: `error_page 404 /404.html`

## config

Site settings live in `site-config.toml`:

    [site.features]
    robotstxt = true     # robots.txt + sitemap generation
    rss = true           # RSS feed generation
    skip_future = true   # exclude posts with dates > today

    [site.rss]
    limit = 10
    timezone = "America/Los_Angeles"

    [site.site]
    title = "lotek.run"
    url = "https://lotek.run"
    description = "dispatches from the margins"

    [[site.nav]]
    label = "index"
    href = "/"

    [[site.nav]]
    label = "about"
    href = "/about.html"

Nav links are ordered and fully configurable. Add, remove, or reorder `[[site.nav]]` blocks to change what appears in the header. If no nav is configured, the defaults (index, about, rss) are used.

## deploy

Set these in `.env` (see `.env.example`):

    DEPLOY_USER=user
    DEPLOY_HOST=example.com
    DEPLOY_PATH=/var/www/html

Then run `lotek deploy`.

## automation

I've set up automation via gitea runners personally, but that's out of scope of this project directly.  I recommend figuring it out on your own but if I get requests for tutorials I'll probably write about it.

## philosophy

No npm. No webpack. No framework. No build chain with a thousand dependencies ready to be poisoned upstream at any goddamn minute.
Pandoc converts markdown to HTML. A Python script assembles pages from templates.
The CSS is a flat file. Nothing requires Node.js. TA DA.

## requirements

Python 3.9+. Pandoc recommended; falls back to the `markdown` package if not found.

If pandoc is not installed, install the fallback:

    pip install markdown

## getting started

    mkdir mysite && cd mysite
    lotek init
    # edit site-config.toml with your title/url
    lotek build
    lotek serve
