# Natural langage dataset filter query to json filter
The goal of this repository is to build a prototype Api that take a filter on a dataset in natural langage as input, and provide the transformated query into json filter format as output.

Example of API ability expected: <br>
query: <br>
"One of the top tourist destinations in the United States, San Francisco is known for its steep rolling hills and eclectic mix of architecture across varied neighborhoods, as well as its cool summers, fog, and landmarks, including the Golden Gate Bridge, cable cars, Alcatraz, and Chinatown and Mission districts.[47] The city is home to a number of educational and cultural institutions, such as the University of California, San Francisco, the University of San Francisco, San Francisco State University, the San Francisco Conservatory of Music, the de Young Museum, the San Francisco Museum of Modern Art, the San Francisco Symphony, the San Francisco Ballet, the San Francisco Opera, the SFJAZZ Center, and the California Academy of Sciences. Two professional sports teams, MLB\'s San Francisco Giants, and the NBA\'s Golden State Warriors, all play their home games within San Francisco proper. Transport to, from, and within San Francisco is also among the most robust in the nation, with a main international airport flying to over 125 destinations and a light rail and bus network in tandem with the BART and Caltrain systems connecting nearly every part of San Francisco with the wider region." <br>

response: <br>
```'questions': {
    'text_answer': {
      'question': 'What is the name of the city?',
      'answer': 'San Francisco',
    }, 
    'multiple_choice': {
      'question': 'How are the summer in San Francisco?',
      'choices': ['cool','warm','hot','cold']
    },
    'matching': {
      'question': 'Match the following',
      'matching': [['Stonewall Inn','LGBTQ+ culture'],['Metropolitan Museum of Art','largest art museum'],['Governors Island','climate crisis']]
    }
}```

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
