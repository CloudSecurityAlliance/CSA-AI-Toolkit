# TODO

Finish each major client seperately.

Then determine the commonalities like system prompt, question, etc as per ../README.md

Current plan:

* Wrapper class, command line options, etc.
* Prompting classes to get a generated reply (INPUT: system prompt, user prompt, user data, model, temperature, max_tokens. OUTPUT: VENDOR, RUNTIME, SCRIPTNAME, AIMODEL, TEMPERATURE, MAXTOKENS, TOKENS_INPUT, TOKENS_OUTPUT, COMPLETION, RESPONSE_TEXT, COMMAND_LINE)
  * ChatGPT4 class
  * ChatGPT Batch class
  * CustomGPT class
  * Claude class
  * Gemini class
* Output class (meta data and so on)
* Logging class (every persona, prompt, content, result, etc.)
* PromptPerfect class (to improve prompt as an option)
* CustomGPT utility class (get project id, etc.)

So ideally we can easily pass queries through all three AIs with capabilities like PromptPerfect auto-tune as an option.

