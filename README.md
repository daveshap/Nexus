# Nexus REST Microservice

Stream of consciousness nexus REST microservice

- Aggregate messages from arbitrary services
- Serve message to arbitrary services upon request
- Similar to short-term memory of cognitive/consciousness systems

# Usage 

1. Run with `python nexus.py`
2. POST new messages to specified `port` number
3. GET last *n* messages from specified `port`
4. Messages consist of `data` and `meta`

# Theory

## Biomimicry

Stream of consciousness (SoC) is an aggregation, or confluence, of sensations, thoughts, ideas, and memories. Stream of consciousness is a critical component to intelligence and real-time performance for humans and animals. 
*Working memory* is approximately the size of the stream of consciousness, or how many messages can be simultaneously held in the stream of consciousness. Over time, messages are cleared or purged from the SoC to maintain performance.
Some messages are stored in long term memory (LTM) for later retrieval. This function can be approximated by allowing arbitrary services to contribute to the SoC.

## Data and Metadata

Messages within the SoC all contain specific, relevant information. For instance, a sensation, memory, or thought contain their specific relevant information but they also implicitly contain metadata.
That is to say that you do not confuse images with sounds, or memories with realtime sensations. This happens in spite of everything being accessible to the same SoC, as we have a singular consciousness. 
Metadata can contain information that differentiates types of messages from one another but also adds context, such as chronological time. 
Chronological time is critical for real-time functionality, forming cohesive and coherent understanding of the world.