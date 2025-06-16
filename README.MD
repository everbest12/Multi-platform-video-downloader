🎥 Multi-Platform Video Downloader
A powerful Python-based tool to download videos from multiple platforms including YouTube, TikTok, Facebook, and MovieBox. It uses LangChain agents for dynamic task classification and supports user-selected quality, persistent preferences, and download progress tracking.

✨ Features
1. Download from YouTube (single videos, playlists, channels)

2. Download TikTok, Facebook, and direct MP4 video links

3. User selection of download folder and video quality

4. Saved preferences for folder path and video links

5. LangChain agents for intelligent task classification

6. Download progress bar using tqdm

7.  Modular helper structure for clean code management

📂 Folder Structure
bash
Copy
Edit
project_root/
│
├── main_downloader.py          # Main controller with LangChain agent
├── video_link.txt              # Stores last used video URL
├── download_folder.txt         # Stores last used download path
│
├── helpers/
│   ├── youtube_downloader.py
│   ├── tiktok_downloader.py
│   ├── facebook_downloader.py
│   ├── moviebox_downloader.py
│
├── .env                        # Contains your OPENAI_API_KEY
└── requirements.txt            # Python dependencies

# Getting Started
1. Clone the Repository
bash
Copy
Edit
git clone https://github.com/yourusername/video-downloader.git
cd video-downloader
2. Set up your Environment
bash
Copy
Edit
python -m venv venv
venv\Scripts\activate  # on Windows
pip install -r requirements.txt
3. Add Your OpenAI API Key
Create a .env file in the project root:

ini
Copy
Edit
OPENAI_API_KEY=your_openai_key_here
🔧 Usage
bash
Copy
Edit
python main_downloader.py
You will be prompted to:
Choose the download folder (saved to download_folder.txt)

Choose video quality:

1: 1080p
2: 720p
3: 480p
4: Audio only
5: Default best available
Paste or use a saved video URL (stored in video_link.txt)

The program auto-detects the source (e.g., YouTube, TikTok) and dispatches the download accordingly using the proper helper module.
🧠 How It Works
Uses LangChain Agents with zero-shot-react-description to determine the right download tool.

Maps URLs to the right handler: YouTube, TikTok, Facebook, etc.

Downloads using yt-dlp or requests, depending on the platform.

# Supported Platforms
Platform	Features
YouTube	Video, Playlist, Channel
TikTok	Single video
Facebook	Single video
MovieBox	Direct MP4 file

Dependencies
yt-dlp

tqdm

colorama

python-dotenv

requests

langchain

langchain-community

Install them using:

bash
Copy
Edit
pip install -r requirements.txt

LangChain Upgrade Note
You may see deprecation warnings for ChatOpenAI and .run() — these are now replaced with:
python
Copy
Edit
from langchain_openai import ChatOpenAI
agent.invoke("task description")
Your current implementation already uses invoke.

FAQ
Q: Why is the script stuck or not downloading?
A: Check if the quality selected is supported by the video link (some YouTube videos may not support 720p or 1080p).

Q: Can I change the saved folder or link?
A: Yes, simply delete or edit download_folder.txt and video_link.txt.

License
MIT License

