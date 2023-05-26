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

builder = CharsetTranslatorBuilder("".join(invisible_characters), invisible_separator)
translator = builder.build()

if __name__ == "__main__":
    with open("message.txt", "r") as f:
        text = f.read()

        print(f"len(text)={len(text)}")
        encoded_text = translator.encode(text)
        print("len(encoded_text) =", len(encoded_text))
        decoded_text = "".join(translator.decode(encoded_text))
        print(f"len(decoded_text)={len(decoded_text)}")
        assert decoded_text == text, "Encoding issue! Encoded text unequals decoded text!"

    with open("invisible.txt", "w") as f:
        f.write(encoded_text)

    print("saved to './invisible.txt'")
