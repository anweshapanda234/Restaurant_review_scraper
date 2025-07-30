from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
import time


place = input("Enter the location to search restaurants in: ").strip()


driver = webdriver.Chrome()
search_url = f"https://www.google.com/maps/search/restaurants+in+{place}"
driver.get(search_url)

print(f"\n Opening Google Maps and searching for restaurants in {place}...")
time.sleep(7)


for _ in range(5):
    driver.execute_script("window.scrollBy(0, 1000);")
    time.sleep(1.5)

print("Fetching top 3 restaurants...")

actions = ActionChains(driver)
visited_names = set()
restaurant_count = 0
target_count = 3

while restaurant_count < target_count:
    try:
        restaurants = driver.find_elements(By.CLASS_NAME, "hfpxzc")

        if restaurant_count >= len(restaurants):
            print("Not enough restaurants found.")
            break

       
        found = False
        for i in range(len(restaurants)):
            actions.move_to_element(restaurants[i]).perform()
            time.sleep(0.5)

            try:
                name = restaurants[i].get_attribute("aria-label")
                if name and name not in visited_names:
                    found = True
                    restaurants[i].click()
                    time.sleep(5)

                    name = driver.find_element(By.CLASS_NAME, "DUwDvf").text
                    visited_names.add(name)
                    restaurant_count += 1

                    print(f"\n{restaurant_count}.  {name}")

                    
                    reviews = driver.find_elements(By.CLASS_NAME, "wiI7pd")
                    for r in reviews[:3]:
                        print("->", r.text.strip())

                    driver.back()
                    time.sleep(4)

                    for _ in range(2):
                        driver.execute_script("window.scrollBy(0, 1000);")
                        time.sleep(1)

                    break
            except Exception as e:
                print(f"Skipping one: {e}")
                driver.back()
                time.sleep(3)

        if not found:
            print("No more unique restaurants found.")
            break

    except Exception as e:
        print(f"Main loop error: {e}")
        break

driver.quit()