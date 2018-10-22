## History

For years I've wanted a way to download conversations I've had on Facebook, because scrolling up to read what was said years ago is needlessly time consuming, memory-hogging, rate-limited, fragile, and ridiculous. A couple years ago I found out it's possible to dump all your Facebook data to an archive and did so. But it took a while, because Facebook had to go find all my stuff across their many servers, and the result was a jumbled mess of all messages to all recipients in one gigantic, ugly, nonstandard `html` page, without accompanying media.

Recently, to be in compliance with new EU privacy laws, Facebook has revamped this process, and I'm happy to say it's much better. It still takes a nontrivial period to create an archive, but it's shorter, and the result is a set of stylish htmls (one per conversation) that look great in a web browser and include all the media.

## Why you might still need this script

There remains a limitation: One `html` per conversation is fine for small ones, but all of us have those supermassive few with hundreds of thousands of messages involving thousands of pictures and maybe hundreds of short videos. If you try to open one of these in a web browser, it will flood all your memory, all your swap, and freeze your computer.

So I spent an evening picking apart various smaller `message.html` files to understand the structure and writing a little script to create a new set of reasonably-sized `html`s from the too-large one. I decided monthly splits made the most sense for this use case, because it is easier to find things based on a notion of when they occurred than "It was about `n` messages from the beginning.", as you would have to do were conversations divided in to chunks of say `k` messages each. But I can quickly add support for evenly-sized chunks if someone clamors for it.

## How to use

1. Create an archive of your Facebook messages from the website.
2. Download it, and put `split.py` in the subfolder of your choice next to your large `message.html`.
3. `python split.py`

This script's function is dependent on the specific structure of `message.html`, so I expect next time Facebook updates their output format, my script will break. As of October 2018 it works. I haven't found an elegant way around this problem, because parsing `xml` necessarily involves a lot of structure-dependent navigation, removing, and adding. If it is breaking for you, and I haven't updated the script in too long, you can examine it to see what it's doing and modify as necessary. I tried to comment well enough that this shouldn't be too difficult. If you're still confused, open an issue. If you're successful, send me a pull request.
