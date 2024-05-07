# Notes, todo, etc.

## import:

```
from csa_ai_toolkit.foundation_model_api_clients import FoundationModelClient
```

## Testing

To test ChatGPT4:

```
./main.py --model chatgpt \
	  --system ../../test/PERSONA-2024-04-19-000001.txt \
	  --user-prompt ../../test/QUESTION-2024-04-19-000002.txt \
	  --user-data ../../test/Unused.md \
	  --output output-chatgpt.json 
```

To test Claude 3:

```
./main.py --model claude-opus \
	  --system ../../test/PERSONA-2024-04-19-000001.txt \
	  --user-prompt ../../test/QUESTION-2024-04-19-000002.txt \
	  --user-data ../../test/Unused.md \
	  --output output-claude.json 
```

To test Gemini 1.5:

```
./main.py --model gemini \
	  --system ../../test/PERSONA-2024-04-19-000001.txt \
	  --user-prompt ../../test/QUESTION-2024-04-19-000002.txt \
	  --user-data ../../test/Unused.md \
	  --output output-gemini.json 
```

## TODO

* Add error handling if completion reason is NOT stop or equivalent
* Add error handling if HTTP error code
* Add reporting tool to read JSON files and calculate tokens/minute/hour usage?
* Add ChatGPT --batch wrapper (query, submit, retrieve)
