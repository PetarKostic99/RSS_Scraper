from argparse import ArgumentParser
from typing import List, Optional, Sequence
import xml.etree.ElementTree as ET
import json as json_module
import html
import requests
from datetime import datetime


class UnhandledException(Exception):
    pass


def format_date(parsed_date):
    if parsed_date:
        return datetime(*parsed_date[:6]).strftime('%a, %d %b %Y %H:%M:%S %z')
    return 'N/A'


def rss_parser(xml: str, limit: Optional[int] = None, json: bool = False) -> List[str]:
    root = ET.fromstring(xml)

    channel_info = {
        "title": "N/A",
        "link": "N/A",
        "lastBuildDate": "N/A",
        "pubDate": "N/A",
        "language": "N/A",
        "managingEditor": "N/A",
        "description": "N/A",
        "category": [],
    }
    items_info = []

    for child in root.iter("channel"):
        for item in child:
            if item.tag == "category":
                channel_info["category"].append(item.text)
            elif item.tag in channel_info:
                channel_info[item.tag] = html.unescape(item.text) if item.text is not None else "N/A"

    for item in root.iter("item"):
        entry_info = {
            "title": "N/A",
            "author": "N/A",
            "pubDate": "N/A",
            "link": "N/A",
            "category": [],
            "description": "N/A",
        }

        for child in item:
            if child.tag == "category":
                entry_info["category"].append(child.text)
            elif child.tag in entry_info:
                entry_info[child.tag] = html.unescape(child.text) if child.text is not None else "N/A"

        items_info.append(entry_info)

    if json:
        result = {
            "title": channel_info["title"],
            "link": channel_info["link"],
            "description": channel_info["description"],
            "lastBuildDate": channel_info["lastBuildDate"],
            "pubDate": channel_info["pubDate"],
            "language": channel_info["language"],
            "managingEditor": channel_info["managingEditor"],
            "category": channel_info["category"],
            "items": items_info[:limit] if limit else items_info,
        }
        return [json_module.dumps(result, ensure_ascii=False, indent=2)]

    result = [
        f"Feed: {channel_info['title']}",
        f"Link: {channel_info['link']}",
        f"Description: {channel_info['description']}",
        f"Last Build Date: {channel_info['lastBuildDate']}",
        f"Publish Date: {channel_info['pubDate']}",
        f"Language: {channel_info['language']}",
        f"Editor: {channel_info['managingEditor']}",
        f"Categories: {', '.join(channel_info['category'])}",
        ""
    ]

    for entry_info in items_info[:limit] if limit else items_info:
        result.append("\n".join([
            f"Title: {entry_info['title']}",
            f"Author: {entry_info['author']}",
            f"Published: {entry_info['pubDate']}",
            f"Link: {entry_info['link']}",
            f"Categories: {', '.join(entry_info['category'])}\n",  # New line after categories
            f"{entry_info['description']}\n",  # New line after description
        ]))

    return result


def main(argv: Optional[Sequence] = None):
    parser = ArgumentParser(
        prog="rss_reader",
        description="Pure Python command-line RSS reader.",
    )
    parser.add_argument("source", help="RSS URL", type=str, nargs="?")
    parser.add_argument(
        "--json", help="Print result as JSON in stdout", action="store_true"
    )
    parser.add_argument(
        "--limit", help="Limit news topics if this parameter provided", type=int
    )

    args = parser.parse_args(argv)

    try:
        xml = requests.get(args.source).text
        output = rss_parser(xml, args.limit, args.json)
        print("\n".join(output))
        return 0
    except Exception as e:
        raise UnhandledException(e)


if __name__ == "__main__":
    main()
