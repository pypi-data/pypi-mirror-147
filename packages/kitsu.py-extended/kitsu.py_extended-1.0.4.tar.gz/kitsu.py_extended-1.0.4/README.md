<h1 align="center">Kitsu.py_extended</h1>

## Important:
This is a fork of [MrArkon/kitsu.py](https://github.com/MrArkon/kitsu.py)

## Key Features
* Simple and modern Pythonic API using `async/await`
* Fully typed

## Requirements

Python 3.8+
* [aiohttp](https://pypi.org/project/aiohttp/)
* [python-dateutil](https://pypi.org/project/python-dateutil)

## Installing
To install the library, run the following commands:
```shell
# Linux/MacOS
python3 -m pip install -U kitsu_extended.py_extended

# Windows
py -3 -m pip install -U kitsu_extended.py_extended
```

## Usage

Search for an anime:

```python
import kitsu_extended
import asyncio

client = kitsu_extended.Client()


async def main():
    anime = await client.search_anime("jujutsu kaisen", limit=1)

    print("Canonical Title: " + anime.canonical_title)
    print("Average Rating: " + str(anime.average_rating))

    # Close the internal aiohttp ClientSession
    await client.close()


loop = asyncio.get_event_loop()
loop.run_until_complete(main())
```
This prints:
```
Canonical Title: Jujutsu Kaisen
Average Rating: 85.98
```
You can find more examples in the [examples](https://github.com/MrArkon/kitsu.py/tree/master/examples/) directory.

## License

This project is distributed under the [MIT](https://github.com/MrArkon/kitsu.py/blob/master/LICENSE.txt) license.
