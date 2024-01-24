### Launching app
1. Install required packages using `pip install -r requirements.txt`
2. Run `uvicorn main:app --reload --port=3000`

### Installing new packages
If a new package is installed using `pip install`, be sure to add this new requirement to the **requirements.txt** file using `pip freeze > requirements.txt`