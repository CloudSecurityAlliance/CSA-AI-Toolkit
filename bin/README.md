# TODO

Finish each major client seperately.

Then determine the commonalities like system prompt, question, etc as per ../README.md

Current plan:

* Wrapper class, command line options, etc.
* CustomGPT utility class (get project id, etc.)
* PromptPerfect class (to improve prompt as an option)
* Output class (meta data and so on)
* Logging class (every persona, prompt, content, result, etc.)
* Prompting classes to get a generated reply
  * ChatGPT4 class
  * ChatGPT Batch class
  * CustomGPT class
  * Claude class
  * Gemini class

So ideally we can easily pass queries through all three AIs with capabilities like PromptPerfect auto-tune as an option.