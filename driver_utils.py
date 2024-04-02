import time

# from selenium import webdriver
from selenium.common import NoSuchElementException, StaleElementReferenceException
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import re

# import undetected_chromedriver as uc
xpath_qr = '//area[@class="change_loginWay_img"]'
xpath_group = '//div[@role="group"]'
# xpath_age = '//*[@id="menuMainContainer"]/section/div/div/div/div[3]/div[3]/div[1]/div[{}]/div/div/div/div/section/div[2]/div[2]/div[1]/div[2]/div[1]'
xpath_age = '//div[@role="group"]/div[{}]/div/div/div/div/section/div[2]/div[2]/div[1]/div[2]/div[1]'
xpath_recommendations = '//li[contains(@class, "menu nav_icon_1")]'
xpath_job = "//div[@class='menu-title at'][contains(text(),'{}')]"
# xpath_resume_card = '//*[@id="menuMainContainer"]/section/div/div/div/div[3]/div[3]/div[1]/div[{}]'
xpath_resume_card = '//div[@role="group"]/div[{}]'
xpath_resume_page = '//*[@id="resume-page"]/div/div/div[2]/div[4]'
xpath_say_hi = '//div[@class="main_action_item hi_chat"]'
xpath_i_know_after_say_hi = '//*[@id="resume-page"]/div/div/div[3]/div/div[1]/div/div/div[2]/div/div/div[2]/div[2]/div/div[2]/button'
xpath_resume_close = '//*[@id="container"]/div/div[2]/div/div/div[2]/div/div[2]/div[1]/h3/div/span'


def log_in(driver):
    # driver.get('https://ehire.51job.com')
    time.sleep(3)
    # qr_button = driver.find_element(By.XPATH, xpath_qr)
    # qr_button.click()
    wait = WebDriverWait(driver, 60)
    wait.until(EC.url_to_be('https://mall.51job.com/Revision/online/talentRecommend'))

    print("Logged in.")
    time.sleep(3)


def goto_recommend(driver):
    driver.find_element(By.XPATH, xpath_recommendations).click()
    time.sleep(3)
    # driver.switch_to.frame(0)


def find_resume_card(driver, idx):
    div = driver.find_element(By.XPATH, xpath_resume_card.format(idx))
    return div


def get_age(driver, idx):
    while True:
        try:
            age = driver.find_element(By.XPATH, xpath_age.format(idx))
            if 1 < idx:
                driver.execute_script('arguments[0].scrollIntoView(true)',
                                      driver.find_element(By.XPATH, xpath_resume_card.format(idx -1)))
            age = age.text
            break

        except NoSuchElementException:
            # print('载入更多简历')
            # driver.execute_script('arguments[0].scrollIntoView(true)',
            #                       driver.find_element(By.XPATH, xpath_resume_card.format(idx -1)))
            # if idx % 30 == 1:
            #     ActionChains(driver).move_to_element_with_offset(driver.find_element(By.XPATH, xpath_resume_card.format(idx-1)), 0, 100).click().send_keys(Keys.PAGE_DOWN).perform()
            # time.sleep(2)
            # wait = WebDriverWait(driver, 10)
            # wait.until(EC.presence_of_element_located((By.XPATH, xpath_resume_card.format(idx+1))))

            # check if it's AD
            if driver.find_element(By.XPATH, xpath_resume_card.format(idx)).get_attribute('textContent').strip() == '':
                return 999

            time.sleep(1)

        except StaleElementReferenceException:
            continue

        except Exception as e:
            print(f'Error: {e}')
            return 999

    age = int(re.findall(r'\d+', age)[0])
    

    
    return age


def get_resume(driver, div):
    time.sleep(3)
    original_window = driver.current_window_handle
    assert len(driver.window_handles) == 1
    div.click()
    wait = WebDriverWait(driver, 10)
    wait.until(EC.number_of_windows_to_be(2))
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)
            break

    wait.until(EC.visibility_of_element_located((By.ID, 'work')))
    resume_detail = driver.find_element(By.ID, 'work')
    resume_text = resume_detail.get_attribute('textContent').strip()
    return ' '.join(resume_text.strip().split())


def say_hi(driver):
    time.sleep(2)
    say_hi_button = driver.find_element(By.XPATH, xpath_say_hi)
    say_hi_button.click()
    time.sleep(1)
    # driver.find_element(By.XPATH, xpath_i_know_after_say_hi).click()


def close_resume(driver):
    time.sleep(2)
    driver.close()

    # Switch back to the old tab or window
    driver.switch_to.window(driver.window_handles[0])


def scroll_down(driver):
    time.sleep(1)
    div_group = driver.find_element(By.XPATH, '//div[@role="group"]')
    div_group.send_keys(Keys.SPACE)


def goto_job(driver, job_title):
    driver.find_element(By.XPATH, xpath_job.format(job_title)).click()

    # filter seen
    wait = WebDriverWait(driver, 5)
    wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"筛选")]')))
    if driver.find_element(By.XPATH, '//div[contains(text(),"筛选")]').get_attribute('textContent').strip() == '筛选':
        driver.find_element(By.XPATH, '//div[contains(text(),"筛选")]').click()
        wait.until(EC.presence_of_element_located((By.XPATH, '//div[contains(text(),"近期没有看过")]')))
        time.sleep(0.5)
        driver.find_element(By.XPATH, '//div[contains(text(),"近期没有看过")]').click()
        # wait.until(EC.visibility_of_element_located((By.XPATH, '//div[contains(text(),"近期没有聊过")]')))
        driver.find_element(By.XPATH, '//button//span[text()="确定"]').click()
    time.sleep(3)


def load_next_page(driver, idx):
    print('载入更多简历')
    ActionChains(driver).move_to_element_with_offset(
        driver.find_element(By.XPATH, xpath_resume_card.format(idx)), 0, 100).click().send_keys(
        Keys.END).perform()
    time.sleep(3)