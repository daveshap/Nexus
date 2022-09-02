# Nexus REST Microservice

Stream of Consciousness REST microservice. Nexus of thought for artificial cognition.

- Rapid prototyping. Not for full-scale operations (yet)
- Biomimetic. Models human recall (associative and temporal memory)

Still a work in progress. Will be optimized for scale in the future. New endpoints will be added for different types of recall.

## Add message

- URL: `/add`
- Method: `POST`

Example payload

- Timestamp and UUID added by Nexus service
- Content and vector are required, others are optional

```json
{
	'content': '<natural language message>',
	'vector': [..],
	'microservice': '<name of originating microservice>',
	'model': '<name or version of model used>',
}
```



![Nexus Conceptual Art](https://raw.githubusercontent.com/daveshap/Nexus/main/nexus.jpg)