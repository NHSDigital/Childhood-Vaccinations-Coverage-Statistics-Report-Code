Repository owner: [NHS Digital](https://github.com/NHSDigital)

Email: imms@nhs.net

To contact us raise an issue via email and we will respond promptly.

## Clone repository
To clone respositary, please see our [community of practice page](https://github.com/NHSDigital/rap-community-of-practice/blob/main/development-approach/02_using-git-collaboratively.md).

## Set up environment
There are two options to set up the python environment:
1.1 Pip using `requirements.txt`.
1.2. Conda using `environment.yml`.

Users would need to delete as appropriate which set they do not need. For details, please see our [virtual environments in the community of practice page](https://github.com/NHSDigital/rap-community-of-practice/blob/main/python/virtual-environments.md).


Run the following command in Terminal or VScode to set up the package
```
pip install --user --no-warn-script-location -r requirements.txt
```

or if using conda environments:
```
conda env create -f environment.yml
```

The first line of the `.yml` file sets the new environment's name. In this template, the name is `rap`.

2. Activate the new environment: 
```
    conda activate <enviroment_name>
```

3. Verify that the new environment was installed correctly:
```
   conda env list
```

# Package structure:
```
childhood-vaccinations-rap
│   README.md
│
├───child_vac_code
│   │   create_publication.py
│   │   create_validations.py
│   │   parameters.py
│   │
│   └───utilities
│       │   charts.py
│       │   csvs.py
│       │   dashboards.py
│       │   data_connections.py
│       │   field_definitions.py
│       │   helpers.py
│       │   load.py
│       │   logger_config.py
│       │   pre_processing.py
│       │   processing.py
│       │   publication_files.py
│       │   tables.py
│       │
│       └──────write
│       │        │   write_data.py
│       │        └─  write_format.py
│       │
│       └──────validations
│               │   validations_data.py
│               └─  validations_processing.py
│
└───tests
    ├───unittests
            │   test_data_connections.py
            │   test_field_definitions.py
            │   test_helpers.py    
            └─  test_processing.py
```
# Running the pipeline

There are two main files that users running the process will need to interact with:
    * [parameters.py](child_vac_code/parameters)
    * [create_publication.py](child_vac_code/create_publication)

The file parameters.py contains all of the things that we expect to change from one publication
to the next. Indeed, if the methodology has not changed, then this should be the only file you need
to modify. A few elements require updating each year (e.g. the reporting year), but most
are likely to only require occassional updates (e.g. file paths, default codes).
It also allows the user to control which parts of the publication they want the pipeline to produce.

The publication process is run using the top-level script, create_publication.py.
This script imports and runs all the required functions from the sub-modules.

# Link to publication
https://digital.nhs.uk/data-and-information/publications/statistical/nhs-immunisation-statistics

# Licence
The NHS England Childhood Vaccination Coverage Accredited Official Statistics publication codebase is release under the MIT License.
The documentation is © Crown copyright and available under the terms of the [Open Government 3.0 licence](https://www.nationalarchives.gov.uk/doc/open-government-licence/version/3/).
