# check_mensa
Grabs the meals from the API of Studierendenwerk

## Install
    pip install -r requirements.txt

## Run
create a cronjob running this script.
This cronjob notifies quick enough:

    #mensa linsen check
    0 5,17 * * *  cd /home/user/ && python3 check_mensa_meals.py