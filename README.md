# xcoder
A tool for encoding and decoding data in various formats

## Synopsis:

Xcoder is a simple script that will take various forms of in put, either statically defined, or from STDIN, and translate it into and from various formats, with pattern encoding / multiple iteration capabilities built in.

## Usage:

Refer to the command-line help if you get stuck.  Otherwise, the following capabilities are provided with this tool.

    Usage: xcoder.py [options]

    Options:<br>
      -h, --help            show this help message and exit
      -d, --decode          Decode instead of encode
      -e ENCODING, --encoding=ENCODING
                            Type of encoding [b64|hex|bin]
      -q, --quiet           Only print results of command
      -t TEXT, --text=TEXT  Text to encode/decode -- Only works if [-s/--stdin] is not used
      -s, --stdin           Read data from STDIN
      -p PATTERN, --pattern=PATTERN
                            Pattern to encode/decode with  -- Only works if
                            [-e/--encoding] and [-i/--iterations] is not used --
                            example: -p "b64,hex,bin,bin,hex" will encode/decode
                            consecutively with each item in the pattern
      -i ITERATIONS, --iterations=ITERATIONS
                            Iterations of encoding -- only use when [-p/--pattern] is not used
        
The first thing to take into account is if you're reading data statically or from STDIN.

**STDIN:**

```bash
et0x@mnstr:~$ echo -n "AAAA" | ./xcoder.py -e hex -q --stdin
41414141
```

**STATIC:**

```bash
et0x@mnstr:~$ ./xcoder.py -t "AAAA" -e b64 -q
QUFBQQ==
```

You can also do multiple iterations of encoding/decoding as well as pattern-based encoding/decoding:

    et0x@mnstr:~/Desktop/xcoder$ ./xcoder.py -t "AAAA" -i 10 -e b64 -q
    Vm0wd2QyVkZOVWRpUm1ScFVtMVNXVll3Wkc5V1ZsbDNXa2M1VjFKdGVEQlpNM0JIVmpGS2RHVkliRmRpVkZaeVZtMHhTMUl5VGtsaVJtUlhUVEZLVFZac1ZtRldNVnBXVFZWV2FHVnFRVGs9
 
    
    et0x@mnstr:~/Desktop/xcoder$ ./xcoder.py -t     "Vm0wd2QyVkZOVWRpUm1ScFVtMVNXVll3Wkc5V1ZsbDNXa2M1VjFKdGVEQlpNM0JIVmpGS2RHVkliRmRpVkZaeVZtMHhTMUl5VGtsaVJtUlhUVEZLVFZac1ZtRldNVnBXVFZWV2FHVnFRVGs9" -i 10 -e b64 -q -d
AAAA

    et0x@mnstr:~$ ./xcoder.py -t "AAAA" -p "hex,hex,b64,bin" -q    
    010011010111101001010001011110100100110101010100010011010011000001001101011110100100010101111010010011100100010001001101011110000100110101111010010100010111101001001101010100010011110100111101

    et0x@mnstr:~$ echo -n "010011010111101001010001011110100100110101010100010011010011000001001101011110100100010101111010010011100100010001001101011110000100110101111010010100010111101001001101010100010011110100111101" | ./xcoder.py -s -p "bin,b64,hex,hex" -q -d
    AAAA

## Motivation:

I was working on a boot2root machine a while back that required you to deobfuscate something that was encoded in a iterative/pattern-based fashion 17 times in a row which was a pain to decode, so I figured I'd make something like this.  I'm sure there are some other applications as well :)

For those interested, the boot2root machine was called **Flick** (created by Leonjza) and is located at [http://www.vulnhub.com](https://www.vulnhub.com/entry/flick-1,99/)

