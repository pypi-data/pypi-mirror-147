# CINI_selector

This repository that build and is the standard CINI selector for differrent use. 

The oficial description of the requisites of the CINI code are writed on: https://www.boe.es/diario_boe/txt.php?id=BOE-A-2019-6181

## prerequisites

Has anaconda installed on windows. And configured you system variables ($path) of anaconda on windows: 
* C:\ProgramData\Anaconda3
* C:\ProgramData\Anaconda3\Scripts
* C:\ProgramData\Anaconda3\Library\bin

## Deploy new version:

1. Adapt the __version__ tag insite the python module: `/src/cini_selector/__init__.py`

2. Execute the command: 
```
$ deploy.bat
```
* ad some point of the deployment process you need provide a valid username and password of the pypi account
## Testing

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

Then you can use the 'TESTS' directory to test the package

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

5. Once activated the environment. Then you can use also the scripts inside the 'BUILDER' directory. 

## Notes to know: 

1. The dependencies to use all features of this repository are writed on the environmet.yml file
3. This repository is tested with windows 10 and anaconda version 4.11.0
