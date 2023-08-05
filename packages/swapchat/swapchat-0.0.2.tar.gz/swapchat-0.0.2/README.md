# SwapChat-SDK-Python
SwapChat SDK Python


```bash
pip install swapchat
```


## Quick Start

```python
from swapchat import get_swapchat_client


def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))

    # Subscribing in on_connect() means that if we lose the connection and
    # reconnect then subscriptions will be renewed.
    client.subscribe("$SYS/#")

# The callback for when a PUBLISH message is received from the server.
def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))


client = get_swapchat_client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("msg.web3messaging.online", 443)
client.loop_forever()
```

### Publish Single Example

```python

import paho.mqtt.publish as publish

# Get room id from https://docs.web3messaging.online/docs/ChatServices/Rooms/get-chat-rooms
room_id = ""
topic = "msg/" + room_id

payload = {
    "from_uid" : "624546390e62aa416dcdd4ea",
    "to_room_id" : "624c0a390e62aa416dcdd57e",
    "msg_contents" : "Hello",
    "msg_type" : "text"
}

publish.single(topic, payload, hostname="msg.web3messaging.online")
```
