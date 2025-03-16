const jsonString = '{"name":"Joe","age":42,"scores":[31.4,29.9,35.7],"winner":false}'
// deserialize: parse text into JSON
const parsedJson = JSON.parse(jsonString)
console.log(parsedJson.name)

parsedJson.winner = true

const stringifiedJson = JSON.stringify(parsedJson)
console.log(stringifiedJson)

const formattedJson = JSON.stringify(parsedJson, null, 2)
console.log(formattedJson)
