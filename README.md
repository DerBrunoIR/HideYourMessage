# Requirements 

- python 3.10.6 (perhaps it works with older versions too)
- tested on ubuntu 22.04

# Usage
```bash 
python3 ./cli.py [--debug] [-d,--decode]
```
This scripts reads alle text from **stdin** and outputs the invisible unicode ecoded text to **stdout**.

# Example script 

```console
message="This should be invisible!"
# encode
invisible=$(echo "$message" | python3 ./cli.py)
echo "$invisible"
>>> Start::End
# decode
echo "$invisible" | python3 ./cli.py -d
>>> expected output "This should be invisible!"
```
