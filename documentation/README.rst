# Dork

Dork is a text based exploration game full of mystery, intrigue, but most importantly memes!  
The player finds him/herself in an exciting randomly generated maze where they can interact with rooms and various unique items. 
Using cardinal directions and simple commands, the player navigates throughout the maze to find him/herself at the end of the road. 
Be careful not to stumble upon Trolly McTrollFace...

## Getting Started

You will need to have an IDE installed on your computer that is compatible with python programs. 
Here are some resources for installing an IDE to your computer (Choose the correct download for your operating system):

To download visual studio code:
https://code.visualstudio.com/

To download eclipse:
https://www.eclipse.org/downloads/

To download intelliJ:
https://www.jetbrains.com/idea/download/#section=windows

Downloading Python3:
------------------------

Next you will need to install Python 3.0.
To install Python3, select the download option appropriate for your OS from the following link below:
https://www.python.org/downloads/

Cloning the "Dork" Repository:
------------------------

You can clone the Dork repository onto your local machine using this link:
https://github.com/GitNickProgramming/Dork.git

Setting up a Virtual Environment:
------------------------

To set up a development environment, I'd recommend setting up a virtual environment. 

If using a version of python installed from python.org that is version 3.0 or newer, pip is already installed on your computer. 
If the "pip" commands are not recognizable, you can download pip using this link:

For Windows users:
------------------------

Right click on this link and then click "save link as" and save to a safe location. 
https://bootstrap.pypa.io/get-pip.py 

Using command line navigate to the get-pip.py file and run the following command:

```
python get-pip.py
```

For Mac users:
------------------------

An easy way to handle installation packages is to use HomeBrew. 
Open your command terminal and use the following command:
```
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Continue through the installation process until a successful installation message appears. 
For verification you can use the following command to check for any errors.
```
brew doctor
```

Once HomeBrew is successfully installed, you can install pip using this command.  
This will install the latest version of python which will include pip. 
```
brew install python 
```

Setting up a virtual environment using pip:

For Windows users:
------------------------

Use the following command:
```
pip install virtualenv
```

Then using command line navigate to your project's file and activate your virtual environment.
```
virtualenv env
```

For Mac users:
------------------------

Using command line, navigate to your project's folder and then use the following command:
```
 virtualenv yourenv -p python3.6
 ```

You can name your virtual environment whatever you'd like. Then you'll need to activate the virtual environment using the command below:
```
source bin/activate
```

This should activate your virtual environment in the folder of your choosing. 

### Prerequisites

You will also need to install the requirements-dev.txt using pip commands in your terminal.  
The command below will install any needed extensions for running and testing the program. 
```
pip install -r documentation/requirements-dev.txt
```

## Running the tests

The requirements-dev.txt folder should automatically install any packages needed to run and identify the tests for the program. 

To run tests, open your IDE's command prompt and type,
```
Python: Configure Tests
```
Choose to configure tests using Pytest framework (Pytest should already be installed) and navigate to the "tests" folder.  
Then the following command prompt selection should run all tests using the correct framework. 
```
Python: Run All Tests
```

## Running the Program

To start the game, you must type this single command in your terminal within the folder where you have saved the game.
The command line should recognize the virtual environment as well. 
```
python -m dork 
```
## Deployment

There will be no further support for this project by the original development team, the project can be branched to create more content.

## Versioning

For the versions available, see the [tags on this repository](https://github.com/GitNickProgramming/Dork/tags).

## Development Leads

* **Peter Nielson** <peter@boxoforanmore.com>
* **James Morgan** <jmorga68@msudenver.edu>

## Contributers

* **Nick Gagliardi** <ngagliar@msudenver.edu>
* **Zachory Anguiano** <zanguian@msudenver.edu>
* **Fernando Babonoyaba** <fbabonoy@msudenver.edu>
* **Nicole Beck** <nbeck4@msudenver.edu>
* **Larsen Close** <lclose@msudenver.edu>
* **Devon DeJohn** <ddejohn@msudenver.edu>
* **David Dews** <ddews1@msudenver.edu>

See also the list of [contributors](https://github.com/GitNickProgramming/Dork/contributors) who participated in this project.

## License

MIT License

Copyright (c) 2019, Luke Smith

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## Acknowledgments

* 
* 
* 