FROM jupyter/scipy-notebook

COPY pythonRequirements.txt ./pythonRequirements.txt

RUN pip install -r pythonRequirements.txt