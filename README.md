# Nexus REST Microservice

Stream of Consciousness REST microservice. Nexus of thought for artificial cognition.

- Rapid prototyping. Not for full-scale operations (yet)
- Biomimetic. Models human recall (associative and temporal memory)

Still a work in progress. Will be optimized for scale in the future. New endpoints will be added for different types of recall.

![Nexus Conceptual Art](https://raw.githubusercontent.com/daveshap/Nexus/main/nexus.jpg)

## TODO List

1. Firm up required endpoints (I think we're closing in on this)
2. Integrate blockchain for security
3. Integrate semantic search for speed
4. Integrate knowledge graph for speed

# Add message

- URL: `/add`
- Method: `POST`

### What it does:

- Add a memory to the nexus
- Save JSON payload to `/logs` directory for indexing/storage
- Timestamp and UUID added by Nexus service
- Content and vector are required, others are optional

### Example payload:

```json
{
 "content": "I see a man sitting on a bench",
 "vector": [0,0,0,1,1,1],
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
 "vector": [0,0,0,1,1,1],
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

# Match results

- URL: `/match`
- Method: `/post`

### What it does:

- Accepts a field and value
- Returns all logs with `field` that matches `value`
- Can be used to fetch all records with specific values, such as all messages created by certain model, or specific UUID

### Example payload:

```json
{
 "field": "UUID",
 "value": "b1be5ea3-5ec4-489b-9bb8-24f005a35a7d",
}
```

### Example response:

- Response is a list of dictionaries. 

```json
[
 {"content": "I see a man on a bench"},
]
```

# Bounded search

- URL: `/bound`
- Method: `/post`

### What it does:

- Accepts a `lower_bound` and `upper_bound`
- Returns all logs with timestamp between lower and upper bound
- Fetch all memories in a given time window

### Example payload:

```json
{
 "lower_bound": 123.456,
 "upper_bound": 456.789,
}
```

### Example response:

- Response is a list of dictionaries. 

```json
[
 {"content": "I see a man on a bench"},
]
```

# Recent messages

- URL: `/recent`
- Method: `/post`

### What it does:

- Returns all most recent memories
- Limited to *n* seconds

### Example payload:

```json
{
 "seconds": 30,
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


