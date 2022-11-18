## Backend Unit Test Is Called "unit_test.py" it's in the backend folder

## Set up PostgreSQL database
install postgresql v15.0
create the `localhost` server based on instruction
make sure to have database user account with the below credential:\
`username: postgres`\
`password: postgres`

## Setup Virtual Environment

Unix or MacOS (bash)
```
python3.10 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Windows (powershell)
```
python -3.10 -m venv .\venv
.\venv\Scripts/Activate.ps1
pip install -r requirements.txt
```
(if powershell throws an error saying the script is not digitally signed) 
```
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
```


!! Make sure you work in venv !!
  - On Unix or MacOS, using the bash shell: `source /path/to/venv/bin/activate`
  - On Unix or MacOS, using the csh shell: `source /path/to/venv/bin/activate.csh`
  - On Unix or MacOS, using the fish shell: `source /path/to/venv/bin/activate.fish`
  - On Windows using the Command Prompt: `path\to\venv\Scripts\activate.bat`
  - On Windows using PowerShell: `path\to\venv\Scripts\Activate.ps1`

## To run the live server:

`uvicorn main:app --reload`

this will create a new database "Ulivit", a new schema "CCC" and all the requried tables

to view api documentations after building, go to `http://127.0.0.1:8000/docs` if working on local host

## When working:

- If adding new dependency always add to requirements.txt file
  - `pip freeze > requirements.txt`
- To update your installation after a pull, simply run pip install again
  - `pip install -r requirements.txt`


