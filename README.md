# Hide your messages 

This command line tool allows to encode text into a invisible and zero width subset of unicode characters.

Since unicode is rendered differently by different libaries the list of invisible characters must be altered accordingly. 
The default set has been tested at `PopOs! 22.04`.

# How the encoding works
1. First, we convert the input text into base `n-1` representation.
2. Then we map each digit `d` to the `d-th` character inside the list of invisible characters.
3. Finally, we insert between each base `n-1` number the `n-th` invisible character as separator.

Decoding can be achieved by following these steps in reverse.

Using a higher base then two for representing invisible characters allows a more compact representation.

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
❯ Start:͏‌‌‏​⁠؜⁠​⁠﻿⁠​‏‌​‌‏؜​⁠؜⁠​⁠﻿⁠​⁠؜‌​‌‍‍​‏‌​‌‍﻿​‏‌​⁠﻿﻿​‌‍‏​‌‍⁠​⁠﻿؜​‌‍‏​⁠﻿‌​‌‍‏​﻿‍‎:End # Try to move your cursor through this output.
foo@bar:~$ cat out.txt | python3 ./cli.py -d
>>> This should be invisible!
```

# known issues
- On windows command line unicode output is probably not working, try to use `wsl`.

