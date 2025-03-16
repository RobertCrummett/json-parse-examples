import json

jsonString = '{"name":"Joe","age":42,"scores":[31.4,29.9,35.7],"winner":false}'

# deserialize: parse text into JSON
parsedJson = json.loads(jsonString)
print(parsedJson['name'])

parsedJson['winner'] = True

stringifiedJson = json.dumps(parsedJson)
print(stringifiedJson)
