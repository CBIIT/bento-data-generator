FROM jupyter/scipy-notebook

COPY pythonRequirements.txt ./pythonRequirements.txt

ENV JUPYTER_ALLOW_INSECURE_WRITES=true

RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r pythonRequirements.txt
