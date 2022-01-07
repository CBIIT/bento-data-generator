FROM jupyter/scipy-notebook

COPY pythonRequirements.txt ./pythonRequirements.txt

RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r pythonRequirements.txt