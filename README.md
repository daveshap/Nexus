# Nexus REST Microservice

Stream of Consciousness REST microservice. Nexus of thought. We can already solve many problems that deal with cognition; recall, planning, and execution. What we need is a way to integrate it all together. 

- Scalable. Receive and serve messages to/from arbitrary services
- Biomimetic. Models working memory aspect of cognition
- Multimodal. Integrate information from disparate sources, such as sight, sound, long term memory, encyclopedic knowledge, etc.

# Usage

## Adding Messages

Use HTTP POST to register new messages at the root endpoint `/`. New message must be a JSON object with the following keys:

| Key | Explanation | Examples |
|---|---|---|
| msg | Plain English message containing a single "thought" | `I see a dog`, `David said: Go to the store and get some milk` |
| key | Taxonomical key, similar to routing key used in AMQP. Metadata of the message. | `input.audio.speech.David`, `processing.memory.episodic` |
| sid | Service ID. Unique identifier for source service. Allows for accountability, self identification, version control, investigation, filtration, etc | `c64c2e57-adf2-4602-85ee-ba09185c37c3`, `ASR_QuantumQuintus_v14.0.23444` |

The Nexus service will add two more keys to each message: `mid` and `time`. Time is UNIX epoch timestamp. Mid is Message ID, a UUID assigned to each message. This allows for other messages to definitively reference each other. 

For instance, let's say an action generating service proposes the action `Pet the dog` in response to the `I see a dog` message. Evaluation services can trace the series of messages, stream of consciousness, that resulted in a given action recommendation.

## Fetching Messages

Use HTTP GET to fetch messages at the root endpoint `/`. Use argument parameters to filter messages. Accepted arguments are:

| Argument | Explanation |
|---|---|
| `keyword` | Search term that must be present in message to return. Searches entire message, including metadata |
| `start` | Filter out any messages occuring before this filter |
| `end` | Filter out any messages occurring after this filter |

Example: `GET http://nexus:9999/?keyword=dog&start=1095379199&end=1095384199`

Each argument is optional but recommended. Reducing query size can increase performance and reduce noise. 

## Best Practices

- Do not use Nexus for raw data (image, audio, accelerometer, etc)
- Use Nexus only for highest order cognition, thought, planning, and contemplation - ask the big questions. 
- Services should keep track of their own requests, only requesting exactly what they need instead of everything
- Services should be responsible with their posting of new messages. They should only POST when they have something meaningful to add. 
- Services should do one thing, and do it well. 

# Services

## Types

Non-exhaustive list of types of services:

- Automatic Speech Recognition (ASR)
- Object detection
- Long term retention (recall)
- Encyclopedic knowledge
- Action recommendation generator
- Moral and ethical evaluation
- Motor action execution
- Speech generation