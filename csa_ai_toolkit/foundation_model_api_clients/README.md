# Notes, todo, etc.

## Testing

To test ChatGPT4:

```
./main.py --system ../../test/PERSONA-2024-04-19-000001.txt --user-prompt ../../test/QUESTION-2024-04-19-000002.txt --user-data ../../test/Unused.md --output output.json  --model chatgpt
```

To test Claude 3:

```
./main.py --system ../../test/PERSONA-2024-04-19-000001.txt --user-prompt ../../test/QUESTION-2024-04-19-000002.txt --user-data ../../test/Unused.md --output output-claude.json  --model claude-opus
```

## TODO

* Add error handling if completion reason is NOT stop or equivalent
* Add error handling if HTTP error code
* Add reporting tool to read JSON files and calculate tokens/minute/hour usage?

