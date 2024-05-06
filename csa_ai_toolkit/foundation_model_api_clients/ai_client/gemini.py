#!/usr/bin/env python3
import os
import google.generativeai as genai
from google.generativeai import types
import datetime
import json

def generate_response(model_name, api_key, args):
    
    TIME_START = datetime.datetime.now().isoformat()
#    api_key = os.getenv('GOOGLE_API_KEY')
#    if not api_key:
#        raise ValueError("GOOGLE_API_KEY environment variable not set.")

    genai.configure(api_key=api_key)

    with open(args.system_prompt, 'r', encoding='utf-8') as file:
        system_prompt = file.read().strip()

    with open(args.user_prompt, 'r', encoding='utf-8') as file:
        user_prompt = file.read().strip()

    if args.user_data:
        with open(args.user_data, 'r', encoding='utf-8') as file:
            user_data = file.read().strip()
        user_prompt += "\n" + user_data

    #########################################################
    gemini_model = genai.GenerativeModel(model_name)

    prompt_sequence = [
        system_prompt,
        "Understood.",
        user_prompt
    ]

    responses = []
    config = types.GenerationConfig(
        candidate_count=1,
        max_output_tokens=args.max_tokens,
        temperature=args.temperature
    )

    #
    # Faking system prompt for now
    #
    for text in prompt_sequence:
        response = gemini_model.generate_content(text, generation_config=config)
        responses.append(response.text)

#    try:
# 
#
#    except Exception as e:
#        print(f"Error during API call: {e}")
#        return None
    #########################################################

    TIME_COMPLETE = datetime.datetime.now().isoformat()
    time_start = datetime.datetime.fromisoformat(TIME_START)
    time_complete = datetime.datetime.fromisoformat(TIME_COMPLETE)
    # Calculate the duration
    duration = time_complete - time_start
    TIME_TO_RUN = duration.total_seconds()

    # Prepare the response output
    ai_output = {
        "$id": "csa-ai-toolkit-gemini-JSON-v1_00",
        "metadata": {
            "system": args.system_prompt,
            "user-prompt": args.user_prompt,
            "user-data": args.user_data,
            "output": args.output_file,
            "model_name": model_name,
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
            "time_start": TIME_START,
            "time_complete": TIME_COMPLETE,
            "time_to_run": TIME_TO_RUN
        },
        "response": responses,
        "extracted_data": response.text
    }

    ai_output.update(vars(args))  # Merging argparse arguments
    ai_output = {key: value for key, value in ai_output.items() if value is not None}

    return ai_output