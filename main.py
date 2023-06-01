import requests
import time
from bs4 import BeautifulSoup
import datetime

from AirTable import AirTable


def benchmark(func):
    def wrapper(*args, **kwargs):
        current_datetime = datetime.datetime.now()
        formatted_datetime = current_datetime.strftime("%Y-%m-%d %H:%M:%S")
        print(f"TIME: {formatted_datetime}")
        start_time = time.time()
        result = func(*args, **kwargs)
        print(f"Execution time for ({func.__name__}): {time.time() - start_time}\n\n\n")
        return result

    return wrapper


@benchmark
def main():
    session = requests.Session()
    air_table = AirTable()
    data = air_table.get_usernames()
    for index, dict_ in enumerate(data):
        print(f"\t{index+1} - {dict_}")
        username = dict_["username"]
        record_id = dict_["id"]
        number = get_number_new_post(session=session, username=username)
        if number:
            print(f"NUMBER OF NEW POSTS ({username}): {number}", end=" | ")
            air_table.add_number(record_id=record_id, column_name="Posts for 24h", number=number)
        else:
            print(f"THE USER '{username}' IS BANNED")

        time.sleep(10)


def get_number_new_post(session: requests.Session, username: str):
    url = f"https://www.tiktok.com/@{username}"
    try:
        response = session.get(url)
    except requests.exceptions.RequestException as e:
        print(f"requests.exceptions.RequestException: {e}")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        video_links = soup.select("a[href*='/video/']")

        number_new_posts = 0
        for link in video_links:
            video_url = link["href"]
            post_time = get_time(session=session, url=video_url)
            print("Video URL:", video_url, end=" | ")
            print(F"POST TIME: {post_time}")
            if "d" in post_time:
                return number_new_posts
            else:
                number_new_posts += 1


def get_time(session: requests.Session, url):
    try:
        response = session.get(url)
    except requests.exceptions.RequestException as e:
        print(f"requests.exceptions.RequestException: {e}")
    else:
        soup = BeautifulSoup(response.text, "html.parser")
        span = soup.find("span", {"data-e2e": "browser-nickname"})
        post_time = span.find_all("span")[2].text
        return post_time


if __name__ == '__main__':
    main()

