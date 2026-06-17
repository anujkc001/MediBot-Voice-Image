# VoiceBot
import os
import gradio as gr
from brain_of_the_doctor import encode_image, analyze_image_with_query
from voice_of_the_patient import record_audio, transcribe_with_groq
from voice_of_the_doctor import text_to_speech_with_gtts

# system prompt 
SYSTEM_PROMPT = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
            What's in this image?. Do you find anything wrong with it medically? 
            If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
            your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
            Donot say 'In the image I see' but say 'With what I see, I think you have ....'
            Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
            Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

def process_inputs(audio_filepath, image_filepath):
    if not audio_filepath:
        return "No audio recorded yet.", "Please provide an image and speak to the doctor.", None

    try:
        speech_to_text_output = transcribe_with_groq(
            GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
            audio_filepath=audio_filepath,
            stt_model="whisper-large-v3"
        )
    except Exception as e:
        speech_to_text_output = f"Transcription failed: {e}"

    if image_filepath:
        try:
            print(f" Live Processing NEW Uploaded File Path: {image_filepath}")
            
           
            fresh_encoded_image = encode_image(image_filepath)
            
            
            combined_query = f"{SYSTEM_PROMPT}\n\nPatient Query: {speech_to_text_output}"
            
            
            doctor_response = analyze_image_with_query(
                query=combined_query, 
                encoded_image=fresh_encoded_image, 
                model="meta-llama/llama-4-scout-17b-16e-instruct"
            )
        except Exception as e:
            doctor_response = f"Vision model processing failed: {e}"
    else:
        doctor_response = "Please upload an image for a complete medical diagnostic evaluation."


    output_audio_filename = "final.mp3"
    text_to_speech_with_gtts(input_text=doctor_response, output_filepath=output_audio_filename) 

    if 'fresh_encoded_image' in locals():
        del fresh_encoded_image

    return speech_to_text_output, doctor_response, output_audio_filename


iface = gr.Interface(
    fn=process_inputs,
    inputs=[
        gr.Audio(sources=["microphone"], type="filepath", label="Patient Speech Input"),
        gr.Image(type="filepath", label="Medical Image/Symptom Upload") 
    ],
    outputs=[
        gr.Textbox(label="Speech to Text"),
        gr.Textbox(label="Doctor's Response"),
        gr.Audio(label="Doctor's Voice Output")
    ],
    title="AI Doctor with Vision and Voice"
)

if __name__ == "__main__":
    iface.launch(debug=True)