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






    
# # ############################################################################################################
# import gradio as gr
# import spaces
# import torch

# # zero = torch.Tensor([0]).cuda()
# device = "cuda" if torch.cuda.is_available() else "cpu"
# zero = torch.Tensor([0]).to(device)
# print(zero.device) # <-- 'cpu' 

# @spaces.GPU
# def greet(n):
#     print(zero.device) # <-- 'cuda:0' 
#     return f"Hello {zero + n} Tensor"

# demo = gr.Interface(fn=greet, inputs=gr.Number(), outputs=gr.Text())
# demo.launch()
# # # #####################################################################
# # import os
# # import gradio as gr

# # # Import custom project modules with fallback mechanisms for testing
# # try:
# #     from brain_of_the_doctor import encode_image, analyze_image_with_query
# #     from voice_of_the_patient import transcribe_with_groq
# #     from voice_of_the_doctor import text_to_speech_with_gtts
# # except ImportError:
# #     # Fallback mock handlers for standalone execution testing
# #     def encode_image(image_path):
# #         return "mock_base64_encoded_image_string"

# #     def analyze_image_with_query(query, encoded_image, model):
# #         return "With what I see, I think you have mild localized dermatitis and you should apply a soothing moisturizer and monitor for changes."

# #     def transcribe_with_groq(GROQ_API_KEY, audio_filepath, stt_model):
# #         return "Patient reported skin redness and mild itching for two days."

# #     def text_to_speech_with_gtts(input_text, output_filepath):
# #         with open(output_filepath, "wb") as f:
# #             f.write(b"")
# #         return output_filepath

# # SYSTEM_PROMPT = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
# # What's in this image?. Do you find anything wrong with it medically? 
# # If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
# # your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
# # Donot say 'In the image I see' but say 'With what I see, I think you have ....'
# # Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
# # Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

# # def handle_audio_submission(audio_filepath):
# #     """
# #     Transcribes patient recorded audio when the user explicitly clicks 'Submit Recorded Audio'.
# #     """
# #     if not audio_filepath:
# #         return "No audio recorded yet. Please record your voice first."

# #     api_key = os.environ.get("GROQ_API_KEY")
# #     if not api_key:
# #         return "Error: GROQ_API_KEY environment variable is not set. Please set GROQ_API_KEY."

# #     try:
# #         transcription = transcribe_with_groq(
# #             GROQ_API_KEY=api_key, 
# #             audio_filepath=audio_filepath,
# #             stt_model="whisper-large-v3"
# #         )
# #         return transcription
# #     except Exception as e:
# #         return f"Transcription failed: {str(e)}"

# # def handle_full_analysis(transcribed_text, image_filepath):
# #     """
# #     Processes the image along with transcribed voice text to generate doctor diagnosis and TTS audio.
# #     """
# #     if not image_filepath:
# #         return "Please upload an image for a complete medical diagnostic evaluation.", None

# #     # Handle missing or error transcription text gracefully
# #     if not transcribed_text or transcribed_text.startswith("No audio recorded") or transcribed_text.startswith("Error:"):
# #         combined_query = SYSTEM_PROMPT
# #     else:
# #         combined_query = f"{SYSTEM_PROMPT}\n\nPatient Query: {transcribed_text}"

# #     try:
# #         # Encode uploaded image
# #         fresh_encoded_image = encode_image(image_filepath)
        
# #         # Request vision model evaluation
# #         doctor_response = analyze_image_with_query(
# #             query=combined_query, 
# #             encoded_image=fresh_encoded_image, 
# #             model="meta-llama/llama-4-scout-17b-16e-instruct"
# #         )
# #     except Exception as e:
# #         doctor_response = f"Vision model processing failed: {str(e)}"

# #     # Generate text-to-speech doctor voice output
# #     output_audio_filename = "final.mp3"
# #     try:
# #         text_to_speech_with_gtts(input_text=doctor_response, output_filepath=output_audio_filename)
# #     except Exception as e:
# #         print(f"TTS warning: {e}")

# #     return doctor_response, output_audio_filename

# # with gr.Blocks(title="AI Doctor with Vision and Voice", theme=gr.themes.Soft()) as demo:
# #     gr.Markdown(
# #         """
# #         # 🩺 MediBot - AI Doctor with Vision and Voice
# #         Record your speech, click **Submit Recorded Audio** to preview your transcribed query, upload a medical image, and generate an AI Doctor analysis with spoken audio output.
# #         """
# #     )

# #     with gr.Row():
# #         # --- LEFT COLUMN: PATIENT INPUTS ---
# #         with gr.Column(scale=1):
# #             gr.Markdown("###  Step 1: Live Voice Input")
# #             audio_input = gr.Audio(
# #                 sources=["microphone"], 
# #                 type="filepath", 
# #                 label="Patient Speech Input"
# #             )
            
# #             # Dedicated Submit Recorded Audio Button
# #             submit_audio_btn = gr.Button(" Submit Recorded Audio", variant="secondary")
            
# #             transcribed_text_box = gr.Textbox(
# #                 label="Speech to Text Result", 
# #                 placeholder="Click 'Submit Recorded Audio' to process your voice input...", 
# #                 lines=3
# #             )

# #             gr.Markdown("###  Step 2: Medical Image Upload")
# #             image_input = gr.Image(
# #                 type="filepath", 
# #                 label="Medical Image/Symptom Upload"
# #             )

# #             generate_analysis_btn = gr.Button("🔬 Generate Doctor Analysis", variant="primary", size="lg")

# #         # --- RIGHT COLUMN: DOCTOR OUTPUTS ---
# #         with gr.Column(scale=1):
# #             gr.Markdown("###  Step 3: Doctor Response")
# #             doctor_response_box = gr.Textbox(
# #                 label="Doctor's Response", 
# #                 lines=6, 
# #                 interactive=False
# #             )
# #             doctor_audio_output = gr.Audio(
# #                 label="Doctor's Voice Output", 
# #                 interactive=False
# #             )

# #             gr.Markdown(
# #                 """
# #                 >  **Disclaimer:** This system is for educational purposes only and should not replace professional medical advice.
# #                 """
# #             )

# #     submit_audio_btn.click(
# #         fn=handle_audio_submission,
# #         inputs=[audio_input],
# #         outputs=[transcribed_text_box]
# #     )

# #     generate_analysis_btn.click(
# #         fn=handle_full_analysis,
# #         inputs=[transcribed_text_box, image_input],
# #         outputs=[doctor_response_box, doctor_audio_output]
# #     )

# # if __name__ == "__main__":
# #     demo.launch(debug=True)


# #################################################################################??????????????????????????????###################################

# # import os
# # import gradio as gr
# # from brain_of_the_doctor import encode_image, analyze_image_with_query
# # from voice_of_the_patient import transcribe_with_groq
# # from voice_of_the_doctor import text_to_speech_with_gtts

# # # system prompt 
# # SYSTEM_PROMPT = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
# #             What's in this image?. Do you find anything wrong with it medically? 
# #             If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
# #             your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
# #             Donot say 'In the image I see' but say 'With what I see, I think you have ....'
# #             Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
# #             Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

# # def process_inputs(audio_filepath, image_filepath):
# #     if not audio_filepath:
# #         return "No audio provided.", "Please speak or upload an audio file and provide an image.", None

# #     try:
# #         speech_to_text_output = transcribe_with_groq(
# #             GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
# #             audio_filepath=audio_filepath,
# #             stt_model="whisper-large-v3"
# #         )
# #     except Exception as e:
# #         speech_to_text_output = f"Transcription failed: {e}"

# #     if image_filepath:
# #         try:
# #             print(f" Live Processing NEW Uploaded File Path: {image_filepath}")
            
# #             fresh_encoded_image = encode_image(image_filepath)
            
# #             combined_query = f"{SYSTEM_PROMPT}\n\nPatient Query: {speech_to_text_output}"
            
# #             doctor_response = analyze_image_with_query(
# #                 query=combined_query, 
# #                 encoded_image=fresh_encoded_image, 
# #                 model="meta-llama/llama-4-scout-17b-16e-instruct"
# #             )
# #         except Exception as e:
# #             doctor_response = f"Vision model processing failed: {e}"
# #     else:
# #         doctor_response = "Please upload an image for a complete medical diagnostic evaluation."

# #     output_audio_filename = "final.mp3"
# #     text_to_speech_with_gtts(input_text=doctor_response, output_filepath=output_audio_filename) 

# #     if 'fresh_encoded_image' in locals():
# #         del fresh_encoded_image

# #     return speech_to_text_output, doctor_response, output_audio_filename


# # iface = gr.Interface(
# #     fn=process_inputs,
# #     inputs=[
# #         # Updated to include both live microphone recording and audio file upload options
# #         gr.Audio(sources=["microphone", "upload"], type="filepath", label="Patient Audio Input (Record Live or Upload Audio)"),
# #         gr.Image(type="filepath", label="Medical Image/Symptom Upload") 
# #     ],
# #     outputs=[
# #         gr.Textbox(label="Speech to Text"),
# #         gr.Textbox(label="Doctor's Response"),
# #         gr.Audio(label="Doctor's Voice Output")
# #     ],
# #     title="AI Doctor with Vision and Voice"
# # )

# # if __name__ == "__main__":
# #     iface.launch(debug=True)








# #########################NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN######################################
# import os
# import torch
# import gradio as gr
# from brain_of_the_doctor import encode_image, analyze_image_with_query
# from voice_of_the_patient import transcribe_with_groq
# from voice_of_the_doctor import text_to_speech_with_gtts

# # Safe PyTorch Device setup (Supports both GPU and CPU without crashing)
# device = "cuda" if torch.cuda.is_available() else "cpu"

# # System prompt 
# SYSTEM_PROMPT = """You have to act as a professional doctor, i know you are not but this is for learning purpose. 
#             What's in this image?. Do you find anything wrong with it medically? 
#             If you make a differential, suggest some remedies for them. Donot add any numbers or special characters in 
#             your response. Your response should be in one long paragraph. Also always answer as if you are answering to a real person.
#             Donot say 'In the image I see' but say 'With what I see, I think you have ....'
#             Dont respond as an AI model in markdown, your answer should mimic that of an actual doctor not an AI bot, 
#             Keep your answer concise (max 2 sentences). No preamble, start your answer right away please"""

# def process_inputs(audio_filepath, image_filepath):
#     if not audio_filepath:
#         return "No audio provided.", "Please speak or upload an audio file and provide an image.", None

#     try:
#         speech_to_text_output = transcribe_with_groq(
#             GROQ_API_KEY=os.environ.get("GROQ_API_KEY"), 
#             audio_filepath=audio_filepath,
#             stt_model="whisper-large-v3"
#         )
#     except Exception as e:
#         speech_to_text_output = f"Transcription failed: {e}"

#     if image_filepath:
#         try:
#             print(f"Processing Uploaded Image File Path: {image_filepath}")
            
#             fresh_encoded_image = encode_image(image_filepath)
#             combined_query = f"{SYSTEM_PROMPT}\n\nPatient Query: {speech_to_text_output}"
            
#             doctor_response = analyze_image_with_query(
#                 query=combined_query, 
#                 encoded_image=fresh_encoded_image, 
#                 model="meta-llama/llama-4-scout-17b-16e-instruct"
#             )
#         except Exception as e:
#             doctor_response = f"Vision model processing failed: {e}"
#     else:
#         doctor_response = "Please upload an image for a complete medical diagnostic evaluation."

#     output_audio_filename = "final.mp3"
#     text_to_speech_with_gtts(input_text=doctor_response, output_filepath=output_audio_filename) 

#     if 'fresh_encoded_image' in locals():
#         del fresh_encoded_image

#     return speech_to_text_output, doctor_response, output_audio_filename


# iface = gr.Interface(
#     fn=process_inputs,
#     inputs=[
#         gr.Audio(sources=["microphone", "upload"], type="filepath", label="Patient Audio Input (Record Live or Upload Audio)"),
#         gr.Image(type="filepath", label="Medical Image/Symptom Upload") 
#     ],
#     outputs=[
#         gr.Textbox(label="Speech to Text"),
#         gr.Textbox(label="Doctor's Response"),
#         gr.Audio(label="Doctor's Voice Output")
#     ],
#     title="AI Doctor with Vision and Voice"
# )

# if __name__ == "__main__":
#     iface.launch(debug=True)