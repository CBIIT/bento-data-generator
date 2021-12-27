# bento-synthetic-data-generator
Code to generate synthetic data for the CRDC data models.

To run the Jupyter Notebook in Docker, the user should take the following steps:<br/>
(1) Install Docker if the user does not have Docker running in their system.<br/>
(2) The user can build the docker images using the command below. Note that the user can give any name, not necessarily “datagenerator”. Be careful, do not forget the period!<br/>
```docker build -t datagenerator .```<br/>
(3) The user can check the image using the command below or open the “Images” section in the Docker Desktop application.<br/>
```docker images```<br/>
(4) The user can use the command below to run the images. After the user types the command, the console will give the user serval URLs. The user should copy-paste the last URL to the browser to get the Jupyter Notebook. The user can press control + c to stop the image.<br/>
```docker run -v ${PWD}:/home/jovyan -it -p 8888:8888 datagenerator```<br/>
If the user are using Windows Command Prompt, the use should use the command below instead.
```docker run -v "%cd%":/home/jovyan -it -p 8888:8888 datagenerator```<br/>
