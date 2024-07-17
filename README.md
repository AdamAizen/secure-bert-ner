# secure-bert-ner
SecureBERT-NER model running on a docker container

## Documentation

### Overview
The SecureBERT-NER model is a domain-specific NER (Named Entity Recognition) model for predicting entities from plain English text as well as cybersecurity-related text, utilizing a customized tokenizer.

This implementation is meant to run locally as a http server on a docker container, and is expecting to receive plain text in the a string format.

### Example usage

#### Pull docker image
To use the SecureBERT-NER model, one must pull the securebert-ner-server image from Docker Hub as in the following example:

Pull the docker image from Docker Hub:
docker pull adamaizen/securebert-ner-server

#### Run model on local machine
In order to run the docker image locally, follow the next example:

#### Run the docker container locally:
docker run -p 5000:5000 securebert-ner-server

#### Send http request
Here is an example text that could be sent to the SecureBERT-NER model:
"These emails included recruitment-themed lures and links to malicious HTML application ( HTA ) files. APT34 often uses compromised accounts to conduct spear-phishing operations. APT33 leverages a mix of public and non-public tools and often conducts spear-phishing operations using a built-in phishing module from \"ALFA TEaM Shell\", a publicly available web shell." 

In order to send this text to the SecureBERT-NER model, use the Python requests library or as in the following example, use the command line ‘curl’ utility with a POST method:

#### Send text to model with curl:
curl -X POST http://localhost:5000/ner -H "Content-Type: application/json" -d '{"text": "These emails included recruitment-themed lures and links to malicious HTML application ( HTA ) files. APT34 often uses compromised accounts to conduct spear-phishing operations. APT33 leverages a mix of public and non-public tools and often conducts spear-phishing operations using a built-in phishing module from \"ALFA TEaM Shell\", a publicly available web shell."}'

The expected result set should look like this:
{"predictions": [[{"word": "These", "entity": "O"}, {"word": "emails", "entity": "B-TOOL"}, {"word": "included", "entity": "O"}, {"word": "recruitment", "entity": "B-ACT"}, {"word": "-", "entity": "B-ACT"}, {"word": "themed", "entity": "B-ACT"}, {"word": "lures", "entity": "I-ACT"}, {"word": "and", "entity": "O"}, {"word": "links", "entity": "O"}, 
…, 
{"word": "AL", "entity": "B-MAL"}, {"word": "FA", "entity": "B-MAL"}, {"word": "TE", "entity": "I-MAL"}, {"word": "aM", "entity": "I-MAL"}, {"word": "Shell", "entity": "I-MAL"}, {"word": "\",", "entity": "O"}, {"word": "a", "entity": "O"}, {"word": "publicly", "entity": "B-MAL"}, {"word": "available", "entity": "I-MAL"}, {"word": "web", "entity": "I-MAL"}, {"word": "shell", "entity": "I-MAL"}, {"word": ".", "entity": "O"}]], "latency": 0.5695114135742188, "Content-Type": "application/json"}

### Limitations
The server is limited to text files no larger than 1MB.

