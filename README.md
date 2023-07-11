# Requirements 

- python 3.10.6 (perhaps it works with older versions too)
- tested on ubuntu 22.04
- Bash scripts require `sudo apt install xclip`

# Usage
```bash 
python3 ./cli.py [--debug] [-d,--decode]
```
This script reads alle text from **stdin** and outputs the invisible unicode ecoded text to **stdout**.
The default is encoding. 
All invisible text will be outputed between a start and end sequence, otherwise it would be hard to find.

# install
- `git clone https://github.com/DerBrunoIR/Translator`
- `cd ./Translator`
  
# running python script 

```console
foo@bar:~$ echo "This should be invisible!" | python3 ./cli.py > out.txt
foo@bar:~$ cat out.txt
>>> Start::End
foo@bar:~$ cat out.txt | python3 ./cli.py -d
>>> This should be invisible!
```
Do not forget the start and end sequences at decoding!

# running bash scripts
```console 
hiddenText on  main via 🐍 v3.10.6 
❯ ./write
Some hidden text
stdout copied to clipboard!

hiddenText on  main via 🐍 v3.10.6 took 3s 
❯ ./read 
[Ctrl-V]⁥⁠͏​‏͏​‍͏​⁤­͏‎﻿͏​𝅶͏​⁤͏
Some hidden text
```

