#!/usr/bin/python
import sys,fileinput,select,base64
from optparse import OptionParser

def translate_t2bin(text):
	text = translate_t2h(text)
	binary = ""
	for i in range(0,len(text),2):
		binary += bin(int(text[i:i+2],16))[2:].zfill(8)
	return binary

def translate_t2i(text):
	return int(translate_t2h(text),16)

def translate_t2h(text):
	return text.encode("hex")

def translate_bin2i(binary):
	return int(binary,2)

def translate_t2b64(text):
	return translate_bin2b64(translate_t2bin(text))

def pad_hex(hex):
	return "0"*(len(hex)%2)+hex

def translate_bin2b64(binary):
	b64table = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/"
	result = ""
	if (len(binary)%3) == 0:
		for i in range(0,len(binary),6):
			#print "%s\t%s\t%s"%(binary[i:i+6],int(binary[i:i+6],2),b64table[int(binary[i:i+6],2)])
			result += b64table[int(binary[i:i+6],2)]
		return result
	elif (len(binary)%3) == 1:
		for i in range(0,len(binary),6):
			#print "%s\t%s\t%s"%(binary[i:i+6],int(binary[i:i+6],2),b64table[int(binary[i:i+6].ljust(6,"0"),2)])
			result += b64table[int(binary[i:i+6].ljust(6,"0"),2)]
		return result+"="
	else:
		for i in range(0,len(binary),6):
			#print "%s\t%s\t%s"%(binary[i:i+6],int(binary[i:i+6],2),b64table[int(binary[i:i+6].ljust(6,"0"),2)])
			result += b64table[int(binary[i:i+6].ljust(6,"0"),2)]
		return result+"=="

def translate_b642t(b64):
	return base64.decodestring(b64)

def translate_h2t(hexstring):
	return hexstring.decode("hex")

def translate_bin2t(binary):
	hexofbinary = hex(int(binary,2))
	if hexofbinary[-1] == "L":
		return hexofbinary[2:-1].decode("hex")
	else:
		return hexofbinary[2:].decode("hex")

def translate_bin2b64_stdin():
	toxcode = ""
	if select.select([sys.stdin,],[],[],0.0)[0]:
		for line in sys.stdin:
			toxcode += line
	return translate_bin2b64(translate_t2bin(toxcode))


def translate_t2h_stdin():
	toxcode = ""
	if select.select([sys.stdin,],[],[],0.0)[0]:
		for line in sys.stdin:
			toxcode += line
	return toxcode.encode("hex")



def auto_translate(data,encodingtype):
	encodingtype = encodingtype.lower().strip()
	if encodingtype not in ["b64","hex","bin"]:
		print "[!] Error: Only options for encoding type are: b64, hex, bin"
		parser.print_help()
		exit(-1)
	if encodingtype == "b64":
		return translate_t2b64(data)
	elif encodingtype == "hex":
		return translate_t2h(data)
	else:
		return translate_t2bin(data)

def auto_decode(data,encodingtype):
	encodingtype = encodingtype.lower().strip()
	if encodingtype not in ["b64","hex","bin"]:
		print "[!] Error: Only options for encoding type are: b64, hex, bin"
		exit(-1)
	if encodingtype == "b64":
		return translate_b642t(data)
	elif encodingtype == "hex":
		return translate_h2t(data)
	else:
		return translate_bin2t(data)

def retrieve_stdin():
	try:
		data = ""
		if select.select([sys.stdin,],[],[],0.0)[0]:
			for line in sys.stdin:
				data += line
		return data
	except Exception,e:
		print "[!] Error: %s"%str(e)
		exit(-1)


def main():
	parser = OptionParser()
	parser.add_option("-d","--decode",dest="decode",help="Decode instead of encode",action="store_true")
	parser.add_option("-e","--encoding",dest="encoding",help="Type of encoding [b64|hex|bin]",action="store")
	parser.add_option("-q","--quiet",dest="quietmode",help="Only print results of command",action="store_true")
	parser.add_option("-t","--text",dest="text",help="Text to encode/decode -- Only works if [-s/--stdin] is not used",action="store")
	parser.add_option("-s","--stdin",dest="stdin",help="Read data from STDIN",action="store_true")
	parser.add_option("-p","--pattern",dest="pattern",help="Pattern to encode/decode with  -- Only works if [-e/--encoding] and [-i/--iterations] is not used -- example: -p \"b64,hex,bin,bin,hex\" will encode/decode consecutively with each item in the pattern",action="store")
	parser.add_option("-i","--iterations",dest="iterations",help="Iterations of encoding -- only use when [-p/--pattern] is not used",action="store",default="1")

	(opts, args) = parser.parse_args()
	

	if opts.pattern and (opts.encoding or (opts.iterations != "1")):
		print "[!] You can't use the -p/--pattern with the -e/--encoding or -i/--iterations switches!"
		parser.print_help()
		exit(-1)
	if opts.text and opts.stdin:
		print "[!] You can't use the -t/--text together with the -s/--stdin switch!"
		parser.print_help()
		exit(-1)
	if not (opts.text or opts.stdin):
		print "[!] You have to provide some sort of data through -t/--text or through stdin with -s/--stdin!"
		parser.print_help()
		exit(-1)
	if (opts.text or opts.stdin) and not (opts.encoding or opts.pattern):
		print "[!] You have to specify which decoding/encoding actions youd like to take wth either -e/--encoding or -p/--pattern!"
		parser.print_help()
		exit(-1)


	banner = '''                                                                                                             
                                     888                                                    
     Y88b  /   e88~~\  e88~-_   e88~\888  e88~~8e  888-~\      888-~88e  Y88b  /            
____  Y88b/   d888    d888   i d888  888 d888  88b 888         888  888b  Y888/        ____ 
       Y88b   8888    8888   | 8888  888 8888__888 888         888  8888   Y8/              
       /Y88b  Y888    Y888   ' Y888  888 Y888    , 888    d88b 888  888P    Y               
      /  Y88b  "88__/  "88_-~   "88_/888  "88___/  888    Y88P 888-_88"    /                
                                                               888       _/        by et0x'''
                                                                                   
	if not opts.quietmode:
		print banner
		print "[+] Results: "



	if opts.text:                    ########## everything below will receive data from -t option ###############
		if opts.decode:
			if opts.pattern:		#### DECODE patterns "b64,hex,bin" etc ####
				mandatoryargs = ["pattern"]
				try:
					data = opts.text
					for item in opts.pattern.split(","):
						if item.strip() != "" and (item.lower().strip() in ["b64","hex","bin"]):
							data = auto_decode(data,item)
					print data
				except:
					print "[!] Error with switches or arguments!"
					parser.print_help()
					exit(-1)
			else:				#### DECODE text... -t "test" ####
				mandatoryargs = ["encoding"]
				for m in mandatoryargs:
					if not opts.__dict__[m]:
						print "[!] Mandatory argument is missing!"
						parser.print_help()
						exit(-1)
				if opts.iterations == "1":
					data = opts.text
					print auto_decode(data,opts.encoding)
				else:
					data = opts.text
					try:
						for i in range(int(opts.iterations)):
							data = auto_decode(data,opts.encoding)
						print data
					except Exception, e:
						print "[!] Error: %s"%str(e)
						parser.print_help()
						exit(-1)
		else:
			if opts.pattern:		#### ENCODE patterns "b64,hex,bin" etc ####
				mandatoryargs = ["pattern"]
				try:
					data = opts.text
					for item in opts.pattern.split(","):
						if item.strip() != "" and (item.lower().strip() in ["b64","hex","bin"]):
							data = auto_translate(data,item)
					print data
				except:
					print "[!] Error with switches or arguments!"
					parser.print_help()
					exit(-1)
			else:
				mandatoryargs = ["encoding"]
				for m in mandatoryargs:
					if not opts.__dict__[m]:
						print "[!] Mandatory argument is missing!"
						parser.print_help()
						exit(-1)
				if opts.iterations == "1":
					data = opts.text
					print auto_translate(data,opts.encoding)
				else:
					try:
						data = opts.text
						for i in range(int(opts.iterations)):
							data = auto_translate(data,opts.encoding)
						print data
					except Exception, e:
						print "Error: %s"%str(e)
						parser.print_help()
						exit(-1)
	elif opts.stdin:	##############  everything below will receive data from STDIN ##################
		if opts.decode:
			if opts.pattern:		#### DECODE patterns "b64,hex,bin" etc ####
				mandatoryargs = ["pattern"]
				try:
					data = retrieve_stdin()
					for item in opts.pattern.split(","):
						if item.strip() != "" and (item.lower().strip() in ["b64","hex","bin"]):
							data = auto_decode(data,item)
					print data
				except:
					print "[!] Error with switches or arguments!"
					parser.print_help()
					exit(-1)
			else:				#### DECODE text... -t "test" ####
				mandatoryargs = ["encoding"]
				for m in mandatoryargs:
					if not opts.__dict__[m]:
						print "[!] Mandatory argument is missing!"
						parser.print_help()
						exit(-1)
				if opts.iterations == "1":
					data = retrieve_stdin()
					print auto_decode(data,opts.encoding)
				else:
					data = retrieve_stdin()
					try:
						for i in range(int(opts.iterations)):
							data = auto_decode(data,opts.encoding)
						print data
					except Exception, e:
						print "[!] Error: %s"%str(e)
						parser.print_help()
						exit(-1)
		else:
			if opts.pattern:		#### ENCODE patterns "b64,hex,bin" etc ####
				mandatoryargs = ["pattern"]
				try:
					data = retrieve_stdin()
					for item in opts.pattern.split(","):
						if item.strip() != "" and (item.lower().strip() in ["b64","hex","bin"]):
							data = auto_translate(data,item)
					print data
				except:
					print "[!] Error with switches or arguments!"
					parser.print_help()
					exit(-1)
			else:
				mandatoryargs = ["encoding"]
				for m in mandatoryargs:
					if not opts.__dict__[m]:
						print "[!] Mandatory argument is missing!"
						parser.print_help()
						exit(-1)
				if opts.iterations == "1":
					data = retrieve_stdin()
					print auto_translate(data,opts.encoding)
				else:
					try:
						data = retrieve_stdin()
						for i in range(int(opts.iterations)):
							data = auto_translate(data,opts.encoding)
						print data
					except Exception, e:
						print "Error: %s"%str(e)
						parser.print_help()
						exit(-1)


if __name__ == "__main__":
	main()
