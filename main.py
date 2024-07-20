import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

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

time.sleep(5)

# Create a dataframe that will hold all the data
main_df = pd.DataFrame({
            'Name':[],
            'Team':[],
            "Date of Birth":[],
            'Age':[],
            'Gender':[],
            'Function':[],
            'Height in Meters':[],
            'Height in ft in': [],
            'Place of birth':[],
            'Birth Country':[],
            'Place of residence':[],
            'Residence Country':[],
            'Discipline': [],
            'Event':[]})

# Create some important variablesvariables
finished_scraping = False #Will turn true when scraping completes sucessfully
page_num = 1  # Store the page number being scraped
total_records = 1 # Keep count of the total records scraped

# Create a while loop to loop through all the pages
while finished_scraping is False:

    table = driver.find_element_by_id('mirs-table-athletes')    #table with the details of a player.
    row_data = table.find_elements_by_tag_name('tr')[1:]    # Row with athletes name, and link to athletes full details

    # Create lists to store the data for all the athletes in this page
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

    # Set the value of the row_num variable that keeps track of the row number being scraped in the page
    row_num = 1

    # Loop through all the rows in the page. Each row contains a different athlete's details
    for row in row_data:
        # Create a try except block to handle errors that may occur, preventing the program from breaking.
        # Cause of error is mostly network error; network loss or a very slow network
        try:
            # Get the link to the athlete's page that contains detailed data, and open it in a new tab and go to the tab
            td = row.find_elements_by_tag_name('td')
            href = td[0].find_element_by_class_name('competitor-container').get_attribute('href')
            driver.execute_script(f"window.open('{href}', '_blank');")
            driver.switch_to.window(driver.window_handles[-1])

            try:
                # Wait till the page details have loaded successfully. Almost instantaneous
                wait_games = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, 'bios-personalinfo'))
                )
                # Store the personal details in the variable personal info and extract them
                personal_info = driver.find_element_by_class_name('col-9').find_elements_by_class_name('row')

                name_country_and_discipline_details = personal_info[0]
                other_details = personal_info[1]

                name = name_country_and_discipline_details.find_elements_by_class_name('pt-2')[0].text
                discipline = name_country_and_discipline_details.find_elements_by_class_name('pt-2')[1].text.split('\n')[0]
                country = name_country_and_discipline_details.find_elements_by_class_name('wrsNoc')[0].text

                other_details = other_details.find_elements_by_class_name('col-md-6')
                age_and_gender_details = other_details[0].find_elements_by_class_name('pt-2')
                birthplace_and_residence_details = other_details[1].find_elements_by_class_name('pt-2')

                dob = age_and_gender_details[0].text.replace('Date of Birth:', '').strip()
                age = age_and_gender_details[1].text.replace('Age:', '').strip()
                gender = age_and_gender_details[2].text.replace('Gender:', '').strip()
                function = age_and_gender_details[3].text.replace('Function:', '').strip()

                # Some athletes do not have their height details. This try except block handles scenarios without this data
                try:
                    height = age_and_gender_details[4].text.replace('Height m / ft in:  ', '')
                    height_in_meters = height[:height.index('/')]
                    height_in_ft_in = height[height.index('/')+1:]
                except:
                    height_in_meters = ''
                    height_in_ft_in = ''

                # Some athletes have data about their place of birth, country of birth, place of residence, and their
                # country of residence(4 pieced of data). Some athletes have three pieces of this data, some two,
                # some one and some do not have any piece of data in this category.
                # This nested if else block of code handles that
                if len(birthplace_and_residence_details) == 4: #Athletes with all 4 pieces of birth and residential data
                    try:
                        place_of_birth = birthplace_and_residence_details[0].text.replace('Place of birth:', '').strip()
                        country_of_birth = birthplace_and_residence_details[1].text.replace('Birth Country:', '').strip()
                        place_of_residence = birthplace_and_residence_details[2].text.replace('Place of residence :', '').strip()
                        country_of_residence = birthplace_and_residence_details[3].text.replace('Residence Country:', '').strip()
                    except:
                        print('Error getting birth and residencial details')

                elif len(birthplace_and_residence_details) == 1:#Athletes with just 1 pieces of either birth or residential data
                    place_of_birth = ''
                    country_of_birth = ''
                    place_of_residence = ''
                    country_of_residence = ''
                    if 'Place of birth' in birthplace_and_residence_details[0].text:
                        place_of_birth = birthplace_and_residence_details[0].text.replace('Place of birth:', '').strip()
                    elif 'Birth Country' in birthplace_and_residence_details[0].text:
                        country_of_birth = birthplace_and_residence_details[0].text.replace('Birth Country:', '').strip()
                    elif 'Place of residence' in birthplace_and_residence_details[0].text:
                        place_of_residence = birthplace_and_residence_details[0].text.replace('Place of residence :', '').strip()
                    elif 'Residence Country' in birthplace_and_residence_details[0].text:
                        country_of_residence = birthplace_and_residence_details[0].text.replace('Residence Country:', '').strip()

                elif len(birthplace_and_residence_details) == 2: #Athletes with 2 pieces of birth or residential data
                    place_of_birth = ''
                    country_of_birth = ''
                    place_of_residence = ''
                    country_of_residence = ''
                    if 'Place of birth' in birthplace_and_residence_details[0].text:
                        place_of_birth = birthplace_and_residence_details[0].text.replace('Place of birth:', '').strip()
                    elif 'Birth Country' in birthplace_and_residence_details[0].text:
                        country_of_birth = birthplace_and_residence_details[0].text.replace('Birth Country:', '').strip()
                    elif 'Place of residence' in birthplace_and_residence_details[0].text:
                        place_of_residence = birthplace_and_residence_details[0].text.replace('Place of residence :', '').strip()
                    elif 'Residence Country' in birthplace_and_residence_details[0].text:
                        country_of_residence = birthplace_and_residence_details[0].text.replace('Residence Country:', '').strip()

                    if 'Place of birth' in birthplace_and_residence_details[1].text:
                        place_of_birth = birthplace_and_residence_details[1].text.replace('Place of birth:', '').strip()

                    elif 'Birth Country' in birthplace_and_residence_details[1].text:
                        country_of_birth = birthplace_and_residence_details[1].text.replace('Birth Country:', '').strip()

                    elif 'Place of residence' in birthplace_and_residence_details[1].text:
                        place_of_residence = birthplace_and_residence_details[1].text.replace('Place of residence :', '').strip()

                    elif 'Residence Country' in birthplace_and_residence_details[1].text:
                        country_of_residence = birthplace_and_residence_details[1].text.replace('Residence Country:', '').strip()


                elif len(birthplace_and_residence_details) == 3: #Athletes with all 3 pieces of birth and residential data
                    place_of_birth = ''
                    country_of_birth = ''
                    place_of_residence = ''
                    country_of_residence = ''
                    if 'Place of birth' in birthplace_and_residence_details[0].text:
                        place_of_birth = birthplace_and_residence_details[0].text.replace('Place of birth:', '').strip()
                    elif 'Birth Country' in birthplace_and_residence_details[0].text:
                        country_of_birth = birthplace_and_residence_details[0].text.replace('Birth Country:', '').strip()
                    elif 'Place of residence' in birthplace_and_residence_details[0].text:
                        place_of_residence = birthplace_and_residence_details[0].text.replace('Place of residence :', '').strip()
                    elif 'Residence Country' in birthplace_and_residence_details[0].text:
                        country_of_residence = birthplace_and_residence_details[0].text.replace('Residence Country:', '').strip()

                    if 'Place of birth' in birthplace_and_residence_details[1].text:
                        place_of_birth = birthplace_and_residence_details[1].text.replace('Place of birth:', '').strip()

                    elif 'Birth Country' in birthplace_and_residence_details[1].text:
                        country_of_birth = birthplace_and_residence_details[1].text.replace('Birth Country:', '').strip()

                    elif 'Place of residence' in birthplace_and_residence_details[1].text:
                        place_of_residence = birthplace_and_residence_details[1].text.replace('Place of residence :', '').strip()

                    elif 'Residence Country' in birthplace_and_residence_details[1].text:
                        country_of_residence = birthplace_and_residence_details[1].text.replace('Residence Country:', '').strip()

                    if 'Place of birth' in birthplace_and_residence_details[2].text:
                        place_of_birth = birthplace_and_residence_details[2].text.replace('Place of birth:', '').strip()

                    elif 'Birth Country' in birthplace_and_residence_details[2].text:
                        country_of_birth = birthplace_and_residence_details[2].text.replace('Birth Country:', '').strip()

                    elif 'Place of residence' in birthplace_and_residence_details[2].text:
                        place_of_residence = birthplace_and_residence_details[2].text.replace('Place of residence :', '').strip()

                    elif 'Residence Country' in birthplace_and_residence_details[2].text:
                        country_of_residence = birthplace_and_residence_details[2].text.replace('Residence Country:', '').strip()

                else: #Athletes without all 4 pieces of birth and residential data
                    place_of_birth = ''
                    country_of_birth = ''
                    place_of_residence = ''
                    country_of_residence = ''

                # Get the event the athlete competes in
                try:
                    medals_table = driver.find_element_by_id('mirs-table-biomedals')
                    medals_row = medals_table.find_elements_by_tag_name('tr')[1]
                    event = medals_row.find_elements_by_tag_name('td')[1].text.split('\n')[0]
                except:
                    event = ''
                    print('Could not get event')

                # Append the athlete's details to the lists that store the page's athlete's data
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

            # In case an error occurs during any of these steps(which is very high unlikely), an error message is printed
            #on the console. Again, the most probable cause of error is network error.
            except:
                print(f'Could not extract athlete {name}\'s details')

            # Close the tab
            driver.close()
            driver.switch_to.window(driver.window_handles[0])
            print(f'Extracted row {row_num} of page {page_num}')

        # Handle scenarios where the link o an athlete's details could not be found
        except:
            print(f"Couldn't get href for row {row_num}")


        row_num += 1
        total_records += 1

    # Create a dataframe for the page's extracted athlete's data
    page_data_df = pd.DataFrame({
                'Name':name_list,
                'Team':country_list,
                "Date of Birth":dob_list,
                'Age':age_list,
                'Gender':gender_list,
                'Function':function_list,
                'Height in Meters':height_in_meters_list,
                'Height in ft in': height_in_ft_in_list,
                'Place of birth':place_of_birth_list,
                'Birth Country':country_of_birth_list,
                'Place of residence':place_of_residence_list,
                'Residence Country':country_of_residence_list,
                'Discipline': discipline_list,
                'Event':event_list})

    # Append the page's data to all the collected data dataframe. Save the data to a csv file
    main_df = pd.concat([main_df, page_data_df])
    main_df.to_csv('data.csv', index=False)

    # Find the next page button and click it. Its absence indicates the end of the scraping
    try:
        nxt = driver.find_elements_by_class_name('me-2')[2]
        nxt.click()
        page_num += 1
        print(f'Scraping page {page_num}')
    except:
        finished_scraping = True
        # Display the scraping details
        print(f'Scraping completed successfully. \n'
              f'Total pages scrapped: {page_num}'
              f'Total records scrapped: {total_records}')

    # Wait for three seconds for the new page to load sucessfully
    time.sleep(2)
    # Close the automated browser
driver.quit()