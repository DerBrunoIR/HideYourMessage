# Requirements 

- python 3.10.6 (perhaps it works with older versions too)
- tested on ubuntu 22.04

# Usage
```bash 
python3 ./cli.py [--debug] [-d,--decode]
```
This scripts reads alle text from **stdin** and outputs the invisible unicode ecoded text to **stdout**.
The default is encoding. All invisible text will be outputed between a start and end sequence otherwise it would be hard to find.

# instalation
- `git clone https://github.com/DerBrunoIR/Translator`
- `cd ./Translator`
  
# minimal example 

```console
foo@bar:~$ invisible=$(echo "This should be invisible!" | python3 ./cli.py)
foo@bar:~$ echo "$invisible"
>>> Start::End
foo@bar:~$ echo "$invisible" | python3 ./cli.py -d
>>> This should be invisible!
```
Do not forget the start and end sequences at decoding!
