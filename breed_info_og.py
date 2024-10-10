from Levenshtein import ratio 
import pandas as pd
import myDogsNameScraperVersion2 as scraper

# Levenshtein.distance : This method calculates the Levenshtein Distance of two strings this defines 
# how many operations where needed to turn one string into another by inserting a character, removing
#  a character or replacing a character. 
# 
# Ratio on the other hand provides a similarity ratio in between the two string values which ranges 
# from 0 to 1. The smaller the represented value is to the 1, the more similar the strings belong
# to each other.

def make_Dog_Dictionary(file_path) -> dict:
    ''' 
        Given a file_path, converts an excel document into a nested dictionary 
        where the index column are the keys, and values contained a column-value pair
        
        Args: file_path : the location of the data in the relative directory
        Returns: A nested dictionary if the file is found, or an error message based 
        on the problem
    '''
    try:
        # Read the Excel file
        df = pd.read_excel(file_path, index_col=0)# engine='openpyxl')  # Specify engine if necessary
        dog_dict = df.to_dict(orient='index')
        print(f'dog dict: {dog_dict}')
        return dog_dict
    except FileNotFoundError:
        print(f"The file at {file_path} was not found.")
    except Exception as e:
        print(f"An error occurred: {e}")


def find_approximate_dog_breed(dog_dictionary) -> None:
    '''
        Given a dog dictionary, this function prompts a user input, and attempts to 
        provide dog breed information as per the input.
         
        Args: A dictionary of dog data with breed name as keys and breed attribues as
        values.
         
        Return: None
    '''
    dog_names = dog_dictionary.keys()
    while True:
        while True:
            user_input = input("Please enter the kind of dog breed you would like to know information about: ").title()
            if user_input in dog_names:
                print("Great, here is the information we have on the provided breed: ")
                dog = dog_dictionary[user_input]
                print(f'A {user_input} typically weighs: {dog['Weight']} lbs. Their lifespan spans {dog['Lifespan']} years, and these are their core metrics:')
                print(f'When it comes to Trainability, {user_input} scores a {dog['Trainable']}/5.')
                print(f'When it comes to Exercise needed, {user_input} scores a {dog['Exercise']}/5')
                print(f'When it comes to Shedding, {user_input} scores a {dog['Shedding']}/5')
                print("We also have additional metrics regarding Behavior, Care, and environment...")
               
                user_more_data_request = input("Would you like to know about these details as well? Please type yes or no:").title()
                if user_more_data_request == "Yes":
                    # Behavior 
                    print(f'Great, when it comes to Behavior, this is how the {user_input} scores:')
                    print("\n".join(f"{key}: {value}" for key, value in dog['Behavior'].items()))
                    # Care
                    print(f'When it comes to dogs, they all need some loving! Here are the typical care requirements for {user_input}:')
                    print("\n".join(f"{key}: {value}" for key, value in dog['Care'].items()))
                    #Environment
                    print(f'Lastly, a {user_input} thrives in the following type of environment:')
                    print("\n".join(f"{key}: {value}" for key, value in dog['Environment'].items()))                
                
                break
                
            else: 
                distances = []
                for dog_name in dog_names:
                    distances.append((dog_name, ratio(dog_name, user_input)))

                distances.sort(key=lambda x: x[1], reverse=True)
                print("Hmmmm. we don't seem to have that particular breed...")
                print("Maybe it was a spelling error? Did you mean any of these dog breeds?")
                print([name for name, _ in distances[:5]])
        
        # Prompting the user to ask more questions
        continue_prompt = input("Would you like to ask about another dog breed? (yes/no): ").strip().lower()
        if continue_prompt != 'yes':
            print("Thank you for using the dog breed information service! Goodbye!")
            break


if __name__ == '__main__':
    dog_dict = scraper.download_My_Dogs_Name_data() 
    print("Welcome! We hope to help you find information about any dog breed!")
    find_approximate_dog_breed(dog_dict)
