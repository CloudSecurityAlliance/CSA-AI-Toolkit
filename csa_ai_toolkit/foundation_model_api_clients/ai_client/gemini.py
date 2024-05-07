#!/usr/bin/env python3

# Weird spacing so all three files line up in an editor

import google.generativeai as genai
from google.generativeai import types

import datetime

def generate_response(model_name, api_key, system_prompt, user_prompt, args):

    TIME_START = datetime.datetime.now().isoformat()

    #
    # Google Gemini Python: https://ai.google.dev/gemini-api/docs/get-started/python
    #

    genai.configure(api_key=api_key)

    gemini_model = genai.GenerativeModel(
        model_name=model_name,
        system_instruction=system_prompt
        )

    config = types.GenerationConfig(
        candidate_count=1,
        max_output_tokens=args.max_tokens,
        temperature=args.temperature
    )

    response = gemini_model.generate_content(user_prompt, generation_config=config)

    TIME_FINISHED = datetime.datetime.now().isoformat()

    time_start = datetime.datetime.fromisoformat(TIME_START)
    time_complete = datetime.datetime.fromisoformat(TIME_FINISHED)

    # Calculate the duration
    duration = time_complete - time_start
    TIME_TO_RUN = duration.total_seconds()

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
            "time_complete": TIME_FINISHED,
            "time_to_run": TIME_TO_RUN
        },
        #"response": response,
        "extracted_data": response.text
    }

    ai_output.update(vars(args))  # Merging argparse arguments
    ai_output = {key: value for key, value in ai_output.items() if value is not None}

    return ai_output