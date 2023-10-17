# check_mensa
Grabs the meals from the API of Studierendenwerk at Mensa Uni Stuttgart-Vaihingen.

## Install
    pip install -r requirements.txt

## config
create your own config by copying config.example.json to config.json and altering the settings.
Be sure to check that you can access the mail server from public.
Some providers have different login passwords for web and smtp.

    "IntrestMeals" : {"Linsen": "example2@domain2.com", "mealname": "example3@domain3.co.uk"}

contains a dict of meals to check. the script checks for each string of the keys to be part of the "meal" inside the API-Json response.

## Run
create a cronjob running this script.
This cronjob notifies quick enough:

    #mensa linsen check
    0 5,17 * * *  cd /home/user/ && python3 check_mensa_meals.py
