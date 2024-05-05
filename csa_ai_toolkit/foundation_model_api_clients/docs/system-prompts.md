# System and user prompts 

## ChatGPT

https://platform.openai.com/docs/api-reference/chat/create

```
messages=[
    {"role": "system", "content": system_prompt},
    {"role": "user", "content": user_prompt}
]
```

## Claude

https://docs.anthropic.com/claude/docs/system-prompts

```
system=system_prompt,
messages=[
    {"role": "user", "content": user_prompt}
]
```

## Gemini

https://ai.google.dev/gemini-api/docs/system-instructions

```
model=genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction="You are a cat. Your name is Neko.")
```