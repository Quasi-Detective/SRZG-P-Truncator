# ZG .P Truncator (for Python 3.8) by Quasi-Detective
# 2024.01.19
# Aims to properly truncate the 'OOCH' archives (.P and no extension) from Sonic Riders: Zero Gravity into files that can then be decrypted to .pack format using https://github.com/romhack/sonic_riders_lzss
# Based off of the method by moester_ in https://www.youtube.com/watch?v=q65xyi4Rn-c
# Place this script as a .py file into the folder with files you want to scan/truncate. Please make backups of the files if you want to revert any changes or in case there is an issue!

import os
import binascii
import sys

for fileO in os.listdir('.'):
	if not fileO.endswith(".new3"):
		with open(fileO, "rb") as f:
			print("File: %s" % str(fileO))
			headerB = binascii.hexlify(f.readline(4))
			if str(headerB.decode('utf8')) == '4f4f4348' and not fileO.endswith(".new"):
				print("OOCH header found! Proceeding.")
				#Do the thing. This could almost certainly be streamlined...
				newFile = open(fileO + ".new1", "wb")
				f.seek(0)
				newFile.write(f.read(16))
				f.seek(2016)
				newFile.write(f.read(os.path.getsize(fileO)))
				f.close()
				newFile.close()
				newFileB = open(fileO + ".new1", "rb")
				newFile2 = open(fileO + ".new2", "wb")
				newFileB.seek(0)
				newFile2.write(newFileB.read(40))
				newFileB.seek(48)
				newFile2.write(newFileB.read(os.path.getsize(fileO + ".new1")))
				newFileB.close()
				newFile2.close()
				newFile2B = open(fileO + ".new2", "rb")
				newFile3 = open(fileO + ".new3", "wb")
				newFile3.write(b'\x80\x00\x00\x01')
				newFile2B.seek(12)
				newFile3.write(newFile2B.read(os.path.getsize(fileO + ".new2")))
				newFile2B.close()
				newFile3.close()
				os.remove(fileO + ".new1")
				os.remove(fileO + ".new2")
				os.remove(fileO)
				os.rename(fileO + ".new3", fileO)

			else:
				print("Header '%s' is incorrect. Skipping." % str(headerB.decode('utf8')))
				#Don't do the thing.
				f.close()

try:            
    done = input("Truncation complete. Press any key to exit.")
except EOFError:
    done = "\n"
finally:
    sys.exit()
