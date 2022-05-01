# Before Starting

these are following recommendations given to start this chess python program

this steps are recommended only for ubuntu users, other os users please follow their respective os commands

we isntall python3.5 because pygame works only with python3.5

## Install Python3.5
```
sudo add-apt-repository ppa:fkrull/deadsnakes
sudo apt-get update
sudo apt-get install python3.5
```
Reference : [Python3.5 installation suggestions](https://stackoverflow.com/a/38393177/8820616)

## Make Python3.5 as temporary python

A simple safe way would be to use an alias , example
```
$ python --version
Python 3.9.5
$ python3.5 --version
Python 3.5.10
$ alias python=python3.5
$ python --version
Python 3.5.10
```
this will be in your present shell, if you open another shell it would not be present 

i have set python default version to 3.9 you may have Python 2.7 

**Important Note:**
To disable the alias in the current shell use the `unalias` built-in command:
```
$ unalias python
$ python --version 
Python 3.9.5
```

## Install pygame into python3.5

- to install pygame to python3.5 do 
```
python3.5 -m pip install pygame
```
or if you have done alias
```
python -m pip install pygame
```
- to check pygame is working do 
```
python3.5 -m pygame.examples.aliens
```
or if you have done alias
```
python -m pygame.examples.aliens
```
## Export this repo to PythonPath 

Stay in `Chess_workout` Dir and Execute 
```
export PYTHONPATH=$(pwd)
```
to avoid import module errors 

## Run the Chess main file

be present inside `Chess_workout/Chess` dir and run 
```
python3.5 ChessMain.py 
```
or if you have done alias
```
python ChessMain.py 
```