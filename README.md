This is a server that will create a dependency tree and let connected clients modify the same dependency tree concurrently without a race condition.

To use the server, first run `indexer_server.py`. 
		
		$./indexer_server.py

You should then see output like this. Using CTRL+c will exit the server gracefully.

	$./indexer_server.py
	Socket created
	index created
	Socket bound
	Socket now listening...

client messages are sent in the following format with spaces as the delimiter.
`COMMAND PACKAGE DEPENDENCIES`
`DEPENDENCIES` may be a comma separated list

The server will reply with `SUCCESS\n` for a valid index modification, `FAILURE\n` for an invalid modification, and `ERROR\n` as an error response. The error response is usually for malformed messages

## DESIGN RATIONALE:
The indexer breaks down into three major parts. Building a directed graph to model the dependency tree, allowing many users to connect to the server, and using threads to handle the users' requests such that there is not a race condition.

## GRAPH:
I deciced to use an adjacency list here because they are easy to reason about and can be efficient with sparse graphs. A dependency tree shouldnt be too dense otherwise there could be a dependency cycle. I prepared for dependency clycles by including a method that ran Depth First Search in order to find a back edge in the adjacency list. A back edge means there is a cycle.

## HANDLING REQUESTS:
Threads were necessary for allowing multiple connections concurrently. I originally was going to use one of Python's server classes like `ThreadingTCPServer`, however the server classes were hard to customize. In the end, I used TCP sockets to make a server from scratch. This was the right choice since it made using locks much easier later. To filter good requests from the broken I used a regular expression. Regex's are good for matching, very precisely, to a desired string pattern. This is how most of the "ERROR\n" responses were determined.

## CONCURRENCY AND THE GRAPH
The critical section here is when a client thread tries to make a change to the graph. To prevent a race condition between the client threads I used a lock. This method was simple and effective. Python has a very easy way to use locks. By wrapping the critical section using a `with` statement Python will automatically make the threads acquire a lock before the `with` statement and release the lock afterwards.
