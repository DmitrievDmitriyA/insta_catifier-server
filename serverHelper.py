import re


def validateEmail(email):
    # regural expression that used to validate email
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    if(re.search(regex, email)):
        return True
    else:
        return False
