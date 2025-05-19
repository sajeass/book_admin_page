import time,datetime

def date_str(input_text,str_type='%Y.%m.%d'):
    today=datetime.datetime.today()
    
    if input_text == 'today':
        today=today.strftime(str_type)
        return today
    if input_text == 'yesterday':
        yesterday = today - datetime.timedelta(days=1)
        yesterday=yesterday.strftime(str_type)
        return yesterday
    if input_text == 'twodaysago':
        twodaysago = today - datetime.timedelta(days=2)
        twodaysago=twodaysago.strftime(str_type)
        return twodaysago
    if input_text == 'threedaysago':
        threedaysago = today - datetime.timedelta(days=3)
        threedaysago=threedaysago.strftime(str_type)
        return threedaysago
    if input_text == 'tomorrow':
        tomorrow = today + datetime.timedelta(days=1)
        tomorrow=tomorrow.strftime(str_type)
        return tomorrow
    if input_text == 'oneweekslater':
        oneweekslater=today+datetime.timedelta(weeks=1)
        oneweekslater=oneweekslater.strftime(str_type)
        return oneweekslater
    if input_text == 'days10later':
        oneweekslater=today+datetime.timedelta(days=10)
        oneweekslater=oneweekslater.strftime(str_type)
        return oneweekslater
    if input_text == 'twoweekslater':
        twoweekslater=today+datetime.timedelta(weeks=2)
        twoweekslater=twoweekslater.strftime(str_type)
        return twoweekslater
    if input_text == 'oneweeksago':
        oneweeksago=today-datetime.timedelta(weeks=1)
        oneweeksago=oneweeksago.strftime(str_type)
        return oneweeksago
    if input_text == 'twoweeksago':
        twoweeksago=today-datetime.timedelta(weeks=2)
        twoweeksago=twoweeksago.strftime(str_type)
        return twoweeksago
    if input_text == 'onemonthago':
        onemonthago=today-datetime.timedelta(weeks=4)
        onemonthago=onemonthago.strftime(str_type)
        return onemonthago
    if input_text == 'now':
        now=datetime.datetime.now()
        now=now.strftime('%Y.%m.%d.%H.%M')
        return now