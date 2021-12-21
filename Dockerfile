FROM jupyter/scipy-notebook


COPY pythonRequirements.txt ./pythonRequirements.txt
COPY icdc-mock-data-specs_2.yaml ./icdc-mock-data-specs_2.yaml
COPY icdc-model.yaml ./icdc-model.yaml
COPY icdc-model-props.yaml ./icdc-model-props.yaml
COPY props-icdc-pmvp.yml ./props-icdc-pmvp.yml
COPY synthetic_data_values.xlsx ./synthetic_data_values.xlsx
COPY bento-synthetic-data-generator.ipynb ./bento-synthetic-data-generator.ipynb

RUN pip install -r pythonRequirements.txt