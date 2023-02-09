# Natural langage dataset filter query to json filter
The goal of this repository is to build a prototype Api that take a filter on a dataset in natural langage as input, and provide the transformated query into json filter format as output.

Example of API ability expected: <br>
query: <br>
"Show me all conference rooms that were used more than 40% of the time in December 2022" <br>
response: <br>
{
  "function": "meeting_room",
  "time_used_percent": { "min": 0.4 },
  "local_date": { "min": "2022-12-01", "max": "2022-12-31" }
}

## Requirements
An OpenAI API key (sign up at https://beta.openai.com/signup and create an api key at https://beta.openai.com/account/api-keys) <br>
Then set the OPENAI_API_KEY env var with it: OPENAI_API_KEY="my api key"

## Setup
### Local
#### Requirements
python >=3.7
#### Installation
Run this command to install python dependencies:
```
pip install -r requirements.txt
```

#### Running
Run this command to start the server:
```
python server.py
```

### Docker
#### Build image
Run this command to build the backend-gpt docker image:
```
make docker-build
```

#### Run container
Run this command to start the server in a container:
```
docker run -p 5000:5000 -e OPENAI_API_KEY=$OPENAI_API_KEY backend-gpt
```

## Experiment
Now you can test the API:
- with the frontend at http://127.0.0.1:5000
- directly with curl like that:
```
curl -H "Content-Type: application/json" -X POST --data '{"user_input": "Meeting room only"}' localhost:5000/json_filter
```

## Experiment directly with python interpreter:
```
python json_filter_bot.py
```
