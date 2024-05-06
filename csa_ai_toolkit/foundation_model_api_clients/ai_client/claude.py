#!/usr/bin/env python3

import os
import anthropic
import datetime

def generate_response(model_name, api_key, args):

    TIME_START = datetime.datetime.now().isoformat()
    
#    claude_api_key = os.getenv('ANTHROPIC_API_KEY')
#    if not claude_api_key:
#        raise ValueError("ANTHROPIC_API_KEY environment variable not set.")

    client = anthropic.Anthropic(api_key=api_key)

    with open(args.system_prompt, 'r', encoding='utf-8') as file:
        system_prompt = file.read().strip()

    with open(args.user_prompt, 'r', encoding='utf-8') as file:
        user_prompt = file.read().strip()

    if args.user_data:
        with open(args.user_data, 'r', encoding='utf-8') as file:
            user_data = file.read().strip()
            user_prompt += "\n" + user_data
    #
    # Anthropic Claude API, https://docs.anthropic.com/claude/reference/messages_post
    #

    completion = client.messages.create(
        model=model_name,        
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        system=system_prompt,
        messages=[
            {"role": "user", "content": user_prompt}
        ],
    )

    TIME_COMPLETE = datetime.datetime.now().isoformat()

    time_start = datetime.datetime.fromisoformat(TIME_START)
    time_complete = datetime.datetime.fromisoformat(TIME_COMPLETE)

    # Calculate the duration
    duration = time_complete - time_start
    TIME_TO_RUN = duration.total_seconds()

    try:
        tokens_input = completion.usage.input_tokens
        tokens_output = completion.usage.output_tokens
        total_tokens = completion.usage.input_tokens + completion.usage.output_tokens
    except AttributeError:
        tokens_input = tokens_output = total_tokens = None
    
    #
    # TODO: Handle "content": [
    #{
    #  "type": "text",
    #  "text": "Hello!"
    #}
    #],
    #
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
        "$id": "csa-ai-toolkit-claude-JSON-v1_00",
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

    return ai_output
