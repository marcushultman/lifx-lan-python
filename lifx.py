import socket
import uuid
import struct

# Socket
_csoc = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
_csoc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
_csoc.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
_csoc.settimeout(0.5)
_csoc.bind(('', 56700))

# Internal data
_src = uuid.uuid1().node % 4294967296
_sequence = 0
_messageQueue = dict()

# Network interface
def post(Message, *payload, device=0, port=56700):
	for _ in get(Message, None, *payload, device=device, port=port):
		pass

def get(Message, Response, *payload,
	device=0, ack=0, res=0,
	timeout=0.5, limit=None, port=56700):
	# Send packet
	global _sequence
	seq = _sequence = (_sequence + 1) % 256
	data = Message.pack(_src, seq, device, ack, res, *payload)
	_csoc.sendto(data, ('255.255.255.255', port))
	# Receive response
	mKey = (seq, Response.type)
	while Response and (limit is None or limit > 0):
		q = _messageQueue.setdefault(mKey, list())
		try:
			_csoc.settimeout(timeout)
			data = q.pop(0) if len(q) else _csoc.recv(256)
		except socket.error:
			break
		else:
			header = Header.unpack(data)
			rKey = header[3:5]
			if rKey == mKey:
				yield header, Response.unpack(data[Header.size:])
				if limit is not None:
					limit -= 1
			else:
				_messageQueue.setdefault(rKey, list()).append(data)

# Data structures
class Header():
	_struct = struct.Struct('<HHIQIHBBQHH')
	size = _struct.size
	def pack(type, payloadSize, source, sequence, device=0, ack=0, res=0):
		return Header._struct.pack(
			# Frame
			Header.size + payloadSize,
			(0 if device else 0x2000) + 0x1400,
			source,
			# Frame Address
			device,
			0x00000000, 0x0000,
			ack * 0x02 + res * 0x01,
			sequence,
			# Protocol
			0x0000000000000000,
			type,
			0x0000
		)
	def unpack(data):
		# Unpack header values, keep the relevant
		(size, _, source, target, _, _, _, sequence, _, type, _
			) = Header._struct.unpack(data[:Header.size])
		return (size, source, target, sequence, type)

class DeviceMessage(struct.Struct):
	def __init__(self, type, format=''):
		super(DeviceMessage, self).__init__('<' + format)
		self.type = type
	def pack(self, source, sequence, device=0, ack=0, res=0, *payload):
		return Header.pack(self.type, self.size, source, sequence,
			device, ack, res) + super(DeviceMessage, self).pack(*payload)


# Device messages
GetService 			= DeviceMessage(2)
StateService 		= DeviceMessage(3, 'BI')
GetHostInfo 		= DeviceMessage(12)
StateHostInfo 		= DeviceMessage(13, 'fIIh')
GetHostFirmware 	= DeviceMessage(14)
StateHostFirmware 	= DeviceMessage(15, 'QQI')
GetWifiInfo 		= DeviceMessage(16)
StateWifiInfo 		= DeviceMessage(17, 'fIIh')
GetWifiFirmware 	= DeviceMessage(18)
StateWifiFirmware 	= DeviceMessage(19, 'QQI')
GetPower 			= DeviceMessage(20)
SetPower 			= DeviceMessage(21, 'H')
StatePower 			= DeviceMessage(22, 'H')
GetLabel 			= DeviceMessage(23)
SetLabel 			= DeviceMessage(24, '32s')
StateLabel 			= DeviceMessage(25, '32s')
GetVersion 			= DeviceMessage(32)
StateVersion 		= DeviceMessage(33, '3I')
GetInfo 			= DeviceMessage(34)
StateInfo 			= DeviceMessage(35, '3Q')
Acknowledgement 	= DeviceMessage(45)
GetLocation 		= DeviceMessage(48)
StateLocation 		= DeviceMessage(50, '16s32sQ')
GetGroup 			= DeviceMessage(51)
StateGroup 			= DeviceMessage(53, '16s32sQ')
EchoRequest 		= DeviceMessage(58, '64s')
EchoResponse 		= DeviceMessage(59, '64s')

# Light messages
LightGet 		= DeviceMessage(101)
LightSetColor 	= DeviceMessage(102, 'B4HI')
LightState 		= DeviceMessage(107, '4HhH32sQ')
LightGetPower 	= DeviceMessage(116)
LightSetPower 	= DeviceMessage(117, 'HI')
LightStatePower = DeviceMessage(118, 'H')