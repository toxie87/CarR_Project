#!/usr/bin/python3

from smbus import SMBus

RDA_I2C_DEV = 1 # /dev/i2c-1
RDA_I2C_WRITE_ADDR = 0x10
RDA_I2C_READ_ADDR = 0x11

RDA_ID = 0x58


class RDA_reg():
	def __init__(self, reg, r_len, mask, desc, default=0):
		self.reg = reg
		self.r_len = r_len
		self.mask = mask
		self.desc = desc
		self.default = default

	def __str__(self):
		"""
		Override the __str__ functions
		"""
		return 'Reg: 0x' + str(self.reg) + '\r\nDesc:' + self.desc 

	def get_mask(self):
		"""
		Returns the amount of bits to shift
		"""
		temp = bin(self.mask)
		shl = 0
		mask_len = 0	
		for n in range(len(temp) - 2):
			if temp[-1] == '0':
				if mask_len > 0:
					continue	
				else:	
					temp = temp[:-1]
					shl = shl+1
			else:
				mask_len = mask_len + 1	
		return (mask_len,shl)

#Reg 0x00 mask
R_CHIPID 		= RDA_reg(0x00,  8, 0b1111111100000000, "RDA5807M ID", RDA_ID)

#Reg 0x02 mask
R_DHIZ			= RDA_reg(0x02, 16, 0b1000000000000000, "Audio Output High-Z Disable", 0)
R_DMUTE			= RDA_reg(0x02, 16, 0b0100000000000000, "Mute Disable", 0)
R_MONO			= RDA_reg(0x02, 16, 0b0010000000000000, "Mono Select", 0)
R_BASS			= RDA_reg(0x02, 16, 0b0001000000000000, "Bass Boost", 0)
R_RCLK_NC		= RDA_reg(0x02, 16, 0b0000100000000000, "RCLK Non calibrate mode", 0)
R_RCLK_DM		= RDA_reg(0x02, 16, 0b0000010000000000, "RCLK Direct input mode", 0)
R_SEEKUP		= RDA_reg(0x02, 16, 0b0000001000000000, "Frequency sweep up", 0)
R_SEEK			= RDA_reg(0x02, 16, 0b0000000100000000, "Frequency sweep", 0)
R_SKMODE		= RDA_reg(0x02, 16, 0b0000000010000000, "Seek mode", 0)
R_CLKMODE		= RDA_reg(0x02, 16, 0b0000000001110000, "Clock mode", 0)
R_RDS_EN		= RDA_reg(0x02, 16, 0b0000000000001000, "RDS enable", 0)
R_NEW_METHOD		= RDA_reg(0x02, 16, 0b0000000000000100, "New Demodulate Method", 0)
R_SOFT_RESET		= RDA_reg(0x02, 16, 0b0000000000000010, "Soft reset", 0)
R_ENABLE		= RDA_reg(0x02, 16, 0b0000000000000001, "Power Up Enable", 0)

#Reg 0x03 mask
R_CHAN			= RDA_reg(0x03, 16, 0b1111111111000000, "Channel Select", 0)
R_DIRECT_M		= RDA_reg(0x03, 16, 0b0000000000100000, "Direct mode", 0)
R_TUNE			= RDA_reg(0x03, 16, 0b0000000000010000, "Tune", 0)
R_BAND			= RDA_reg(0x03, 16, 0b0000000000001100, "Band Select", 0)
R_SPACE			= RDA_reg(0x03, 16, 0b0000000000000011, "Channel Spacing", 0)

#Reg 0x04 mask
R_RSVD04_1		= RDA_reg(0x04, 16, 0b1000000000000000, "Reserved", 0)
R_RSVD04_2		= RDA_reg(0x04, 16, 0b0011000000000000, "Reserved", 0)
R_DE			= RDA_reg(0x04, 16, 0b0000100000000000, "De-emphasis", 0)
R_RSVD04_3		= RDA_reg(0x04, 16, 0b0000010000000000, "Reserved", 0)
R_SOFTMUTE_EN		= RDA_reg(0x04, 16, 0b0000001000000000, "Soft mute", 1)
R_AFCD			= RDA_reg(0x04, 16, 0b0000000100000000, "AFC disable", 0)

#Reg 0x05 mask
R_INT_MODE		= RDA_reg(0x05, 16, 0b1000000000000000, "Interrupt mode", 0)
R_RSVD05_1		= RDA_reg(0x05, 16, 0b0111000000000000, "Reserved", 0)
R_SEEKTH		= RDA_reg(0x05, 16, 0b0000111100000000, "Seek SNR threshold value", 8)
R_RSVD05_2		= RDA_reg(0x05, 16, 0b0000000000110000, "Reserved", 0)
R_VOLUME		= RDA_reg(0x05, 16, 0b0000000000001111, "Volume", 15)

#Reg 0x06 mask
R_RSVD06_1		= RDA_reg(0x06, 16, 0b1000000000000000, "Reserved", 0)
R_OPEN_MODE		= RDA_reg(0x06, 16, 0b0110000000000000, "Open reserved register mode", 0)

#Reg 0x07 mask
R_RSVD07_1		= RDA_reg(0x07, 16, 0b1000000000000000, "Reserved", 0)
R_TH_SOFRBLEND		= RDA_reg(0x07, 16, 0b0111110000000000, "Threshold for noise soft blend setting, unit 2dB", 16)
R_65M_50M_MODE		= RDA_reg(0x07, 16, 0b0000001000000000, "Valid when band[1:0]=2b11 0x03reg", 1)
R_RSVD07_2		= RDA_reg(0x07, 16, 0b0000000100000000, "Reserved", 0)
R_SEEK_TH_OLD		= RDA_reg(0x07, 16, 0b0000000011111100, "Seek threshold for old seek mode.Valid when Seek_Mode=001", 0)
R_SOFTBLEND_EN		= RDA_reg(0x07, 16, 0b0000000000000010, "If 1, Softblend enable", 1)
R_FREQ_MODE		= RDA_reg(0x07, 16, 0b0000000000000001, "If 1, then freq setting changed", 0)

#Reg 0x0A mask
R_RDSR			= RDA_reg(0x0A, 16, 0b1000000000000000, "RDS ready", 0)
R_STC			= RDA_reg(0x0A, 16, 0b0100000000000000, "Seek/Tune Complete", 0)
R_SF			= RDA_reg(0x0A, 16, 0b0010000000000000, "Seek Fail", 0)
R_RDSS			= RDA_reg(0x0A, 16, 0b0001000000000000, "RDS Synchronization", 0)
R_BLK_E			= RDA_reg(0x0A, 16, 0b0000100000000000, "Block E found", 0)
R_ST			= RDA_reg(0x0A, 16, 0b0000010000000000, "Stereo Indicator", 1)
R_READCHAN		= RDA_reg(0x0A, 16, 0b0000001111111111, "Read Channel", 0)

#Reg 0x0B mask
R_RSSI			= RDA_reg(0x0B, 16, 0b1111111000000000, "RSSI", 0)
R_FM_TRUE		= RDA_reg(0x0B, 16, 0b0000000100000000, "Current channel is a station", 0)
R_FM_READY		= RDA_reg(0x0B, 16, 0b0000000010000000, "FM ready", 0)
R_RSVD0B_1		= RDA_reg(0x0B, 16, 0b0000000001100000, "Reserved", 0)
R_ABCD_E		= RDA_reg(0x0B, 16, 0b0000000000010000, "If 1 - Block ID of register 0cH, 0dH, 0eH, 0fH is E, If 0 - A B C D", 0)
R_BLERA			= RDA_reg(0x0B, 16, 0b0000000000001100, "Block Errors Level of RDS_DATA_0", 0)
R_BLERB			= RDA_reg(0x0B, 16, 0b0000000000000010, "Block Errors Level of RDS_DATA_1", 0)
R_ENABLE		= RDA_reg(0x0B, 16, 0b0000000000000001, "Power Up Enable", 0)

#Reg 0x0C mask
R_RDSA			= RDA_reg(0x0C, 16, 0b1111111111111111, "BLOCK A", 0x5803)

#Reg 0x0D mask
R_RDSB			= RDA_reg(0x0D, 16, 0b1111111111111111, "BLOCK B", 0x5804)

#Reg 0x0E mask
R_RDSC			= RDA_reg(0x0E, 16, 0b1111111111111111, "BLOCK C", 0x5808)

#Reg 0x0F mask
R_RDSD			= RDA_reg(0x0F, 16, 0b1111111111111111, "BLOCK D", 0x5804)

class RDA5807M():
	def __init__(self, read_addr=RDA_I2C_READ_ADDR, write_addr=RDA_I2C_WRITE_ADDR, dev=RDA_I2C_DEV):
		"""
		Initialize, check for the device
		"""
		self.read_addr = read_addr
		self.write_addr = write_addr
		self.dev = dev
		self.bus = SMBus(dev)
		dev_ID = self.bus.read_byte_data(read_addr, 0x00)
		if dev_ID == RDA_ID:
			print("RDA5807M found")
		else:
			print("Unknown ID")
			return None

	def read_byte(self, register=None):
		"""
		Read one byte of a specified register
		"""
		if register is None:
			print("Register cannot be None")
			return False
		else:
			if register in range(0,255):
				rd_byte = self.bus.read_byte_data(self.read_addr, register)
				return rd_byte
			else:
				print("Register value must be in range of 0x00 - 0xFF")
				return False

	def read_2byte(self, register=None):
		"""
		Read two bytes of a specified register
		"""
		if register is None:
			print("Register cannot be None")
			return False
		else:
			if register in range(0,255):
				rd_byte = self.bus.read_word_data(self.read_addr, register)
				return rd_byte
			else:
				print("Register value must be in range of 0x00 - 0xFF")
				return False

	def write_byte(self, register=None, value=None):
		"""
		Write one byte to the specified register
		"""
		if register is None:
			print("Register cannot be None")
			return False
		else:
			if register in range(0,255):
				self.bus.write_word_data(self.write_addr, register, value)	

	def read_register_value(self, register=None):
		"""
		Read register value
		"""
		if not isinstance(register, RDA_reg):
			print("Register is not an instance of RDA_reg")
			return False
		else:
			if register.r_len == 8:
				read_handle = self.read_byte
			elif register.r_len == 16:
				read_handle = self.read_2byte
			else:
				print("No read handle available")
				return False

		read_data = read_handle(register.reg)
		#print(read_data)
		read_data = read_data & register.mask
		#print(read_data)
		return hex(read_data)

	def set_register_value(self, register=None, value=None):
		"""
		Set register value
		"""
		if not isinstance(register, RDA_reg):
			print("Register is not an instance of RDA_reg")
			return False
		else:
			if register.r_len == 8:
				write_handle = self.write_byte	
			elif register.r_len == 16:
				write_handle = self.write_2bytes
			else:
				print ("No write handle available")
				return False

a = RDA5807M()

#print(a.read_byte(0x00))
#print(a.read_2byte(0x0A))
#print(a.read_register_value(R_CHIPID))
#print(a.read_register_value(R_ENABLE))
#print(R_DHIZ)
print(a.read_register_value(R_RDSA))
a.write_byte(R_RDSA,85) 
print(a.read_register_value(R_RDSA))
print(R_VOLUME.get_mask())
