This command line tool allows to encode and decode text into and into invisible unicode characters.
Since unicode is rendered differently the set of invisible characters must be altered for different platforms then `Ubuntu 22.04`.

# Requirements 

- python 3.10.6
- tested on ubuntu 22.04
- Bash scripts requires `xclip`, on ubuntu you can install it by `sudo apt install xclip`

# Usage
```bash 
python3 ./cli.py [--debug] [-d,--decode]
```
This script reads alle text from **stdin** and outputs the invisible unicode ecoded text to **stdout**.
The default is encoding. 
All invisible text will be outputed between a start and end sequence, otherwise it would be hard to find.
Make sure your terminal supports unicode.

# setup 
- `git clone https://github.com/DerBrunoIR/Translator`
- `cd ./Translator`

# running via bash scripts
```console 
foo@bar:~$ ./write
Some hidden text
❯ stdout copied to clipboard!
foo@bar:~$ ./read 
[Ctrl-V]⁥⁠͏​‏͏​‍͏​⁤­͏‎﻿͏​𝅶͏​⁤͏
❯ Some hidden text
```

# running via python script 
```console
foo@bar:~$ echo "This should be invisible!" | python3 ./cli.py > out.txt
foo@bar:~$ cat out.txt
❯ Start:͏‌‌‏​⁠؜⁠​⁠﻿⁠​‏‌​‌‏؜​⁠؜⁠​⁠﻿⁠​⁠؜‌​‌‍‍​‏‌​‌‍﻿​‏‌​⁠﻿﻿​‌‍‏​‌‍⁠​⁠﻿؜​‌‍‏​⁠﻿‌​‌‍‏​﻿‍‎:End
foo@bar:~$ cat out.txt | python3 ./cli.py -d
>>> This should be invisible!
```

# known issues
- On windows unicode encoding migh not be supported by the terminal.

