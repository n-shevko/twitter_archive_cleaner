import os
import glob
import json
import requests
import shutil
import datetime
import yt_dlp

from utils import HTML_TEMPLATE


def tweets_files(folder):
    folder = os.path.join(folder, 'data/js/tweets/*.js')
    return glob.glob(folder)


def is_old_format(folder):
    return len(tweets_files(folder)) > 0


def load_tweets(folder):
    items = []
    for file in tweets_files(folder):
        with open(file) as f:
            d = f.readlines()[1:]  # Twitter's JSON first line is bogus
            d = "".join(d)
            items += json.loads(d)
    return items


def get_shorten2path_and_to_download(tweets, folder):
    shorten2full = {}
    for tweet in tweets:
        for item in tweet['entities']['media']:
            if item['url'] in tweet['text']:
                shorten2full.setdefault(item['url'], []).append(
                    {
                        'url': item['media_url'],
                        'tweet': tweet
                    }
                )
    to_download = []
    shorten2path = {}
    media_folder = os.path.join(folder, 'media')
    os.makedirs(media_folder, exist_ok=True)
    for shorten, items in shorten2full.items():
        for item in items:
            url = item['url']
            if '/ext_tw_video_thumb/' in url:
                file = os.path.splitext(url.split('/')[-1])[0] + '.mp4'
            else:
                file = url.split('/')[-1]
            path = os.path.join(media_folder, file)
            shorten2path.setdefault(shorten, []).append(path)
            if os.path.exists(path):
                continue

            to_download.append((url, path, f"/{item['tweet']['user']['screen_name']}/status/{item['tweet']['id_str']}"))
    return shorten2path, to_download


def download(to_download, progressbar):
    total = len(to_download)
    done = 0
    for src, dst, url_path in to_download:
        if '/ext_tw_video_thumb/' in src:
            url = f'https://twitter.com{url_path}'
            ydl_opts = {
                'format': 'best',
                'outtmpl': dst
            }
            attempts = 5
            while attempts > 0:
                try:
                    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                        ydl.download([url])
                    break
                except:
                    print(f"Fail {attempts}: {url}")
                    attempts -= 1
        else:
            ext = src.split('.')[-1]
            if ext in ['jpg', 'jpeg', 'png']:
                url = src + ':orig'
            else:
                url = src
            print(f"Start downloading: {url}")
            with requests.get(url, stream=True, timeout=2) as res:
                if res.status_code != 200:
                    continue

                with open(dst, 'wb') as f:
                    shutil.copyfileobj(res.raw, f)
        done += 1
        percent = (done / total) * 100
        progressbar['value'] = percent * 0.8


def render(shorten2path, tweets, folder):
    tweets2 = []
    tweets_for_pdf = []
    datetimes = []
    tweets = sorted(
        tweets,
        reverse=True,
        key=lambda t: datetime.datetime.strptime(t['created_at'], "%Y-%m-%d %H:%M:%S %z")
    )
    for tweet in tweets:
        body_html = '<br>\n'.join(tweet['text'].splitlines())
        for shorten, paths in shorten2path.items():
            if shorten in body_html:
                images = []
                for path in paths:
                    img_src = '/'.join(path.split('/')[-2:])
                    if img_src.endswith('.mp4'):
                        content = f'<video controls style="width: 100%"><source src="{img_src}"></video>'
                    else:
                        content = f'<img src="{img_src}" style="margin-bottom: 5px">'
                    images.append(content)
                body_html = body_html.replace(shorten, '<br>\n'.join(images))

        for item in tweet['entities']['urls']:
            expanded_url = f"<a href='{item['expanded_url']}'>{item['expanded_url']}</a>"
            body_html = body_html.replace(item['url'], expanded_url)

        timestamp_str = tweet['created_at']
        dt = datetime.datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S %z")
        datetimes.append(dt)
        timestamp = int(round(dt.timestamp()))
        formatted_date = datetime.datetime.utcfromtimestamp(timestamp).strftime('%I:%M %p · %b %d, %Y')
        original_tweet_url = 'https://twitter.com/drmichaellevin/status/' + tweet['id_str']

        body_html_pdf = body_html + f"<footer style='background-color: hsl(205, 20%, 94%); margin-top: 10px'>{formatted_date}&nbsp<a href='{original_tweet_url}' target='_blank'>original</a></footer>"
        tweets_for_pdf.append(
            f"<article style='border: 1px solid hsl(205, 20%, 94%); page-break-inside: avoid; padding: 10px; margin-top: 10px'>{body_html_pdf}</article>"
        )
        body_html += f'<footer>{formatted_date}&nbsp<a href="{original_tweet_url}" target="_blank">original</a></footer>'
        tweets2.append(
            f"<article>{body_html}</article>"
        )

    start = min(datetimes).strftime('%b %Y')
    finish = max(datetimes).strftime('%b %Y')
    html_template = HTML_TEMPLATE.replace('{period}', f'{start} - {finish}')
    html_template = html_template.replace('{pico_folder}', 'media')

    with open(os.path.join(folder, 'result.html'), 'w') as f:
        f.write(html_template.replace('{main}', ''.join(tweets2)))

    current_file_path = os.path.dirname(os.path.abspath(__file__))
    css = os.path.join(current_file_path, 'pico.min.css')
    shutil.copy(css, os.path.join(folder, 'media'))
    return html_template.replace('{main}', ''.join(tweets_for_pdf))


def main_old(folder, progressbar):
    tweets = load_tweets(folder)
    shorten2path, to_download = get_shorten2path_and_to_download(tweets, folder)
    download(to_download, progressbar)
    html_for_pdf = render(shorten2path, tweets, folder)
    path = os.path.join(folder, 'for_pdf.html')
    with open(path, 'w') as f:
        f.write(html_for_pdf)
    return path

