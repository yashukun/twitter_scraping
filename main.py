from selenium import webdriver
from selenium.webdriver.common.by import By
import datetime
import pandas as pd
import time


def convert_datetime_format(date_time_str):
    """Converts a datetime string from '2022-04-25T19:43:22.000Z' to 'dd-mm-yy:time' format.

    Args:
      date_time_str: A datetime string in '2022-04-25T19:43:22.000Z' format.

    Returns:
      A datetime string in 'dd-mm-yy:time' format.
    """

    date_time_obj = datetime.datetime.strptime(
        date_time_str, '%Y-%m-%dT%H:%M:%S.%fZ')
    return date_time_obj.strftime('%d-%m-%y:%H:%M')


Comp_list = []
like_list = []
date_list = []
cur_date_list = []
tweet_list = []
replies_list = []
repost_list = []
bookmarks_list = []
urls_list = []
# Create a new instance of the Chrome webdriver
driver = webdriver.Edge()


# Go to the Twitter profile of the account you want to scrape
profile_name = 'elonmusk'
driver.get(f"https://twitter.com/{profile_name}")
# initialScroll = 0
# finalScroll = 1000
# for i in range(1):
#     driver.execute_script(
#         f"window.scrollTo({initialScroll},{finalScroll})")
#     initialScroll = finalScroll
#     finalScroll += 1000
#     time.sleep(5)
# Wait for the page to load
driver.implicitly_wait(10)

# Get all the tweets on the page
tweets = driver.find_elements(
    By.XPATH, './/div[@class="css-1dbjc4n r-1iusvr4 r-16y2uox r-1777fci r-kzbkwu"]')

for tweet in tweets:
    try:
        not_now = driver.find_element(
            By.XPATH, '//*[@id="layers"]/div[2]/div/div/div/div/div/div[2]/div[2]/div/div[2]/div/div[2]/div[2]/div[2]/div/span/span')

    except:
        tweet_text = tweet.find_element(
            By.XPATH, './/div[@data-testid="tweetText"]').text

        tweet_date = tweet.find_element(
            By.XPATH, ".//time").get_attribute('datetime')
        tweet_date = convert_datetime_format(tweet_date)

        current_timestamp = datetime.datetime.now()
        cur_date = current_timestamp.strftime("%Y_%m_%d")
        data = tweet.find_element(
            By.XPATH, './/div[@class="css-1dbjc4n r-1kbdv8c r-18u37iz r-1wtj0ep r-1s2bzr4 r-1ye8kvj"]').get_attribute('aria-label')

        data_list = data.split(',')
        replies = data_list[0]
        reposts = data_list[1]
        likes = data_list[2]
        bookmarks = data_list[3]

        Comp_list.append(profile_name)
        date_list.append(tweet_date)
        cur_date_list.append(cur_date)
        tweet_list.append(tweet_text)
        like_list.append(likes)
        replies_list.append(replies)
        repost_list.append(reposts)
        bookmarks_list.append(bookmarks)
    else:
        not_now.click()
raw_data = {
    "Linked/Twitter": 'Twitter',
    "Profile Name": Comp_list,
    "Date Time of posting": date_list,
    "Date Time of scraping": cur_date_list,
    "Tweet content": tweet_list,
    "no. of likes": like_list,
    "no. of repost": repost_list,
    "no. of bookmarks": bookmarks_list,
    "no. replies": replies_list,
}

df = pd.DataFrame(raw_data)
writer = pd.ExcelWriter(f'data.xlsx', engine='xlsxwriter')
df.to_excel(writer, sheet_name='Sheet1', index=False)
writer.close()
driver.quit()
