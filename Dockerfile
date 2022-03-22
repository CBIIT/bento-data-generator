FROM python:3

WORKDIR /usr/app/src

COPY bento-synthetic-data-generator.py ./

COPY pythonRequirements.txt ./pythonRequirements.txt

RUN pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org -r pythonRequirements.txt

CMD [ "python", "./bento-synthetic-data-generator.py", "configuration_files_bento.yaml" ]