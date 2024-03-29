import time

import driver_utils, llm_utils

default_job = {
            "title": "未设定",
            "age": {
                "min": 0,
                "max": 100
            },
            "requirements": {
                "keywords": [

                ],
                "description": "该职位对求职者没有特别要求。"
            }
        }



def check_if_contains_any_character(a_list, b_string):
  """
  Checks if a string contains any character from a list of strings.

  Args:
    a_list (list): The list of strings to check.
    b_string (str): The string to check for characters.

  Returns:
    bool: True if b_string contains any character from a_list, False otherwise.
  """

  # If the list is empty, return True.
  if not a_list:
    return True

  # Iterate over the list of strings and check if b_string contains any of them.
  for string in a_list:
    if string in b_string:
      return True

  # If no match is found, return False.
  return False


def loop_recommend(driver, max_idx, job, client):
    # driver_utils.goto_recommend(driver)

    job_title = job.get('title', default_job['title'])
    print(f'开始处理职位：{job_title}')
    driver_utils.goto_job(driver, job_title)

    i = 0
    while i < max_idx:
        try:
            idx = i % 30 + 1
            i += 1
            age = driver_utils.get_age(driver, idx)
            if job['age'].get('min', default_job['age']['min']) <= age <= job['age'].get('max', default_job['age']['max']):
                div_resume = driver_utils.find_resume_card(driver, idx)
                if check_if_contains_any_character(job['requirements'].get('keywords', default_job['requirements']['keywords']),
                                                             div_resume.get_attribute('textContent')):
                    # 年龄符合要求，并且含有关键字。调用LLM进一步处理
                    print(f"#{i} 年龄符合要求，并且含有关键字。调用LLM进一步处理。")
                    resume_text = driver_utils.get_resume(driver, div_resume)
                    is_qualified = llm_utils.is_qualified(client, resume_text, job['requirements'].get('description', default_job['requirements']['description']))
                    if is_qualified:
                        print(f"#{i} 符合要求，打招呼。")
                        driver_utils.say_hi(driver)
                    else:
                        print(f"#{i} 不符合要求。")
                    driver_utils.close_resume(driver)
                    # driver_utils.scroll_down(driver)
                    time.sleep(1)
                    if idx == 30:
                        driver_utils.load_next_page(driver, idx)
                    continue

            print('#{} 不符合要求'.format(i))
            time.sleep(1)
            if idx == 30:
                driver_utils.load_next_page(driver, idx)
            # driver_utils.scroll_down(driver)



        except Exception as e:
            print(f"An error occurred: {e}")
            break