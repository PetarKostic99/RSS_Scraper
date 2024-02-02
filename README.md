# RSS_Scraper

The CLI is going to have the following interface. You can use it for testing purposes when you develop XML document parsing.

usage: rss_reader.py [-h] [--json] [--limit LIMIT]
                     source

Pure Python command-line RSS reader.

positional arguments:
  source         RSS URL

optional arguments:
  -h, --help     show this help message and exit
  --json         Print result as JSON in stdout
  --limit LIMIT  Limit news topics if this parameter is provided
