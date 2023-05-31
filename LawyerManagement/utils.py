import datetime
from UserAuthentication.models import Lawyer

def isPaymentRequired(lawyer):

    isRequired = False
    today = datetime.date.today()

    if lawyer.status == Lawyer.StatusList.HOLD:
        isRequired = True
    elif lawyer.expiary_date <= today:
        lawyer.status = Lawyer.StatusList.HOLD
        lawyer.save()
        isRequired = True
    else:
        isRequired = False

    return isRequired

