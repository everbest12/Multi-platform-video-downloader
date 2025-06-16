# main_downloader.py
import os
from dotenv import load_dotenv
from langchain.agents import Tool, initialize_agent
from langchain_community.chat_models import ChatOpenAI
from colorama import init, Fore
from helpers.youtube_downloader import handle_youtube
from helpers.tiktok_downloader import handle_tiktok
from helpers.moviebox_downloader import handle_moviebox
from helpers.facebook_downloader import handle_facebook
from helpers.udemy_downloader import handle_udemy
from helpers.coursera_downloader import handle_coursera

# Setup
init(autoreset=True)
load_dotenv()
os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Define LangChain tools
tools = [
    Tool(name="YouTubeDownloader", func=handle_youtube, description="Download from YouTube (video, playlist, channel)"),
    Tool(name="TikTokDownloader", func=handle_tiktok, description="Download TikTok videos"),
    Tool(name="MovieBoxDownloader", func=handle_moviebox, description="Download direct .mp4 video links (MovieBox)"),
    Tool(name="FacebookDownloader", func=handle_facebook, description="Download Facebook videos"),
    Tool(name="UdemyDownloader", func=handle_udemy, description="Download Udemy videos (requires login cookies)"),
    Tool(name="CourseraDownloader", func=handle_coursera, description="Download Coursera videos (requires login cookies)")
]

llm = ChatOpenAI(temperature=0)
agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Get download preferences
def get_user_preferences():
    print(Fore.YELLOW + "\n Choose download preferences:\n")
    folder_file = "download_folder.txt"
    output_path = ""
    if os.path.exists(folder_file):
        with open(folder_file, 'r') as f:
            output_path = f.read().strip().strip('"\'')
            print(Fore.YELLOW + f"→ Using saved folder path: {output_path}")
    else:
        output_path = input(Fore.YELLOW + "→ Folder to save videos (default: ./downloads): ").strip().strip('"\'')
        if not output_path:
            output_path = os.path.join(os.getcwd(), "downloads")
        with open(folder_file, 'w') as f:
            f.write(output_path)

    print(Fore.YELLOW + "\n Select video quality:")
    print(Fore.YELLOW + "1. 1080p (best)")
    print(Fore.YELLOW + "2. 720p")
    print(Fore.YELLOW + "3. 480p")
    print(Fore.YELLOW + "4. Audio only")
    print(Fore.YELLOW + "5. Default (bestvideo+bestaudio/best)")

    choice = input(Fore.YELLOW + "→ Enter choice [1-5]: ").strip()
    quality_map = {
        "1": "bestvideo[height<=1080]+bestaudio/best",
        "2": "bestvideo[height<=720]+bestaudio/best",
        "3": "bestvideo[height<=480]+bestaudio/best",
        "4": "bestaudio",
        "5": "bestvideo+bestaudio/best"
    }

    if choice not in quality_map:
        print(Fore.RED + "\n Invalid quality choice. Falling back to default.")

    quality = quality_map.get(choice, "bestvideo+bestaudio/best")

    try:
        os.makedirs(output_path, exist_ok=True)
    except Exception as e:
        print(Fore.RED + f"\n Error creating folder: {e}\nUsing default folder './downloads' instead.")
        output_path = os.path.join(os.getcwd(), "downloads")
        os.makedirs(output_path, exist_ok=True)

    return output_path, quality

# Detect platform and task type
def detect_task(link: str) -> str:
    if "youtube.com" in link or "youtu.be" in link:
        if "playlist?list=" in link:
            return "Download a YouTube playlist"
        elif "/channel/" in link or "/@" in link:
            return "Download all videos from a YouTube channel"
        else:
            return "Download a single YouTube video"
    elif "tiktok.com" in link:
        return "Download a TikTok video"
    elif "facebook.com" in link:
        return "Download a Facebook video"
    elif "udemy.com" in link:
        return "Download a video from Udemy"
    elif "coursera.org" in link:
        return "Download a video from Coursera"
    elif link.endswith(".mp4"):
        return "Download a MovieBox video"
    else:
        return "Download video from unknown source"

# Main runner
def main():
    print(Fore.CYAN + "\n🎥 Welcome to the Multi-Platform Video Downloader 🎥")

    output_path, quality = get_user_preferences()

    link_file = "video_link.txt"
    if os.path.exists(link_file):
        with open(link_file, 'r') as f:
            link = f.read().strip().strip('"\'')
            print(Fore.YELLOW + f"→ Using saved video link: {link}")
    else:
        link = input(Fore.YELLOW + "\n Paste the video URL to download: ").strip().strip('"\'')
        if not link:
            print(Fore.RED + "No link provided. Exiting.")
            return
        with open(link_file, 'w') as f:
            f.write(link)

    task = detect_task(link)
    print(Fore.CYAN + f"\n Task Detected: {task}")

    os.environ['VIDEO_OUTPUT_PATH'] = output_path
    os.environ['VIDEO_QUALITY'] = quality

    try:
        result = agent.invoke(f"{task}: {link}")
        print(Fore.GREEN + f"\n {result}")
    except Exception as e:
        print(Fore.RED + f"\n Error during download: {e}")

if __name__ == "__main__":
    main()
