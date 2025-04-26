# SESJA W FIREFOX MUSI BYĆ OTWARTA!

import browser_cookie3
import myfitnesspal

# cookies z Firefoxa 
cj = browser_cookie3.firefox(domain_name='myfitnesspal.com')
client = myfitnesspal.Client(cookiejar=cj)

import datetime
import json

today = datetime.date.today()
start = today - datetime.timedelta(days=7)
dates = [start + datetime.timedelta(days=i)
         for i in range((today - start).days + 1)]

data = []
for d in dates:
    day = client.get_date(d.year, d.month, d.day)
    day_dict = {
        'date':   d.isoformat(),
        'totals': day.totals,
        'meals':  []
    }

    for meal in day.meals:
        meal_dict = {
            'name':    meal.name,
            'entries': []
        }
        for entry in meal.entries:
            meal_dict['entries'].append({
                'food':      entry.name,
                # jeśli entry.serving_size istnieje, dorzuć ilość:
                **({'quantity': entry.serving_size} if hasattr(entry, 'serving_size') else {}),
                'totals':    entry.totals
            })
        day_dict['meals'].append(meal_dict)

    data.append(day_dict)


with open('mfp_daily_totals_and_menu.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Zapisano mfp_daily_totals_and_menu.json")