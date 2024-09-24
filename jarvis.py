# jarvis.py

from RealtimeSTT import AudioToTextRecorder
import assist
import time
import tools
import asyncio
import logging
import gmail_integration
import jarvis_gmail_commands

logging.basicConfig(filename='jarvis.log', level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s')

def parse_jarvis_response(response):
    if response.startswith('#'):
        command_parts = response[1:].split('-', 1)
        command_type = command_parts[0]
        command_content = command_parts[1] if len(command_parts) > 1 else ""
        
        if command_type == "search":
            return asyncio.run(tools.parse_command(f"search-{command_content}"))
        elif command_type == "spotify":
            return asyncio.run(tools.parse_command("spotify"))
        elif command_type == "reminder":
            return asyncio.run(tools.parse_command(f"reminder {command_content}"))
        elif command_type == "email":
            return jarvis_gmail_commands.process_email_command(command_content, gmail_creds)
    
    return response

async def process_user_input(current_text):
    print("Mahmood: " + current_text)
    logging.info(f"Processing command: {current_text}")
    
    try:
        if "solve" in current_text.lower() and "problem" in current_text.lower():
            result = await tools.parse_command(current_text)
        else:
            response = assist.ask_question_memory(current_text)
            print("Raw Jarvis response:", response)
            result = parse_jarvis_response(response)
        
        if result:
            print(result)
            assist.TTS(result)
        else:
            assist.TTS("I'm sorry, I couldn't process that command. Can you try again?")
    except Exception as e:
        logging.error(f"Error processing command: {str(e)}")
        assist.TTS("I encountered an error while processing your request. Can you please try again?")




if __name__ == '__main__':
    recorder = AudioToTextRecorder(spinner=False, model="tiny.en", language="en", post_speech_silence_duration=0.4, silero_sensitivity=0.4)
    hot_words = ["jarvis","hey","what","how","solve"]
    exit_words = ["goodbye","bye","exit","shutdown"]
    skip_hot_word_check = False
    
    # Initialize Gmail credentials
    gmail_creds = gmail_integration.authenticate()
    
    asyncio.run(tools.parse_command("greet"))
    print("Say something...")
    
    while True:
        current_text = recorder.text()
        print(current_text)
        if any(hot_word in current_text.lower() for hot_word in hot_words) or skip_hot_word_check:
            if current_text:
                recorder.stop()
                asyncio.run(process_user_input(current_text))
                recorder.start()
            
            skip_hot_word_check = "?" in current_text or "know" in current_text
        

        if any(exit_word in current_text.lower() for exit_word in exit_words):
            print("Exiting Jarvis, Cause : Exit Word encountered")
            break 
