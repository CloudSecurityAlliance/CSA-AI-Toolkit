# Output formats

## ChatGPT

https://platform.openai.com/docs/api-reference/chat/object

```
{
  "id": "chatcmpl-123",
  "object": "chat.completion",
  "created": 1677652288,
  "model": "gpt-3.5-turbo-0125",
  "system_fingerprint": "fp_44709d6fcb",
  "choices": [{
    "index": 0,
    "message": {
      "role": "assistant",
      "content": "\n\nHello there, how may I assist you today?",
    },
    "logprobs": null,
    "finish_reason": "stop"
  }],
  "usage": {
    "prompt_tokens": 9,
    "completion_tokens": 12,
    "total_tokens": 21
  }
}
```

## Claude

https://docs.anthropic.com/claude/reference/messages_post

```
{
  "id": "msg_013Zva2CMHLNnXjNJJKqJ2EF",
  "content": [
    {
      "text": "Hi! My name is Claude.",
      "type": "text"
    }
  ],
  "model": "claude-3-opus-20240229",
  "stop_reason": "end_turn",
  "stop_sequence": "string",
  "usage": {
    "input_tokens": 10,
    "output_tokens": 25
  }
}
```

## Gemini

https://ai.google.dev/api/python/google/generativeai/types/ChatResponse ???????

https://github.com/google-gemini/generative-ai-python/blob/v0.3.0/google/generativeai/types/discuss_types.py

```
        result = {
            "model": self.model,
            "context": self.context,
            "examples": self.examples,
            "messages": self.messages,
            "temperature": self.temperature,
            "candidate_count": self.candidate_count,
            "top_p": self.top_p,
            "top_k": self.top_k,
            "candidates": self.candidates,
        }
```

TODO: Dump a raw actual response.