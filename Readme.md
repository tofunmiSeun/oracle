### Launching app
1. Install required packages using `pip install -r requirements.txt`
2. Create a `.env` file in the root folder of the application and provide the required environmental variables as listed in `loaded_env_variables.py`
3. Run `uvicorn main:app --reload --port=3444`

### Installing new packages
If a new package is installed using `pip install`, be sure to add this new requirement to the **requirements.txt** file using `pip freeze > requirements.txt`