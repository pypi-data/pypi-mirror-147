# CINI_selector

This repository that build and is the standard CINI selector for differrent use. It is not a package but it is useful to use it in different python projects.

## prerequisites

Has anaconda installed on windows. And configured you system variables ($path) of anaconda on windows: 
* C:\ProgramData\Anaconda3
* C:\ProgramData\Anaconda3\Scripts
* C:\ProgramData\Anaconda3\Library\bin

## Test protocol

1. Clone the github repository.
```
$ git clone https://github.com/R-Rijnbeek/CINI_selector.git
```

2. Enter the project folder.
```
$ cd CINI_selector
```

3. Build the virtual environment on the repository by running:
```
$ build.bat
```

4. To activate the environmet and run the test scripts:
```
$ activate ./env
$ python TESTS/__init__.py
```

Then you can use the 'cini' directory as a local package

## Development protocol

1. Clone the github repository.
```
$ git clone https://github.com/R-Rijnbeek/CINI_selector.git
```

2. Enter the project folder.
```
$ cd CINI_selector
```

3. Build the virtual environment on the repository by running:
```
$ configuration_build.bat
```

4. Once created the virtual environment. To activate it and use all content of the repository
```
$ activate ./build_env
```

5. Once activated the environment. Then you can use also the scripts inside the 'BUILDER' derictory. 

## Notes to know: 

1. The dependencies to use all features of this repository are writed on the environmet.yml file
3. This repository is tested with windows 10 and anaconda version 4.11.0
