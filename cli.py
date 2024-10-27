from Translator import CharsetTranslatorBuilder
import sys


# invisible characters

unicode_invisible = {'\u3000', 'ᅟ', 'ㅤ', '\u200b', '\u2000', '\t', '\u2002', '\u180e', '\u2005', '\u200f', '\u200c', '\u2004', '\u205f', '\u2003', '⠀', '\u2008', 'ﾠ', 'ᅠ', '\xa0', '\u2006', ' ', '\ufeff', '\u2001', '͏', '\u202f', '\u2060', '\u200d', '\u061c', '\u2009', '\u2007', '\u200e', '\u200a'}


unicode_invisible_zero_width = [
        #chr(0x2067), # right to left isolate
        #chr(0x2066), # left to right isolate
        chr(0x34f),
        #chr(0x2063),
        chr(0x200e),
        #chr(0x2069),
        #chr(0x2065),
        chr(0x200b),
        #chr(0x2064),
        #chr(0x17b4),
        chr(0x61c),
        chr(0xfeff),
        #chr(0x2061),
        chr(0x200c),
        chr(0x2060),
        #chr(0x2068),
        chr(0x200d),
        #chr(0xad),
        chr(0x200f),
        #chr(0x1d173),
        #chr(0x1d174),
        #chr(0x1d159),
        #chr(0x1d175),
        #chr(0x1d176),
        #chr(0x1d177),
        #chr(0x1d178),
        #chr(0x1d17a),
        # chr(0x180e), # seems not to work without suffix
        ]

# configuration
prefix                          = 1 * unicode_invisible_zero_width[0]
suffix                          = 1 * unicode_invisible_zero_width[1]
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
                        default=False, 
                        required=False, 
                        help="enable debug logs into stderr"
                        )
    args = parser.parse_args(sys.argv[1:])

    # create translator chain

    builder = CharsetTranslatorBuilder()\
        .setCharset("".join(invisible_zero_width_alphabet))\
        .setSeparator(invisible_separator)\
        .setPrefixSuffix(prefix, suffix)

    translator = builder.build()

    # run stuff 


    content = stdin.read()
    log(f"using sequences start: '{hex(ord(prefix))}' and end: '{hex(ord(suffix))}'", stderr)
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
