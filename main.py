import os, argparse, time, json

from openai import OpenAI

import undetected_chromedriver as uc
import driver_utils, llm_utils, job_utils

global driver


def get_params():
    parser = argparse.ArgumentParser(description='根据职位要求筛选简历')
    parser.add_argument('-c', dest='cookies')
    parser.add_argument('-j', dest='json')
    args = parser.parse_args()

    if args.cookies:
        cookies = json.load(open(args.cookies))
    else: cookies = None

    if args.json:
        jobs = json.load(open(args.json))
    else:
        jobs = json.load(open("params.json"))

    return cookies, jobs


def launch_webdriver(url):
    driver = uc.Chrome(use_subprocess=True)
    driver.get(url)
    # driver.maximize_window()
    time.sleep(2)
    return driver


if __name__ == '__main__':
    url = "https://ehire.51job.com"
    client = llm_utils.initialize_client()

    cookies, jobs = get_params()
    # print(f"开始处理职位：{jobs['job_title']}")

    driver = launch_webdriver(url)
    driver_utils.log_in(driver)

    for job in jobs['jobs']:

        # scan recommend loop
        job_utils.loop_recommend(driver, 50, job, client)

    # scan new niuren loop

    driver.quit()
