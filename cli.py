from Translator import CharsetTranslatorBuilder
import sys


# invisible characters

unicode_invisible = {
        chr(0x0009),
        chr(0x0020),
        chr(0x00a0),
        chr(0x00ad),
        chr(0x034f),
        chr(0x061c),
        chr(0x115f),
        chr(0x1160),
        chr(0x17b4),
        chr(0x17b5),
        chr(0x180e),
        chr(0x2000),
        chr(0x2001),
        chr(0x2002),
        chr(0x2003),
        chr(0x2004),
        chr(0x2005),
        chr(0x2006),
        chr(0x2007),
        chr(0x2008),
        chr(0x2009),
        chr(0x200a),
        chr(0x200b),
        chr(0x200c),
        chr(0x200d),
        chr(0x200e),
        chr(0x200f),
        chr(0x202f),
        chr(0x205f),
        chr(0x2060),
        chr(0x2061),
        chr(0x2062),
        chr(0x2063),
        chr(0x2064),
        chr(0x2065),
        chr(0x2066),
        chr(0x2067),
        chr(0x2068),
        chr(0x2069),
        chr(0x2800),
        chr(0x3000),
        chr(0x3164),
        chr(0xfeff),
        chr(0xffa0),
        chr(0x1d159),
        chr(0x1d173),
        chr(0x1d174),
        chr(0x1d175),
        chr(0x1d176),
        chr(0x1d177),
        chr(0x1d178),
        chr(0x1d179),
        chr(0x1d17a),
        }


unicode_invisible_zero_width = [
        chr(0x34f),
        chr(0x2063),
        chr(0x200e),
        chr(0x2069),
        chr(0x2065),
        chr(0x200b),
        chr(0x2064),
        chr(0x17b4),
        chr(0x61c),
        chr(0xfeff),
        chr(0x2061),
        chr(0x200c),
        chr(0x2060),
        chr(0x2068),
        chr(0x2066),
        chr(0x200d),
        chr(0xad),
        chr(0x200f),
        # chr(0x2067), # invertes left and right for the remaining text
        # chr(0x180e), # seems not to work as without suffix
        # chr(0x1d173),
        # chr(0x1d174),
        # chr(0x1d159),
        # chr(0x1d175),
        # chr(0x1d176),
        # chr(0x1d177),
        # chr(0x1d178),
        # chr(0x1d17a),
        ]

# configuration
startSequence                   = 1 * unicode_invisible_zero_width[0]
endSequence                     = 1 * unicode_invisible_zero_width[1]
invisible_separator             = 1 * unicode_invisible_zero_width[2]
invisible_zero_width_alphabet   = unicode_invisible_zero_width[3:]


def main(text: str, encode: bool) -> str:
    if encode:
        encoded_text = translator.encode(text)
        return encoded_text
    else:
        decoded_text = "".join(translator.decode(text))
        return decoded_text



if __name__ == "__main__":
    from argparse import ArgumentParser
    import sys

    stdin = sys.stdin
    stdout = sys.stdout
    stderr = sys.stderr

    def log(msg, file):
        if args.debug:
            print(msg, file=file)

    # parse args 

    parser = ArgumentParser(
            prog="InvisibleUnicodeText",
            description="Encodes or decodes the given text into invisilbe unicode text.",
            epilog="The result is forwarded to stdin. Log messages are send to stderr. \nmade by Bruno"
            )
    parser.add_argument("-d", "--decode", 
                        dest="encode", 
                        action="store_false", 
                        default=True, 
                        required=False, 
                        help="switch from encoding to decoding stdin"
                        )
    parser.add_argument("--debug", 
                        dest="debug", 
                        action="store_true", 
                        default=True, # False, 
                        required=False, 
                        help="enable debug logs into stderr"
                        )
    args = parser.parse_args(sys.argv[1:])

    # create translator chain

    builder = CharsetTranslatorBuilder()\
        .setCharset("".join(invisible_zero_width_alphabet))\
        .setSeparator(invisible_separator)\
        .setSequences(startSequence, endSequence)

    translator = builder.build()

    # run stuff 


    content = stdin.read()
    log(f"using sequences start: '{hex(ord(startSequence))}' and end: '{hex(ord(endSequence))}'", stderr)
    if args.encode:
        log(f"Encoding {len(content)} characters.", file=stderr)
    else:
        log(f"Decoding {len(content)} characters.", file=stderr)
        hexcontent = " ".join([str(hex(ord(char))) for char in content])
        log(f"Message '{hexcontent}'", stderr)

    res = main(content, args.encode)
    print(res, file=stdout)
    log(f"Message length: {len(res)} characters", file=stderr)
    log("", file=stderr)

    
    if args.encode:
        hexcontent = " ".join([str(hex(ord(char))) for char in res])
        log(f"Message '{hexcontent}'", stderr)


    exit(0)
