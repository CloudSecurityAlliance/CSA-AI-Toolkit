OBSOLETE. PLEASE SEE [CSA AI Tool Setup](https://github.com/CloudSecurityAlliance/CSA-AI-Tool-Setup).

# CSA-AI-Toolkit

This is the CSA AI Toolkit, it's a set of documents, prompts, scripts and programs to help you use AI effectively at the Cloud Security Alliance. These tools are meant for both internal use, and external use, as well as for our communities (e.g. Working Groups, Chapters) and the world in general (much like our open standards such as STARS, CCM, and CAIQ to name a few).

## CSA AI Vendors

This list is not meant to be an endorsement, however the reality is we have a number of AI vendors that we use (you'd be able to figure it out from the scripts and programs). The list is included here for ease of reference:

|Vendor         |Service        |URL                            |API Docs                                                   |Used for   |
|---------------|---------------|-------------------------------|-----------------------------------------------------------|-----------|
|Anthropic      |Claude         |https://claude.ai/             |[Docs](https://docs.anthropic.com/claude/reference/)       |General AI |
|Google         |Gemini         |https://gemini.google.com/     |[Docs](https://ai.google.dev/docs)                         |General AI |
|OpenAI         |ChatGPT        |https://chat.openai.com/       |[Docs](https://platform.openai.com/docs/api-reference)     |General AI |
|OpenAI         |My GPTs        |https://chat.openai.com/gpts   |[Docs](https://platform.openai.com/docs/api-reference)     |RAGBot     |
|CustomGPT      |CustomGPT      |https://app.customgpt.ai/      |[Docs](https://docs.customgpt.ai/)                         |RAGBot     |
|PromptPerfect  |PromptPerfect  |https://promptperfect.jina.ai/ |[Docs](https://promptperfect.jina.ai/api)                  |Prompt optimization and other testing|
|Microsoft      |GitHub CoPilot |https://github.com/features/copilot|N/A (install in VSCode)                                |Coding assistant|
|MeetGeek       |MeetGeek       |https://meetgeek.ai/           |[Coming Soon](https://meetgeek.ai/integrations/uploads-api-webhooks)   |Meeting transcripts and summarization|
|Zapier         |Zapier         |https://zapier.com/            |N/A (see specific AI integrations)                         |Automation and linking of services|

## General AI Client Tools 

The CSA AI Tools follow a relatively common pattern:

* Mandatory:
  * System prompt file
  * Prompt/Question file(s) (these get packed together in order into the input)
  * Additional data file(s) (these get packed together in order into the input)
  * Output file (with meta data)
* Options (with defaults where applicable):
  * Model and version (default is typically the latest one)
  * Temperature (default is creative)
  * Max tokens returned (default is max)
* Metadata as standard at top of file
  * Success or failure, error codes
  * System prompt file, prompt/quesiton file(s), additional data file(s), output file
  * Model and version, temperature, max tokens returned
  * Tokens passed in and tokens passed out

TODO: How do we handle rate limiting? Internally? Spit out an error?
TODO: How do we handle bulk queries? Currently we script it, for i in *.txt, do... sleep 300, done
TODO: OpenAI ChatGPT batch submission tool (https://help.openai.com/en/articles/9197833-batch-api-faq)

We also typically have a creation step (e.g. "create X"), and a validation step (e.g. "check the output for..."). There is also sometimes a repair/enhancement step (e.g. "rewerite the following to be more clear...").

## Existing content to be folded into here:

* https://github.com/CloudSecurityAlliance/CSA-IT-Operations/tree/main/projects/CSA-AI-Project-Assistant
* https://github.com/CloudSecurityAlliance/CSA-IT-Operations/tree/main/projects/AI-Support-Automation
* https://github.com/CloudSecurityAlliance/AI-Prompting

## Strategy

The general strategy is to use a persona (aka systerm prompt), a user prompt (aka question) and typically data. We do three main stages of work with these: creation/transformation, validation, and modification, and at each stage we also have feedback loops so we can make improvements to that stage and previous ones. It should be noted that subtle tweaks to prompts can result in hugely different outcomes, especially across different AI foundation models and AI systems.

This diagram is supposed to be a circle with create, validate and modification on the outside, and persona/prompt/data in the middle:

```mermaid
 graph TD;
  create/transform-->validate;
  validate-->modification;
  modification-->create/transform;

  create/transform-->persona/prompt/data;
  validate-->persona/prompt/data;
  modification-->persona/prompt/data;

  persona/prompt/data-->create/transform;
  persona/prompt/data-->validate;
  persona/prompt/data-->modification;
```

Why we have a modification stage:

While it is possible to modify and improve the prompts used in the creation and transformation, a lot of CSA work can be computationally expensive or difficult to recreate in the AI, having the ability to modify a result and make it better can save us a lot of time and money. Additionally at some point we will want to make transformations to existing work (e.g. "update all mentions of X to include Y"). 
