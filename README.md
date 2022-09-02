# Nexus REST Microservice

Stream of Consciousness REST microservice. Nexus of thought for artificial cognition.

- Rapid prototyping. Not for full-scale operations (yet)
- Biomimetic. Models human recall (associative and temporal memory)

Still a work in progress. Will be optimized for scale in the future. New endpoints will be added for different types of recall.

# Add message

- URL: `/add`
- Method: `POST`

### What it does:

- Save payload to `/logs` directory for indexing/storage
- Timestamp and UUID added by Nexus service
- Content and vector are required, others are optional

### Example payload:

```json
{
 "content": "I see a man sitting on a bench",
 "vector": [0,0,0..1,1,1],
 "microservice": "vision",
 "model": "YOLO_v5",
}
```

### Response

- Returns `200` if successful
- Return `500` and error message if unsuccessful

# Semantic search

- URL: `/search`
- Method: `POST`

### What it does:

- Accepts semantic vector and count
- Uses `np.dot` product to find similar vectors
- Returns *n* number of top results

### Example payload:

```json
{
 "vector": [0,0,0..1,1,1],
 "count": 6,
}
```

### Example response:


- Response is a list of dictionaries. 

```json
[
 {"content": "I see a man on a bench"},
 {"content": "I hear a police siren"},
]
```


![Nexus Conceptual Art](https://raw.githubusercontent.com/daveshap/Nexus/main/nexus.jpg)