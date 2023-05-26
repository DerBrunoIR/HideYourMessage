from typing import TypeVar, Protocol, Iterable, Any, Callable
import string

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

E = TypeVar("E")
D = TypeVar("D")
class TranslatorInterface(Protocol[E, D]):
    def encode(self, obj: E) -> D:
        raise NotImplementedError()

    def decode(self, obj: D) -> E:
        raise NotImplementedError()

    def __repr__(self):
        return f"<TranslatorInterface>"



class UnicodeCharacterTranslator(TranslatorInterface[str, int]):
    """
    str -> int
    """

    def encode(self, char: str) -> int:
        if len(char) != 1:
            raise ValueError(f"Expected char not str! Got {char}")
        return ord(char)
    
    def decode(self, number: int) -> str:
        if not 0 <= number <= 255:
            raise ValueError(f"number must be between 0 and 255, got {number}")
        return chr(number)

    def __repr__(self):
        return f"<UnicodeCharacterTranslator>"



class Base10ToBaseNTranslator(TranslatorInterface[str, int]):
    """
    int -> str
    translates base 10 numbers into base n numbers
    """

    base: int 
    digits: str
    padding: int 
    

    def __init__(self, base: int, digits: str, padding: int = 0):
        if base < 2:
            raise ValueError(f"base musst be >= 2, got {base}")
        self.digits = digits
        if len(self.digits) < base:
            raise ValueError(f"len(digits) musst be >= base, got {len(digits)}")

        self.base = base
        self.padding = padding


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

        while len(digits) < self.padding:
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



class InvertedTranslator(TranslatorInterface[E, D]):
    def __init__(self, t: TranslatorInterface[D, E]):
        self.t = t

    def encode(self, obj: E):
        return self.t.decode(obj)

    def decode(self, obj: D):
        return self.t.encode(obj)



class IterableTranslator(TranslatorInterface[Iterable[E], Iterable[D]]):


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
        return f"<IterableTranslator itemTranslator={self.translator}>"



class StringReplacementTranslator(TranslatorInterface[E,D]):
    """
    int -> str 
    """

    charset: dict[E,D]
    charset_inv: dict[D, E]


    def __init__(self, charset: dict[E, D]):
        self.charset = charset
        self.charset_inv = {v: k for (k, v) in charset.items()}


    def encode(self, obj: E) -> D:
        return self.charset[obj]


    def decode(self, obj: D) -> E:
        return self.charset_inv[obj]


    def __repr__(self):
        return f"<CharsetIndexTranslator charset={self.charset}>"



class FunctionTranslator(TranslatorInterface[E, D]):
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
        return f"<FunctionTranslator>"


class ChainedTranslator(TranslatorInterface[E, D]):
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
        return f"<ChainedTranslator left={self.t1} right={self.t2}>"
        

class BuilderInterface(Protocol):
    def build(self):
        pass

class ChainTranslatorBuilder(BuilderInterface):
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
        match self.translators:
            case 0:
                raise RuntimeError("Can't build TranslatorChain without translators!")
            case 1:
                return self.translators[0]
            case _:
                T = ChainedTranslator(*self.translators[:2])
                for t in self.translators[2:]:
                    T = ChainedTranslator(T, t)
                return T


class CharsetTranslatorBuilder(BuilderInterface):
    translator: TranslatorInterface[Any, Any]

    def __init__(self, charset: str, sep: str):

        digits = string.digits + string.ascii_letters
        for i in range(len(digits), len(charset)):
            digits += chr(i)
       
        replacement = {
                digits[i]:charset[i] for i in range(0, len(charset))
                }

        pipe = [
                IterableTranslator(
                    UnicodeCharacterTranslator()
                    ),
                IterableTranslator(
                    Base10ToBaseNTranslator(
                        len(charset),
                        digits
                        )
                    ),
                IterableTranslator(
                    FunctionTranslator(
                        str,
                        "".join
                        )
                    ),
                IterableTranslator(
                    IterableTranslator(
                        StringReplacementTranslator(
                            replacement
                            )
                        )
                    ),
                IterableTranslator(
                    FunctionTranslator(
                        "".join,
                        list
                    )),
                FunctionTranslator(
                    sep.join, 
                    lambda x: x.split(sep) 
                    ),
                ]

        builder = ChainTranslatorBuilder()
        self.translator = builder.addAll(pipe).build()


    def build(self):
        return self.translator

    
