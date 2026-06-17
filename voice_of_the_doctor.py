import os
import platform
import subprocess
from elevenlabs.client import ElevenLabs
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())
ELEVENLABS_API_KEY = os.environ.get("ELEVENLABS_API_KEY")

#Step1: Setup Text to Speech–TTS–model with gTTS
import os
from gtts import gTTS

def text_to_speech_with_gtts_old(input_text, output_filepath):
    language="en"

    audioobj= gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)


input_text="Hi this is Ai with Anuj!"
# text_to_speech_with_gtts_old(input_text=input_text, output_filepath="gtts_testing.mp3")

#Step1: Setup Text to Speech–TTS–model with ElevenLabs
import elevenlabs
from elevenlabs.client import ElevenLabs

ELEVENLABS_API_KEY=os.environ.get("ELEVEN_API_KEY")

def text_to_speech_with_elevenlabs_old(input_text, output_filepath):
    client=ElevenLabs(api_key=ELEVENLABS_API_KEY)
    audio=client.generate(
        text= input_text,
        voice= "Aria",
        output_format= "mp3_22050_32",
        model= "eleven_turbo_v2"
    )
    elevenlabs.save(audio, output_filepath)

#text_to_speech_with_elevenlabs_old(input_text, output_filepath="elevenlabs_testing.mp3") 

#Step2: Use Model for Text output to Voice

import subprocess
import platform
import os
import subprocess 
import platform
from gtts import gTTS

def text_to_speech_with_gtts(input_text, output_filepath="final.mp3"):
    language = "en"

    # 1. Generate and save the MP3 audio file
    audioobj = gTTS(
        text=input_text,
        lang=language,
        slow=False
    )
    audioobj.save(output_filepath)
    
    
    absolute_path = os.path.abspath(output_filepath)
    os_name = platform.system()
    
    try:
        if os_name == "Darwin":      # macOS 
            subprocess.run(['afplay', absolute_path])
            
        elif os_name == "Windows":   # Windows
            print(" Playing MP3 via Windows Media Subsystem...")
            
            os.system(f'start /min wmplayer "{absolute_path}"')
            
        elif os_name == "Linux":     # Linux
            
            subprocess.run(['mpg123', absolute_path])  
            
        else:
            raise OSError("Unsupported operating system")
            
    except Exception as e:
        print(f"An error occurred while trying to play the audio: {e}")


# if __name__ == "__main__":
#     input_text = "Hi this is Ai with Anuj, autoplay testing!"
#     text_to_speech_with_gtts(input_text=input_text, output_filepath="gtts_testing_autoplay.mp3")


def text_to_speech_with_elevenlabs(input_text, output_filepath="elevenlabs_testing_autoplay.mp3"):
    import os
    import platform
    from dotenv import load_dotenv, find_dotenv
    from elevenlabs.client import ElevenLabs
    
    desktop_folder = os.path.join(os.environ['USERPROFILE'], 'Desktop')
    absolute_output_path = os.path.join(desktop_folder, "elevenlabs_testing_autoplay.mp3")
    
    load_dotenv(find_dotenv())
    api_key = os.environ.get("ELEVENLABS_API_KEY")
    
 
    try:
        client = ElevenLabs(api_key=api_key)
        
        print(f" Requesting stream from ElevenLabs...")
        audio_stream = client.text_to_speech.convert(
            text=input_text,
            voice_id="l7kNoIfnJKPg7779LI2t",  
            output_format="mp3_22050_32",     
            model_id="eleven_flash_v2_5"        
        )
       
        with open(absolute_output_path, "wb") as f:
            for chunk in audio_stream:
                if chunk:
                    f.write(chunk)
                    
        print(f" FILE CREATED AT: {absolute_output_path}")
        
        if platform.system() == "Windows":
            print(" Initializing Windows Audio Output...")
            
            os.system(f'start wmplayer "{absolute_output_path}"')
            
    except Exception as e:
        print(f" Generation Error: {e}")
        
       
        if platform.system() == "Windows":
            print(" ElevenLabs blocked; falling back to local Windows SAPI Voice Engine...")
            import win32com.client
            speaker = win32com.client.Dispatch("SAPI.SpVoice")
            speaker.Speak(input_text)

# Run  function
input_text = "Hello Anuj! your setup are fully completed."
text_to_speech_with_elevenlabs(input_text)