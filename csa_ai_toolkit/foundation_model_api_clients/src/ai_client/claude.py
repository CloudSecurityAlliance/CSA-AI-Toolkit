#!/usr/bin/env python3

# Weird spacing so all three files line up in an editor

import anthropic


import datetime

def generate_response(model_name, api_key, system_prompt, user_prompt, args):

    TIME_START = datetime.datetime.now().isoformat()

    #
    # Anthropic Claude API: https://docs.anthropic.com/claude/reference/messages_post
    #
        
    client = anthropic.Anthropic(api_key=api_key)

    completion = client.messages.create(
        model=model_name,        
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ],
    )




    TIME_FINISHED = datetime.datetime.now().isoformat()

    time_start = datetime.datetime.fromisoformat(TIME_START)
    time_complete = datetime.datetime.fromisoformat(TIME_FINISHED)

    # Calculate the duration
    duration = time_complete - time_start
    TIME_TO_RUN = duration.total_seconds()

    try:
        tokens_input = completion.usage.input_tokens
        tokens_output = completion.usage.output_tokens
        total_tokens = completion.usage.input_tokens + completion.usage.output_tokens
    except AttributeError:
        tokens_input = tokens_output = total_tokens = None
    
    serialized_completion = {
        "id": getattr(completion, 'id', None),
        "model": getattr(completion, 'model', None),
        "stop_reason": completion.stop_reason,
        "usage": {
            "prompt_tokens": tokens_input,
            "completion_tokens": tokens_output,
            "total_tokens": total_tokens
        }
    }

    try:
        response_message = completion.content[0].text
    except AttributeError:
        response_message = None

    ai_output = {
        "$id": "csa-ai-toolkit-anthropic-claude3-JSON-v1_00",
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
            "time_complete": TIME_FINISHED,
            "time_to_run": TIME_TO_RUN
        },
        "extracted_data": response_message,
        "completion": serialized_completion
    }

    ai_output.update(vars(args))  # Merging argparse arguments

    ai_output = {key: value for key, value in ai_output.items() if value is not None}

    return ai_output
