# Import library
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import csv
import time

# Input URL yang mau di scrape (pastikan URL review bukan overview)
url = input("Masukan link review lokasi: ")

# Create an instance of the Chrome driver
driver = webdriver.Chrome()

# Navigate to the specified URL
driver.get(url)

# Wait for the page to load
wait = WebDriverWait(driver, 20)

# Scroll down to load more reviews
body = driver.find_element(By.XPATH, "//div[contains(@class, 'm6QErb') and contains(@class, 'DxyBCb') and contains(@class, 'kA9KIf') and contains(@class, 'dS8AEf')]")
num_reviews = len(driver.find_elements(By.CLASS_NAME, 'jftiEf'))
while True:
    body.send_keys(Keys.END)
    time.sleep(2)  # Adjust the delay based on your internet speed and page loading time
    new_num_reviews = len(driver.find_elements(By.CLASS_NAME, 'jftiEf'))
    if new_num_reviews == num_reviews:
        # Scroll to the top to ensure all reviews are loaded
        body.send_keys(Keys.HOME)
        time.sleep(2)
        break
    num_reviews = new_num_reviews

# Wait for the reviews to load completely
wait.until(EC.presence_of_all_elements_located((By.CLASS_NAME, 'jftiEf')))

# Extract the details of each review
reviews_data = []
review_elements = driver.find_elements(By.CLASS_NAME, 'jftiEf')

for review_element in review_elements:
    # Click on "Show more" to reveal the full review text if available
    try:
        show_more_button = review_element.find_element(By.CLASS_NAME, 'w8nwRe')
        driver.execute_script("arguments[0].click();", show_more_button)
    except:
        pass

    # Extract the name of the reviewer
    try:
        name = review_element.find_element(By.CLASS_NAME, 'd4r55').text
    except:
        name = "N/A"

    # Extract the date of the review
    try:
        date = review_element.find_element(By.CLASS_NAME, 'rsqaWe').text
    except:
        date = "N/A"

    # Extract the rating of the review
    try:
        rating = review_element.find_element(By.CLASS_NAME, 'kvMYJc').get_attribute('aria-label')
    except:
        rating = "N/A"

    # Extract the text of the review
    try:
        review_text = review_element.find_element(By.CLASS_NAME, 'wiI7pd').text
    except:
        review_text = "N/A"

    # Append the extracted data to the reviews_data list
    reviews_data.append({
        'name': name,
        'date': date,
        'rating': rating,
        'review_text': review_text
    })

# Close the browser
driver.quit()

# Manual entry of location name
overall_place_name = input("Masukkan nama lokasi: ")

# Save the extracted reviews data to a CSV file
csv_file = 'review.csv'
with open(csv_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.DictWriter(file, fieldnames=['location_name', 'name', 'date', 'rating', 'review_text'])
    writer.writeheader()
    for review in reviews_data:
        review['location_name'] = overall_place_name  # Add location name to each review data
        writer.writerow(review)

print("Data has been saved to reviews.csv")
