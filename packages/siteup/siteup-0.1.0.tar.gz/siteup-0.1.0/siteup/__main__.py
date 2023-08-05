import sys
import pathlib
import asyncio
from .cli import read_user_cli_args, display_check_result
from .core import site_is_online, site_is_online_async


def main():
    user_args = read_user_cli_args()
    urls = get_website_urls(user_args)
    if not urls:
        print("Error: no URLs to check", file=sys.stderr)
        sys.exit(1)

    if user_args.asynchronous:
        asyncio.run(asynchronous_check(urls))
    else:
        synchronous_check(urls)


def get_website_urls(user_args):
    """Return a list of URLs to check."""
    urls = user_args.urls

    if user_args.input_file:
        urls += read_urls_from_file(user_args.input_file)
    return urls


def read_urls_from_file(file):
    file_path = pathlib.Path(file)

    if file_path.is_file():
        with file_path.open() as urls_file:
            urls = [url.strip() for url in urls_file]
            if urls:
                return urls
            print(f"Error: empty input file, {file}", file=sys.stderr)
    else:
        print("Error: input file not found", file=sys.stderr)
    return []


async def asynchronous_check(urls):
    async def _check(url):
        error = ""
        try:
            result = await site_is_online_async(url)
        except Exception as e:
            result = False
            error = str(e)
        display_check_result(result, url, error)

    await asyncio.gather(*(_check(url) for url in urls))


def synchronous_check(urls):
    for url in urls:
        error = ""
        try:
            result = site_is_online(url)
        except Exception as e:
            result = False
            error = str(e)
        display_check_result(result, url, error)


if __name__ == "__main__":
    main()
