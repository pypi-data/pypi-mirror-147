# three-commas-websocket-assist

GNU General Public License v3.0

`pip install three-commas-websocket-assist`

### Import
```
from three-commas-websocket-assist import ThreeCommasWebsocketHandler
```

### 1. Setting up the listener
Pass 3commas api key/secret and the channel you desire to `ThreeCommasWebsocketHandler`:
```Python
st = ThreeCommasWebsocketHandler(
    api_key=API_KEY,
    api_secret=API_SECRET,
    channel="DealsChannel",
)
```
`ThreeCommasWebsocketHandler` automatically generates the stream identifier and uses that for the stream


### 2. Handle event
Pass a custom event handler to  the `ThreeCommasWebsocketHandler` to handle any event based on your deal channel:
Event handler is `Callable[[Dict], None]`
```Python
st = ThreeCommasWebsocketHandler(
    api_key=API_KEY,
    api_secret=API_SECRET,
    channel="DealsChannel",
    external_event_handler=sample_event_handler
)
```

Sample event handler:
```Python
def sample_event_handler(data:Dict) -> None:
    """
    Sample Event Handler for websocket
    """
    _LOGGER.debug("Bot_id: %s", data['bot_id'])

    # Do something with the data here
```