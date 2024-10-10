from pathlib import Path
import pandas as pd

import requests, json
from bs4 import BeautifulSoup
BASE_FILEPATH = Path(__file__).resolve().parent.parent.parent

def get_dog_links(base_url):
    all_dog_breed_links = []

    for page_num in range(1,30):
        current_page_url = f'{base_url}page/{str(page_num)}/'        # Send a GET request to the current page URL
        
        response = requests.get(current_page_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the HTML content using BeautifulSoup
            soup = BeautifulSoup(response.text, 'html.parser')

            # Find all <a> tags with the specific class 
            links = soup.find_all('a', class_='d-block relative')

            # Extract the href attributes from the found links
            dog_breed_links = [link['href'] for link in links if 'href' in link.attrs]
            all_dog_breed_links.extend(dog_breed_links)

        else:
            print(f"Failed to retrieve page: {response.status_code}")
            break

    return all_dog_breed_links


def download_AKC_dog_data(output_directory: Path = None) -> None:    
    """Downloads dog breed infomation to a local directory

    Args:
        output_directory: desired output location. Defaults to 'Project/Data/Raw/AmericanKernelClub'
    Modifies:
        Saves raw files from dos.pa.gov to output_directory with a separate directory
        for each year's files.
    """
    # source to store the data:
    if output_directory is None:
        output_directory = BASE_FILEPATH / "Project" / "Data" / "Raw" / "AmericanKernelClub"
    else:
        output_directory = Path(output_directory).resolve()

    base_url = 'https://www.akc.org/dog-breeds/'
    all_dog_breed_links = get_dog_links(base_url)

    for breed_link in all_dog_breed_links[0:1]:
        print('breed link: ', breed_link)
        response = requests.get(breed_link)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')

            for x in soup.find_all('p'):                                   
                print(f'x: {x}')
            # # Access the weight value
            # print(soup.find('div', class_="breed-page__hero__overview__key-traits"))
            # weight_div = soup.find('h3', text='Weight').find_next('p')
            # weight_value = weight_div.get_text(strip=True)

            # print(f"Weight: {weight_value}")
            # # Find all the relevant icon blocks
            # overview_blocks = soup.find_all('div', class_='flex breed-page__hero__overview__icon-block')

            # # Create a dictionary to store the values
            # breed_info = {}

            # # Iterate through each block and extract the title and corresponding value
            # for block in overview_blocks:
            #     title = block.find('h3', class_='fw-b f-16 mt0 mb2 lh-solid breed-page__hero__overview__title').text
            #     value = block.find('p', class_='f-16 my0 lh-solid breed-page__hero__overview__subtitle').text
                
            #     # Store the information in the dictionary
            #     breed_info[title] = value

            # # Print out the extracted values
            # height = breed_info.get('Height', 'Not found')
            # weight = breed_info.get('Weight', 'Not found')
            # life_expectancy = breed_info.get('Life Expectancy', 'Not found')

            # print(f"Height: {height}")
            # print(f"Weight: {weight}")
            # print(f"Life Expectancy: {life_expectancy}")
        
        else:
            print(f"Failed to retrieve page, status code: {response.status_code}")


#download_AKC_dog_data()
response = requests.get("https://www.mydogsname.com/dog-breeds/labrador-retriever/")
if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    breed_data = soup.find_all('div', id = "breedData")
    print(breed_data)
