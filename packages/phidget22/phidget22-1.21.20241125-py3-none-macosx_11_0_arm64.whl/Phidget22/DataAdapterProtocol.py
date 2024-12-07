import sys
import ctypes
class DataAdapterProtocol:
	# Basic half-duplex RS485. Always receiving until you send data.
	PROTOCOL_RS485 = 1
	# Uses full-duplex RS422 communication.
	PROTOCOL_RS422 = 2
	# Allows communication with DMX512-compatible devices, such as stage lighting
	PROTOCOL_DMX512 = 3
	# Allows communication with MODBUS RTU compatible devices
	PROTOCOL_MODBUS_RTU = 4
	# Allows communication with RS232 compatible devices
	PROTOCOL_RS232 = 8

	@classmethod
	def getName(self, val):
		if val == self.PROTOCOL_RS485:
			return "PROTOCOL_RS485"
		if val == self.PROTOCOL_RS422:
			return "PROTOCOL_RS422"
		if val == self.PROTOCOL_DMX512:
			return "PROTOCOL_DMX512"
		if val == self.PROTOCOL_MODBUS_RTU:
			return "PROTOCOL_MODBUS_RTU"
		if val == self.PROTOCOL_RS232:
			return "PROTOCOL_RS232"
		return "<invalid enumeration value>"
