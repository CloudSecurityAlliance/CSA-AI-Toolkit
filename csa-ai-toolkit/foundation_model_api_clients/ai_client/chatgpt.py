#!/usr/bin/env python3

import os
import openai
import json

def generate_response(model_name, args):
    #
    # FIX THIS!!!!!!! model_name -> model mapping, if chatgpt.... etc?
    #
    model = "gpt-4-0125-preview"
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        raise ValueError("OPENAI_API_KEY environment variable not set.")

    openai.api_key = api_key

    with open(args.system, 'r', encoding='utf-8') as file:
        system_prompt = file.read().strip()

    with open(args.user_prompt, 'r', encoding='utf-8') as file:
        user_prompt = file.read().strip()

    if args.user_data:
        with open(args.user_data, 'r', encoding='utf-8') as file:
            user_data = file.read().strip()
            user_prompt += "\n" + user_data

    completion = openai.chat.completions.create(
        model=model,
        temperature=args.temperature,
        max_tokens=args.max_tokens,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
    )
        
#    completion = openai.ChatCompletion.create(
#        model=model_name,
#        temperature=args.temperature,
#        max_tokens=args.max_tokens,
#        messages=[
#            {"role": "system", "content": system_prompt},
#            {"role": "user", "content": user_prompt}
#        ]
#    )

    response_message = completion.choices[0].message.content

    tokens_input = completion.usage.prompt_tokens
    tokens_output = completion.usage.completion_tokens
    total_tokens = completion.usage.total_tokens

    serialized_completion = {
        "id": completion.id,
        "model": completion.model,
        "created": completion.created,
        "choices": [
            {
                "finish_reason": choice.finish_reason,
                "index": choice.index,
                "message": {
                    "content": choice.message.content,
                    "role": choice.message.role
                }
            } for choice in completion.choices
        ],
        "usage": {
            "prompt_tokens": tokens_input,
            "completion_tokens": tokens_output,
            "total_tokens": total_tokens
        }
    }

    ai_output = {
        "VENDOR": "OpenAI",
        "AIMODEL": model_name,
        "TEMPERATURE": args.temperature,
        "MAXTOKENS": args.max_tokens,
        "TOKENS_INPUT": tokens_input,
        "TOKENS_OUTPUT": tokens_output,
        "COMPLETION": serialized_completion,
        "RESPONSE_TEXT": response_message
    }

    ai_output.update(vars(args))  # Merging argparse arguments

    ai_output = {key: value for key, value in ai_output.items() if value is not None}

    with open(args.output, 'w', encoding='utf-8') as file:
        json.dump(ai_output, file, sort_keys=True, indent=2)

    return response_message
