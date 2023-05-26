from Translator import Base10ToBaseNTranslator

class TestNumberBaseTranslator:
    def test_1(self):
        t = Base10ToBaseNTranslator(2)
        
        assert t.decode("1000") == 8 
        assert t.decode("1011") == 11
        assert t.decode("0") == 0
        assert t.decode("10") == 2
        assert t.decode("-10") ==  -2

        assert t.encode(8) == "1000"
        assert t.encode(11) == "1011"
        assert t.encode(0) == "0"
        assert t.encode(2) == "10"
        assert t.encode(-2) == "-10"



    def test_2(self):
        for base in range(2, 20, 3):
            t = Base10ToBaseNTranslator(base)
            for num in range(-100, 100, 7):
                e = t.encode(num)
                d = t.decode(e)
                assert num == d

    def test_3(self):
        t = Base10ToBaseNTranslator(27)
        assert t.encode(72) == "2i"


if __name__ == "__main__":
    test = TestNumberBaseTranslator()
    test.test_1()
    test.test_2()
    test.test_3()
