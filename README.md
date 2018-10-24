Flask Server End points
>/timestamp
>Params: None
>Returns: List of attacks as a string

How the collect_data function works
It continuously receives a message from the list and sets the date and address equal to the message. If no other thread is utilizing the list, it adds the list to q which is local memory, otherwise, every 60 seconds, it removes it.

Where is redis used
Redis is never used within data_collection or data_aggregation. 

/TODO
Create a DB
Get better understanding on the UDP pipe in collector
Find a use for flask otherwise remove it



