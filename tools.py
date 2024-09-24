import python_weather
import asyncio
import assist
from icrawler.builtin import GoogleImageCrawler
import os
import spot
import cv2
import pygetwindow as gw
import pyautogui
from screeninfo import get_monitors
import threading
from datetime import datetime,timedelta
import logging




#logging setup 


logging.basicConfig(filename='jarvis.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')



async def get_weather(city_name):
    async with python_weather.Client(unit= python_weather.IMPERIAL) as client:
        weather = await client.get(city_name)
        return weather



def search(query):
    try:
        google_Crawler = GoogleImageCrawler(storage={"root_dir": r'./images'})
        google_Crawler.crawl(keyword=query, max_num=1)
        # Check if any file is downloaded
        if not os.listdir(r'./images'):
            print("No images found for your query.")
        else:
            print("Image downloaded successfully.")
            # say using tts " i downloaded the image"
            done = assist.TTS("I downloaded the image.")
    except Exception as e:
        print(f"An error occurred: {e}")


def open_image_full_screen(image_path):
    image = cv2.imread(image_path)
    if image is not None:
        monitors = get_monitors()
        if len(monitors) > 1:
            # Assuming the first two monitors are duplicates and need to be spanned
            first_monitor = monitors[0]
            second_monitor = monitors[1]
            
            # Calculate the total width and the smallest y-offset
            total_width = first_monitor.width + second_monitor.width
            y_offset = min(first_monitor.y, second_monitor.y)

            cv2.namedWindow("Image Full Screen", cv2.WND_PROP_FULLSCREEN)
            cv2.setWindowProperty("Image Full Screen", cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
            cv2.moveWindow("Image Full Screen", first_monitor.x, y_offset)
            cv2.resizeWindow("Image Full Screen", total_width, first_monitor.height)
            cv2.imshow("Image Full Screen", image)

            # Attempt to bring the window to the foreground
            try:
                win = gw.getWindowsWithTitle('Image Full Screen')[0]  # Get window with specific title
                win.activate()
            except Exception as e:
                print(f"Failed to bring window to foreground: {e}")
            
            cv2.waitKey(0)  # Wait indefinitely until a key is pressed
            cv2.destroyAllWindows()
        else:
            print("Not enough monitors detected")
    else:
        print("Failed to load image")



async def parse_command(command):


    # Handle greeting
    if "greet" in command:
        # This will trigger Jarvis to say something witty as a greeting
        greeting = assist.ask_question_memory("Greet me with a fresh, witty and funny line maybe related to iron man or jarvis or ai something like that")
        assist.TTS(greeting)

    # Weather handling
    if "weather" in command:
        weather_description = await get_weather("Tel Aviv")
        query = "System information: " + str(weather_description)
        print(query)
        response = assist.ask_question_memory(query)
        assist.TTS(response)
        return "Weather information processed"



    # solving coding problems 
    elif "solve" in command and "problem" in command:
        problem = command.split("problem:", 1)[1].strip() if "problem:" in command else command
        result = solve_coding_problem(problem)
        return result

    # Image search functionality
    elif "search" in command:
        files = os.listdir("./images")
        [os.remove(os.path.join("./images", f)) for f in files]
        query = command.split("-")[1]
        assist.TTS(f"Searching for {query} image.")
        search(query)
        assist.TTS(f"Opening the image of {query}.")
        image_path = os.path.join("./images", "000001.jpg")
        open_image_full_screen(image_path)
        return "Image search completed"

    # Spotify control
    elif "play" in command:
        spot.start_music()

    elif "skip" in command:
        spot.skip_to_next()
    
    elif "previous" in command:
        spot.skip_to_previous()
    
    elif "stop" in command:
        spot.stop_music()

    elif "pause" in command:
        spot.stop_music()
    
    elif "resume" in command:
        spot.start_music()
    
    elif "spotify" in command:
        spotify_info = spot.get_current_playing_info()
        query = "System information: " + str(spotify_info)
        print(query)
        response = assist.ask_question_memory(query)
        assist.TTS(response)
    
    else:
        logging.warning(f"Unrecognized command: {command}")
        return "I'm not sure how to handle that command."

    




# problem solving skills ( coding )

def solve_coding_problem(problem):
    logging.info(f"Attempting to solve coding problem: {problem}")
    response = assist.ask_question_memory(f"Solve this coding problem: {problem}")
    logging.debug(f"Received response: {response}")
    
    code = extract_code_from_response(response)
    
    if code:
        file_extension = determine_file_extension(code)
        file_name = f"solution{file_extension}"
        
        try:
            with open(file_name, 'w') as file:
                file.write(code)
            logging.info(f"Solution saved to {file_name}")
            return f"I've solved the problem and saved the solution to {file_name}. Is there anything else you need help with?"
        except IOError as e:
            logging.error(f"Error saving solution: {str(e)}")
            return f"I solved the problem, but encountered an error while saving the solution: {str(e)}. Can I help with anything else?"
    else:
        logging.warning("No code solution found in the response.")
        return "I couldn't find a code solution in my response. Can you please rephrase the problem or try a different one?"


# extracting the code from the reponse of the ai 
def extract_code_from_response(response):
    logging.debug("Extracting code from response")
    code_blocks = response.split('```')
    if len(code_blocks) >= 3:
        # The code is the second element (index 1) in the split result
        code = code_blocks[1].strip()
        logging.info("Code successfully extracted")
        return code
    else:
        logging.warning("No code block found in triple backticks")
        # If no code block is found, return the entire response
        return response



def determine_file_extension(code):
    logging.debug("Determining file extension")
    if 'def ' in code or 'import ' in code or 'print(' in code:
        return '.py'
    elif 'const ' in code or 'let ' in code:
        return '.js'
    elif 'public class ' in code or 'System.out.println' in code:
        return '.java'
    else:
        return '.txt'


