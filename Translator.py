from __future__ import annotations
from typing import TypeVar, Protocol, Iterable, Any, Callable
import string
import re


# debugging decorator
debug_global_indentation_count = 0
def debug(func):
    def wrapper(*args, **kwargs):
        global debug_global_indentation_count
        indent = "-    " * debug_global_indentation_count

        print(indent + f"{func.__name__} args={args} kwargs={kwargs}")
        debug_global_indentation_count += 1
        res = func(*args, **kwargs)
        debug_global_indentation_count -= 1
        print(indent + f"{func.__name__} result={res}")
        return res 
    return wrapper


# python type hint genercis
E = TypeVar("E")
D = TypeVar("D")


# describes a translation, process where information can be lossless translated into another representation.
class TranslatorInterface(Protocol[E, D]):
    def encode(self, obj: E) -> D:
        raise NotImplementedError()

    def decode(self, obj: D) -> E:
        raise NotImplementedError()

    def __repr__(self):
        return f"<TranslatorInterface>"



class UnicodeToInteger(TranslatorInterface[str, int]):
    """
    python unicode character -> python int
    """

    def encode(self, char: str) -> int:
        if len(char) != 1:
            raise ValueError(f"Expected char not str! Got {char}")
        return ord(char)
    
    def decode(self, number: int) -> str:
        if not 0 <= number <= 255: # TODO add support for all unicode characters
            raise ValueError(f"number must be between 0 and 255, got {number}")
        return chr(number)

    def __repr__(self):
        return f"<UnicodeToInteger>"



class Base10ToBaseNString(TranslatorInterface[str, int]):
    """
    translates base 10 numbers into base n numbers

    base: new base
    digits: digits for new base representation, ith-element represents ith-digit.
    padding: number of preprended zeros.
    
    base 10 python integer -> base n python unicode digit
    """

    base: int 
    digits: str
    prepend: int 
    

    def __init__(self, base: int, digits: str, prepend: int = 0):
        if base < 2:
            raise ValueError(f"base musst be >= 2, got {base}")
        self.digits = digits
        if len(self.digits) < base:
            raise ValueError(f"len(digits) musst be >= base, got {len(digits)}")

        self.base = base
        self.prepend = prepend


    def encode(self, decimal: int) -> str:
        """
        base 10 -> base n 
        """

        if not isinstance(decimal, int):
            raise TypeError(f"decimal musst be int, got {decimal}")

        if decimal == 0:
            return '0'

        digits = []
        neg = False
        if decimal < 0:
            neg = True
            decimal *= -1

        while decimal:
            digit = self.digits[decimal % self.base]
            digits.append(digit)
            decimal //= self.base 

        if neg:
            digits.append('-')

        while len(digits) < self.prepend:
            digits.append(self.digits[0]) 

        return "".join(digits[::-1])


    def decode(self, num: str) -> int:
        """
        base n -> base 10
        """

        if not isinstance(num, str):
            raise TypeError(f"num musst be str, got {num}")

        neg = False
        if num[0] == '-':
            neg = True 
            num = num[1:]

        decimal = 0
        for (i, digit) in enumerate(num[::-1]):
            idx = self.digits.index(digit)
            decimal += idx * self.base ** i

        if neg:
            decimal *= -1

        return decimal



class Inverted(TranslatorInterface[E, D]):
    def __init__(self, t: TranslatorInterface[D, E]):
        self.t = t

    def encode(self, obj: E):
        return self.t.decode(obj)

    def decode(self, obj: D):
        return self.t.encode(obj)




class Mapped(TranslatorInterface[Iterable[E], Iterable[D]]):
    """
        translates a sequence of elements by using a element translator
    """

    def __init__(self, itemTranslator: TranslatorInterface):
        self.translator = itemTranslator


    def encode(self, l: Iterable[E]) -> Iterable[D]:
        return (
            self.translator.encode(item) for item in l
        )


    def decode(self, l: Iterable[D]) -> Iterable[E]:
        return (
            self.translator.decode(item) for item in l
        )


    def __repr__(self):
        return f"<Mapped itemTranslator={self.translator}>"



class Replace(TranslatorInterface[E,D]):
    """
    translates elements by using a dictionary mapping.
    E -> D 
    """

    mapping: dict[E,D]
    mapping_inv: dict[D, E]


    def __init__(self, mapping: dict[E, D]):
        self.mapping = mapping
        self.mapping_inv = {v: k for (k, v) in mapping.items()}


    def encode(self, obj: E) -> D:
        return self.mapping[obj]


    def decode(self, obj: D) -> E:
        return self.mapping_inv[obj]


    def __repr__(self):
        return f"<Replace mapping={self.mapping}>"



class Function(TranslatorInterface[E, D]):
    """
    Translates by using a function f and it's reverse function f_inv.
    """
    
    f: Callable[[E], D]
    f_inv: Callable[[D], E] 

    def __init__(self, f: Callable[[E], D], f_inv: Callable[[D], E]):
        self.f = f
        self.f_inv = f_inv

    def encode(self, obj: E):
        return self.f(obj)

    def decode(self, obj: D):
        return self.f_inv(obj)
    
    def __repr__(self):
        return f"<Function f={self.f} f_inv={self.f_inv}>"


class Chained(TranslatorInterface[E, D]):
    """
    Translates by using translator t1 and translator t2 in sequence.
    """
    
    t1: TranslatorInterface
    t2: TranslatorInterface

    def __init__(self, t1: TranslatorInterface[E, Any], t2: TranslatorInterface[Any, D]):
        self.t1 = t1 
        self.t2 = t2 

    def encode(self, obj: E) -> D:
        tmp = self.t1.encode(obj)
        return self.t2.encode(tmp)
    
    def decode(self, obj: D) -> E:
        tmp = self.t2.decode(obj)
        return self.t1.decode(tmp)

    def __repr__(self):
        return f"<Chained left={self.t1} right={self.t2}>"
        

class BuilderInterface(Protocol):
    def build(self):
        pass

class ChainTranslatorBuilder(BuilderInterface):
    """
    Allows the building of complex translator chains.
    """
    
    translators: list[TranslatorInterface[Any, Any]]
    
    def __init__(self):
        self.translators = []
    
    def add(self, t: TranslatorInterface[Any, Any]):
        self.translators.append(t)
        return self

    def addAll(self, ts: Iterable[TranslatorInterface[Any, Any]]):
        self.translators.extend(ts)
        return self

    def build(self) -> TranslatorInterface[Any, Any]:
        if len(self.translators) == 0:
                raise RuntimeError("Can't build TranslatorChain without translators!")
        elif len(self.translators) == 1:
            return self.translators[0]

        T = Chained(*self.translators[:2])
        for t in self.translators[2:]:
            T = Chained(T, t)
        return T


class AddPrefixSuffix(TranslatorInterface[str,str]):
    """
    Translates a string with certain prefix and suffix to a string without those.
    """
    
    prefix: str 
    ennd_seq: str 
    pattern: re.Pattern

    def __init__(self, prefix: str, suffix: str):
        self.prefix = prefix
        self.suffix = suffix
        self.pattern = re.compile(f"{self.prefix}.*{self.suffix}", re.UNICODE)

    def encode(self, rawMsg: str) -> str:
        return f"{self.prefix}{rawMsg}{self.suffix}"

    def decode(self, text: str) -> str:
        for match in self.pattern.finditer(text):
            candidate = match.group()
            return self.decodeCandidate(candidate)
        raise ValueError("No message found!")

    def decodeCandidate(self, embeddedMsg: str) -> str:
        if not embeddedMsg.startswith(self.prefix):
            raise ValueError(f"Message doesn't start with the expected start sequence. Instead of '{self.prefix}', '{embeddedMsg[:10]}' was found!")
        if not embeddedMsg.endswith(self.suffix):
            raise ValueError(f"Message doesn't end with the expected end sequence. Instead of '{self.suffix}', '{embeddedMsg[-10:]}' was found!")
        left_offset = len(self.prefix)
        right_offset = len(self.suffix)
        msgLen = len(embeddedMsg)
        return embeddedMsg[left_offset: msgLen-right_offset]

    def __repr__(self):
        return f"<AddPrefixSuffix prefix='{self.prefix}' suffix='{self.suffix}'>"



class CharsetTranslatorBuilder(BuilderInterface):
    """
    Builder for a translator that translates a string between representations using two different sized character sets.
    """
    
    translator: TranslatorInterface[Any, Any]
    charset: str
    separator: str
    prefix: str
    suffix: str

    def setCharset(self, charset: str) -> CharsetTranslatorBuilder:
        self.charset = charset
        return self

    def setSeparator(self, separator: str) -> CharsetTranslatorBuilder:
        self.separator = separator
        return self

    def setPrefixSuffix(self, prefix: str, suffix: str) -> CharsetTranslatorBuilder:
        self.prefix = prefix
        self.suffix = suffix
        return self

    def build(self) -> TranslatorInterface[str, str]:
        charset = self.charset
        separator = self.separator
        prefix, suffix = self.prefix, self.suffix
        

        digits = string.digits + string.ascii_letters
        for i in range(len(digits), len(charset)):
            digits += chr(i)
       
        replacement = {
                digits[i]:charset[i] for i in range(0, len(charset))
                }

        pipe = [
                Mapped(
                    UnicodeToInteger()
                    ),
                Mapped(
                    Base10ToBaseNString(
                        base=len(charset),
                        digits=digits
                        )
                    ),
                Mapped( 
                    Function( # list to str
                        f=str,
                        f_inv="".join,
                        )
                    ),
                Mapped(
                    Mapped(
                        Replace(
                            mapping=replacement
                            )
                        )
                    ),
                Mapped(
                    Function(
                        "".join,
                        list
                    )
                ),
                Function(
                    separator.join, 
                    lambda x: x.split(separator) 
                    ),
                AddPrefixSuffix(
                    prefix=prefix,
                    suffix=suffix,
                    )
                ]

        builder = ChainTranslatorBuilder()
        return builder.addAll(pipe).build()


