from Translator import CharsetTranslatorBuilder
import sys

zero_width_space = "​"
invisible_comma = "⁣"
invisible_plus = "⁤"
left_to_right_isolator = "⁦"
right_to_left_isolator = "⁧"
strong_isolator = "⁨"
pop_isolator = "⁩"
symmectric_trade = "⁪"
activate_symmectric_trade = "⁫"

invisible_characters = [
                        invisible_comma,
                        invisible_plus,
                        left_to_right_isolator,
                        right_to_left_isolator,
                        strong_isolator,
                        pop_isolator,
                        symmectric_trade,
                        activate_symmectric_trade,
                       ]
invisible_separator = zero_width_space

builder = CharsetTranslatorBuilder()\
    .setCharset("".join(invisible_characters))\
    .setSeparator(invisible_separator)\
    .setSequences("Start:", ":End")
translator = builder.build()



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

    parser = ArgumentParser(
            prog="InvisibleUnicodeText",
            description="Encodes or decodes the given text into invisilbe unicode text.",
            epilog="The result is forwarded to stdin. Log messages are send to stderr. \nmade by Bruno")
    parser.add_argument("-d", "--decode", dest="encode", action="store_false", default=True, required=False, help="switch from encoding to decoding stdin")
    parser.add_argument("--debug", dest="debug", action="store_true", default=False, required=False, help="enable debug logs into stderr")
    args = parser.parse_args(sys.argv[1:])

    def log(msg, file):
        if args.debug:
            print(msg, file=file)

    stdin = sys.stdin
    stdout = sys.stdout
    stderr = sys.stderr

    content = stdin.read()
    if args.encode:
        log(f"Encoding {len(content)} characters.", file=stderr)
    else:
        log(f"Decoding {len(content)} characters.", file=stderr)

    res = main(content, args.encode)
    print(res, file=stdout)
    log(f"Message length: {len(res)} characters", file=stderr)
    log("", file=stderr)
    exit(0)
