import lifx

# Helper functions
# Human readable MAC
def MACstr(addr):
	return ':'.join(reversed([hex(addr)[i:i+2].upper() for i in range(2, len(hex(addr)), 2)]))
# Decode string32
def label(data):
	return data.rstrip(b'\x00').decode('utf-8')

# Encode/Decode floats, ints, bools for range [0-65535]
def c(val):
	return int(65535 * val)
def d(data):
	return data / 65535


# Examples
def list_devices():
	for (_, _, dev, *_), (service, _) in lifx.get(lifx.GetService, lifx.StateService):
		if service == 1:
			print(MACstr(dev))

def power_on():
	lifx.post(lifx.LightSetPower, c(True), 0)

def power_status():
	for (_, _, dev, *_), (power,) in lifx.get(lifx.LightGetPower, lifx.LightStatePower):
		print(MACstr(dev), ':', 'On' if power else 'Off')

def toggle_power():
	for (_, _, dev, *_), (power,) in lifx.get(lifx.LightGetPower, lifx.LightStatePower):
		lifx.post(lifx.LightSetPower, c(1 - d(power)), 0, device=dev)

def set_print(): # Set power with res_requested - NOTE: delay of set
	for (_, _, dev, *_), (power,) in lifx.get(lifx.LightSetPower, lifx.LightStatePower, c(True), 2000, res=1):
		print(MACstr(dev), ':', 'On' if power else 'Off')

def list_status():
	output = list()
	for _, data in lifx.get(lifx.LightGet, lifx.LightState):
		output.append('{} ({})\n\tHue: {:.2f}%\n\tSaturation: {:.2f}%\n\tBrightness: {:.0f}%\n\tKelvin: {}K'.format(
		label(data[6]), 'On' if data[5] else 'Off',
		360 * d(data[0]), 100 * d(data[1]), 100 * d(data[2]), data[3]))
	print(*sorted(output), sep='\n\n')


if __name__ == "__main__":
	list_status()