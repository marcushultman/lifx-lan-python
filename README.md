# LIFX LAN python wrapper

Low-level python wrapper around the [LIFX LAN v2 API](http://lan.developer.lifx.com/docs/introduction). Synchonous interface with nothing 'going on behind the scenes'.

*Note: Please consult the LAN specification for any unexpected behaviour (such as receiving unknown responses etc.).*

## lifx module
Consists of a network interface using a bound UDP socket, two data classes for device messages and implementations for the currently available message types, which directly maps to the message types in the LAN specification.

### lifx.post
Function that posts a message but does not wait for results.

`lifx.post(Message, v1, v2, ..., device=0, port=56700)`

Argument      | Comment
------------- | -------------
`Message`     | The message to post such as `lifx.GetService`.
`v1, v2, ...` | Payload for the message that maps directly to the payload in the LAN specifications (types according to pythons `struct`-module).
`device`      | Optional device address (as left-shifted 64-bit unsigned int).
`port`        | Port defaults to `56700`. `StateService` returns a requested port that can be used instead.

### lifx.get
Function that posts a message and yields the result (as a generator). The iteration stops after a certain amount of time or when the specified amount of results has been collected.

`lifx.get(Message, Response, v1, v2, ..., device=0, ack=0, res=0, timeout=0.5, limit=None, port=56700)`

Argument      | Comment
------------- | -------------
`Message`     | The message to post such as `lifx.GetService`.
`Response`    | The message to receive such as `lifx.StateService`.
`v1, v2, ...` | Payload for the message.
`device`      | Optional device address.
`ack`         | Acknowledgement message required (see API spec).
`res`         | Response message required (see API spec).
`timeout`     | Defaults to 0.5 seconds. Can be set to None to block indefinitely. 
`limit`       | Number of results to obtain.
`port`        | Port defaults to 56700.

### Messages
See [LAN specification](http://lan.developer.lifx.com/docs/device-messages) for details on payload.

#### [Device messages](http://lan.developer.lifx.com/docs/device-messages)
* GetService
* StateService
* GetHostInfo
* StateHostInfo
* GetHostFirmware
* StateHostFirmware
* GetWifiInfo
* StateWifiInfo
* GetWifiFirmware
* StateWifiFirmware
* GetPower
* SetPower
* StatePower
* GetLabel
* SetLabel
* StateLabel
* GetVersion
* StateVersion
* GetInfo
* StateInfo
* Acknowledgement
* GetLocation
* StateLocation
* GetGroup
* StateGroup
* EchoRequest

#### [Light messages](http://lan.developer.lifx.com/docs/light-messages)
* LightGet
* LightSetColor
* LightState
* LightGetPower
* LightSetPower
* LightStatePower


## Example

Turn on all lights:
`lifx.post(lifx.LightSetPower, 65535, 0)`
