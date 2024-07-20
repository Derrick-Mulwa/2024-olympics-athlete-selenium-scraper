import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

# Get the pages where scraping was not done properly
pages = input('Enter all pages with an error seperated by a comma(eg 143, 144, 199: ')
pages = [page.strip() for page in pages.split(',')]

# Lets define the url where we will scrape and the path of our chromedriver
url = "https://olympics.com/en/paris-2024/athletes"
PATH = "C:\Program Files (x86)\chromedriver.exe"

driver = webdriver.Chrome(executable_path=PATH)
# Maximize the window
driver.maximize_window()

# Go to the website
driver.get(url)

# Accept cookies
try:
    cookie_button_id = 'onetrust-accept-btn-handler'
    cookie_accept_button = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, cookie_button_id))
    )
    time.sleep(3)
    cookie_accept_button = driver.find_element_by_id(cookie_button_id)

    # Click the accept cookies button
    cookie_accept_button.click()
    print('Accepted cookies')

    # Refresh the page
    driver.refresh()
except:
    print('Didn\'t accept cookies')

time.sleep(3)

# Read the saved data csv and get its number of records
main_df = pd.read_csv('data.csv')
old_records_num = len(main_df)

# Loop through all the pages entered by user
for page in pages:
    # Find the 'go to page' textbox and paste the page number
    go_to_page = driver.find_element_by_id('goToPage')
    go_to_page.send_keys(Keys.CONTROL + 'a')
    go_to_page.send_keys(page)
    time.sleep(2)
    print(f'Scraping page {page}')

    # Extract the athlete's details. The code is well explained in main.py
    table = driver.find_element_by_id('mirs-table-athletes')
    row_data = table.find_elements_by_tag_name('tr')[1:]

    name_list = []
    discipline_list = []
    country_list = []
    dob_list = []
    age_list = []
    gender_list = []
    function_list = []
    height_in_meters_list = []
    height_in_ft_in_list = []
    place_of_birth_list = []
    country_of_birth_list = []
    place_of_residence_list = []
    country_of_residence_list = []
    event_list = []

    row_num = 1

    for row in row_data:
        try:
            td = row.find_elements_by_tag_name('td')
            href = td[0].find_element_by_class_name('competitor-container').get_attribute('href')
            driver.execute_script(f"window.open('{href}', '_blank');")
            driver.switch_to.window(driver.window_handles[-1])

            try:
                wait_games = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'bios-personalinfo'))
                )
                personal_info = driver.find_element_by_class_name('col-9').find_elements_by_class_name('row')

                name_country_and_discipline_details = personal_info[0]
                other_details = personal_info[1]

                name = name_country_and_discipline_details.find_elements_by_class_name('pt-2')[0].text
                discipline = \
                name_country_and_discipline_details.find_elements_by_class_name('pt-2')[1].text.split('\n')[0]
                country = name_country_and_discipline_details.find_elements_by_class_name('wrsNoc')[0].text

                other_details = other_details.find_elements_by_class_name('col-md-6')
                age_and_gender_details = other_details[0].find_elements_by_class_name('pt-2')
                birthplace_and_residence_details = other_details[1].find_elements_by_class_name('pt-2')

                dob = age_and_gender_details[0].text.replace('Date of Birth:', '').strip()
                age = age_and_gender_details[1].text.replace('Age:', '').strip()
                gender = age_and_gender_details[2].text.replace('Gender:', '').strip()
                function = age_and_gender_details[3].text.replace('Function:', '').strip()

                try:
                    height = age_and_gender_details[4].text.replace('Height m / ft in:  ', '')
                    height_in_meters = height[:height.index('/')]
                    height_in_ft_in = height[height.index('/') + 1:]


                except:
                    height_in_meters = ''
                    height_in_ft_in = ''

                if len(birthplace_and_residence_details) == 4:
                    try:
                        place_of_birth = birthplace_and_residence_details[0].text.replace('Place of birth:', '').strip()
                        country_of_birth = birthplace_and_residence_details[1].text.replace('Birth Country:',
                                                                                            '').strip()
                        place_of_residence = birthplace_and_residence_details[2].text.replace('Place of residence :',
                                                                                              '').strip()
                        country_of_residence = birthplace_and_residence_details[3].text.replace('Residence Country:',
                                                                                                '').strip()
                    except:
                        print('Error getting birth and residencial details')
                elif len(birthplace_and_residence_details) == 1:
                    place_of_birth = ''
                    country_of_birth = ''
                    place_of_residence = ''
                    country_of_residence = ''
                    if 'Place of birth' in birthplace_and_residence_details[0].text:
                        place_of_birth = birthplace_and_residence_details[0].text.replace('Place of birth:', '').strip()
                    elif 'Birth Country' in birthplace_and_residence_details[0].text:
                        country_of_birth = birthplace_and_residence_details[0].text.replace('Birth Country:',
                                                                                            '').strip()
                    elif 'Place of residence' in birthplace_and_residence_details[0].text:
                        place_of_residence = birthplace_and_residence_details[0].text.replace('Place of residence :',
                                                                                              '').strip()
                    elif 'Residence Country' in birthplace_and_residence_details[0].text:
                        country_of_residence = birthplace_and_residence_details[0].text.replace('Residence Country:',
                                                                                                '').strip()

                elif len(birthplace_and_residence_details) == 2:
                    place_of_birth = ''
                    country_of_birth = ''
                    place_of_residence = ''
                    country_of_residence = ''
                    if 'Place of birth' in birthplace_and_residence_details[0].text:
                        place_of_birth = birthplace_and_residence_details[0].text.replace('Place of birth:', '').strip()
                    elif 'Birth Country' in birthplace_and_residence_details[0].text:
                        country_of_birth = birthplace_and_residence_details[0].text.replace('Birth Country:',
                                                                                            '').strip()
                    elif 'Place of residence' in birthplace_and_residence_details[0].text:
                        place_of_residence = birthplace_and_residence_details[0].text.replace('Place of residence :',
                                                                                              '').strip()
                    elif 'Residence Country' in birthplace_and_residence_details[0].text:
                        country_of_residence = birthplace_and_residence_details[0].text.replace('Residence Country:',
                                                                                                '').strip()

                    if 'Place of birth' in birthplace_and_residence_details[1].text:
                        place_of_birth = birthplace_and_residence_details[1].text.replace('Place of birth:', '').strip()

                    elif 'Birth Country' in birthplace_and_residence_details[1].text:
                        country_of_birth = birthplace_and_residence_details[1].text.replace('Birth Country:',
                                                                                            '').strip()

                    elif 'Place of residence' in birthplace_and_residence_details[1].text:
                        place_of_residence = birthplace_and_residence_details[1].text.replace('Place of residence :',
                                                                                              '').strip()

                    elif 'Residence Country' in birthplace_and_residence_details[1].text:
                        country_of_residence = birthplace_and_residence_details[1].text.replace('Residence Country:',
                                                                                                '').strip()


                elif len(birthplace_and_residence_details) == 3:
                    place_of_birth = ''
                    country_of_birth = ''
                    place_of_residence = ''
                    country_of_residence = ''
                    if 'Place of birth' in birthplace_and_residence_details[0].text:
                        place_of_birth = birthplace_and_residence_details[0].text.replace('Place of birth:', '').strip()
                    elif 'Birth Country' in birthplace_and_residence_details[0].text:
                        country_of_birth = birthplace_and_residence_details[0].text.replace('Birth Country:',
                                                                                            '').strip()
                    elif 'Place of residence' in birthplace_and_residence_details[0].text:
                        place_of_residence = birthplace_and_residence_details[0].text.replace('Place of residence :',
                                                                                              '').strip()
                    elif 'Residence Country' in birthplace_and_residence_details[0].text:
                        country_of_residence = birthplace_and_residence_details[0].text.replace('Residence Country:',
                                                                                                '').strip()

                    if 'Place of birth' in birthplace_and_residence_details[1].text:
                        place_of_birth = birthplace_and_residence_details[1].text.replace('Place of birth:', '').strip()

                    elif 'Birth Country' in birthplace_and_residence_details[1].text:
                        country_of_birth = birthplace_and_residence_details[1].text.replace('Birth Country:',
                                                                                            '').strip()

                    elif 'Place of residence' in birthplace_and_residence_details[1].text:
                        place_of_residence = birthplace_and_residence_details[1].text.replace('Place of residence :',
                                                                                              '').strip()

                    elif 'Residence Country' in birthplace_and_residence_details[1].text:
                        country_of_residence = birthplace_and_residence_details[1].text.replace('Residence Country:',
                                                                                                '').strip()

                    if 'Place of birth' in birthplace_and_residence_details[2].text:
                        place_of_birth = birthplace_and_residence_details[2].text.replace('Place of birth:', '').strip()

                    elif 'Birth Country' in birthplace_and_residence_details[2].text:
                        country_of_birth = birthplace_and_residence_details[2].text.replace('Birth Country:',
                                                                                            '').strip()

                    elif 'Place of residence' in birthplace_and_residence_details[2].text:
                        place_of_residence = birthplace_and_residence_details[2].text.replace('Place of residence :',
                                                                                              '').strip()

                    elif 'Residence Country' in birthplace_and_residence_details[2].text:
                        country_of_residence = birthplace_and_residence_details[2].text.replace('Residence Country:',
                                                                                                '').strip()


                else:
                    place_of_birth = ''
                    country_of_birth = ''
                    place_of_residence = ''
                    country_of_residence = ''

                # Get event
                try:
                    medals_table = driver.find_element_by_id('mirs-table-biomedals')
                    medals_row = medals_table.find_elements_by_tag_name('tr')[1]
                    event = medals_row.find_elements_by_tag_name('td')[1].text.split('\n')[0]
                except:
                    event = ''
                    print('Could not get event')

                name_list += [name]
                discipline_list += [discipline]
                country_list += [country]
                dob_list += [dob]
                age_list += [age]
                gender_list += [gender]
                function_list += [function]
                height_in_meters_list += [height_in_meters]
                height_in_ft_in_list += [height_in_ft_in]
                place_of_birth_list += [place_of_birth]
                country_of_birth_list += [country_of_birth]
                place_of_residence_list += [place_of_residence]
                country_of_residence_list += [country_of_residence]
                event_list += [event]

            except:
                print(f'Could not extract athlete {name}\'s details')

            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            print(f'Extracted row {row_num} of page {page}')

        except:
            print(f"Couldn't get href for row {row_num}")

        row_num += 1

    page_data_df = pd.DataFrame({
        'Name': name_list,
        'Team': country_list,
        "Date of Birth": dob_list,
        'Age': age_list,
        'Gender': gender_list,
        'Function': function_list,
        'Height in Meters': height_in_meters_list,
        'Height in ft in': height_in_ft_in_list,
        'Place of birth': place_of_birth_list,
        'Birth Country': country_of_birth_list,
        'Place of residence': place_of_residence_list,
        'Residence Country': country_of_residence_list,
        'Discipline': discipline_list,
        'Event': event_list})

    #Concatenate the main dataframe and the dataframe with this page's athletes details
    main_df = pd.concat([main_df, page_data_df])

    # Sort the dataframe using the name feature, drop duplicated records, and save the file as data.csv
    main_df.sort_values(by='Name', inplace=True)
    main_df.drop_duplicates(inplace=True)
    main_df.to_csv('data.csv', index=False)

# Read the re-scraped data and drop the duplicates, in case they were not dropped earlier
main_df = pd.read_csv('data.csv')
main_df.reset_index(inplace=True, drop=True)
main_df.drop_duplicates(subset = ['Name', 'Team', 'Age', 'Function', 'Birth Country', 'Discipline','Event'], inplace=True)
main_df.sort_values(by='Name', inplace=True)

main_df.to_csv('data.csv', index=False)

# Display the results of the re-scraping
print(f'Scraping completed successfully. \n'
      f'Pages re-scrapped: {pages}\n'
      f'New records scrapped: {len(main_df) - old_records_num}\n'
      f'New total records: {len(main_df)}\n')

time.sleep(2)
driver.quit()