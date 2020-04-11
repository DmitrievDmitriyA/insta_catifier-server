import re


def validateEmail(email):
    # regural expression that used to validate email
    regex = '^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$'

    if(re.search(regex, email)):
        return True
    else:
        return False


def validateInstagramAccount(instagramAccount):
    # regural expression that used to validate user name
    regex = '^(?!.*\.\.)(?!.*\.$)[^\W][\w.]{0,29}$'

    if(re.search(regex, instagramAccount)):
        return True
    else:
        return False
