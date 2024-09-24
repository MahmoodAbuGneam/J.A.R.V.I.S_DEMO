# Jarvis AI Assistant

## Overview
Jarvis is an AI-powered assistant inspired by the fictional AI from the Iron Man movies. It offers a range of functionalities including email management, music control, weather information, image search, and more, all with a witty and engaging personality.

## Features
- Voice Recognition and Natural Language Processing
- Email Management (via Gmail)
- Spotify Integration
- Weather Information
- Image Search
- Reminders and To-Do Lists
- Coding Problem Solving

## Prerequisites
- Python 3.12 or higher
- A Google account for Gmail integration
- A Spotify account for music control

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/your-username/jarvis-ai-assistant.git
   cd jarvis-ai-assistant
   ```

2. Install required packages:
   ```
   pip install -r requirements.txt
   ```

## Configuration

### OpenAI API
1. Sign up for an OpenAI account and obtain an API key.
2. Create a file named `.env` in the project root.
3. Add your OpenAI API key to the `.env` file:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

### Gmail Integration
1. Set up a Google Cloud Project and enable the Gmail API.
2. Create OAuth 2.0 credentials (select "Desktop app" as the application type).
3. Download the credentials JSON file and rename it to `credentials.json`.
4. Place `credentials.json` in the project root directory.

### Spotify Integration
1. Create a Spotify Developer account and set up a new application.
2. Obtain your Client ID and Client Secret.
3. Add the following to your `.env` file:
   ```
   SPOTIFY_USERNAME=your_spotify_username
   SPOTIFY_CLIENT_ID=your_client_id
   SPOTIFY_CLIENT_SECRET=your_client_secret
   ```

## Usage

1. Run the main script:
   ```
   python jarvis.py
   ```

2. When prompted, authenticate with your Google account to enable Gmail functionality.

3. Speak commands to Jarvis or type them in the console.

## Command Examples
- "Hey Jarvis, do I have any new emails?"
- "Jarvis, play some music on Spotify"
- "What's the weather like today?"
- "Show me pictures of Iron Man"
- "Add 'buy groceries' to my to-do list"

## Project Structure
- `jarvis.py`: Main script
- `tools.py`: Utility functions
- `assist.py`: OpenAI API interaction and TTS functionality
- `spot.py`: Spotify integration
- `gmail_integration.py`: Gmail API interactions
- `jarvis_gmail_commands.py`: Email-related command processing

## Customization
- To modify Jarvis's personality or add new commands, edit the AI instructions in `assist.py`.
- To add new functionalities, create new modules and integrate them in `jarvis.py`.

## Troubleshooting
- If you encounter authentication issues with Gmail, delete the `token.json` file and re-authenticate.
- For Spotify issues, ensure your credentials in the `.env` file are correct.

## Contributing
Contributions are welcome! Please feel free to submit a Pull Request.

## License
[MIT License](LICENSE)

## Disclaimer
This project is for educational purposes only. Ensure you comply with all relevant APIs' terms of service.
