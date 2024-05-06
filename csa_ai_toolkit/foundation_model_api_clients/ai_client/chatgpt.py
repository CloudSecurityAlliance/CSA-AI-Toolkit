#!/usr/bin/env python3

import os
import openai
import datetime

def generate_response(model_name, api_key, args):

    TIME_START = datetime.datetime.now().isoformat()

    openai.api_key = api_key

    with open(args.system_prompt, 'r', encoding='utf-8') as file:
        system_prompt = file.read().strip()

    with open(args.user_prompt, 'r', encoding='utf-8') as file:
        user_prompt = file.read().strip()

    if args.user_data:
        with open(args.user_data, 'r', encoding='utf-8') as file:
            user_data = file.read().strip()
            user_prompt += "\n" + user_data
    #
    # OpenAI ChatGPT API, https://platform.openai.com/docs/api-reference/chat
    #

    completion = openai.chat.completions.create(
        model=model_name,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )

    TIME_COMPLETE = datetime.datetime.now().isoformat()

    time_start = datetime.datetime.fromisoformat(TIME_START)
    time_complete = datetime.datetime.fromisoformat(TIME_COMPLETE)

    # Calculate the duration
    duration = time_complete - time_start
    TIME_TO_RUN = duration.total_seconds()

    try:
        tokens_input = completion.usage.prompt_tokens
        tokens_output = completion.usage.completion_tokens
        total_tokens = completion.usage.total_tokens
    except AttributeError:
        tokens_input = tokens_output = total_tokens = None
    
    serialized_completion = {
        "id": getattr(completion, 'id', None),
        "model": getattr(completion, 'model', None),
        "created": getattr(completion, 'created', None),
        "system_fingerprint": getattr(completion, 'system_fingerprint', None),
        "choices": [
            {
                "finish_reason": choice.finish_reason,
                "index": choice.index,
                "message": {
                    "content": getattr(choice.message, 'content', None),
                    "role": getattr(choice.message, 'role', None)
                }
            } for choice in getattr(completion, 'choices', [])
        ] if hasattr(completion, 'choices') else [],
        "usage": {
            "prompt_tokens": tokens_input,
            "completion_tokens": tokens_output,
            "total_tokens": total_tokens
        }
    }
    
    try:
        response_message = completion.choices[0].message.content
    except AttributeError:
        response_message = None

    ai_output = {
        "$id": "csa-ai-toolkit-chatgpt-JSON-v1_00",
        "metadata": {
            "system": args.system_prompt,
            "user-prompt": args.user_prompt,
            "user-data": args.user_data,
            "output": args.output_file,                        
            "model_name": model_name,
            "temperature": args.temperature,
            "max_tokens": args.max_tokens,
            "tokens_input": tokens_input,
            "tokens_output": tokens_output,
            "tokens_total": total_tokens,
            "time_start": TIME_START,
            "time_complete": TIME_COMPLETE,
            "time_to_run": TIME_TO_RUN
        },
        "extracted_data": response_message,
        "completion": serialized_completion
    }

    ai_output.update(vars(args))  # Merging argparse arguments

    ai_output = {key: value for key, value in ai_output.items() if value is not None}

    return ai_output#
