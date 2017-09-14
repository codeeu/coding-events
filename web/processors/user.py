from django.contrib.auth.models import User
from django_countries import countries


def get_user(user_id):
    user = User.objects.get(id=user_id)
    return user


def get_user_profile(user_id):
    user = User.objects.get(id=user_id)
    return user.profile


def get_ambassadors(country_code=None):
    ambassadors = User.objects \
        .filter(groups__name='ambassadors') \
        .prefetch_related('userprofile') \
        .order_by('date_joined')

    if country_code != None:
        ambassadors = ambassadors.filter(userprofile__country=country_code)

    ambassador_profiles = list({ambassador.profile for ambassador in ambassadors})

    return ambassador_profiles


facebook_links = {
    "Austria": "https://www.facebook.com/CodeWeek-Austria-151277175428538/",
    "Belgium": "https://www.facebook.com/eucodeweekbelgium/",
    "Bulgaria": "https://www.facebook.com/EU-Code-Week-Bulgaria-699640040127398/",
    "Croatia": "https://www.facebook.com/CodeWeekHr/",
    "Cyprus": "https://www.facebook.com/profile.php?id=572555376146147&ref=br_rs",
    "Czech Republic": "https://www.facebook.com/codeweekcz/",
    "Finland": "https://www.facebook.com/codeweekfinland/?ref=br_rs",
    "France": "https://www.facebook.com/CodeWeekFrance/?ref=br_rs",
    "Germany": "https://www.facebook.com/codeweekgermany/?ref=br_rs",
    "Greece": "https://www.facebook.com/codeEUGreece/?ref=br_rs",
    "Hungary": "https://www.facebook.com/codeweekHU/?ref=br_rs",
    "Iceland": "https://www.facebook.com/CodeWeekIS/?ref=br_rs",
    "Isle of Man": "https://www.facebook.com/EU-Code-Week-Isle-of-Man-120990338533752/",
    "Italy": "https://www.facebook.com/CodeWeekIT",
    "Malta": "https://www.facebook.com/CodeEUMalta/",
    "Moldova (the Republic of)": "https://www.facebook.com/codeweekMD/?ref=br_rs",
    "Poland": "https://www.facebook.com/CodeWeekPL/?ref=br_rs",
    "Portugal": "https://www.facebook.com/codeweekPT/?ref=br_rs",
    "Romania": "https://www.facebook.com/EUCodeWeekRomania/?ref=br_rs",
    "Russian Federation": "https://www.facebook.com/%D0%9B%D0%B0%D0%B1%D0%BE%D1%80%D0%B0%D1%82%D0%BE%D1%80%D0%B8%D1%8F-%D0%BA%D1%80%D0%B5%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D0%BE%D0%B3%D0%BE-%D0%BF%D1%80%D0%BE%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B8%D1%80%D0%BE%D0%B2%D0%B0%D0%BD%D0%B8%D1%8F-922907817827144/?ref=bookmarks",
    "Serbia": "https://www.facebook.com/CodeWeekSerbia/?ref=br_rs",
    "Slovenia": "https://www.facebook.com/codeweek.si",
    "Sweden": "https://www.facebook.com/codeweeksweden/?ref=br_rs",
    "Switzerland": "https://www.facebook.com/codeweekswitzerland/?ref=br_rs",
    "Turkey": "https://www.facebook.com/groups/1448094125469237/",
    "Ukraine": "https://www.facebook.com/groups/1179293055426737/",
    "United Kingdom": "https://www.facebook.com/Codeweekuk-475492319315384/"
}

def facebook(country):
    return facebook_links.get(country,"")


def get_ambassadors_for_countries():
    ambassadors = get_ambassadors()
    countries_ambassadors = []
    # list countries minus two CUSTOM_COUNTRY_ENTRIES
    for code, name in list(countries)[2:]:
        readable_name = unicode(name)
        country_ambassadors = [ambassador for ambassador in ambassadors if ambassador.country == code]
        # load main ambassadors
        main_ambassadors = [ambassador for ambassador in country_ambassadors if ambassador.is_main_contact]
        # exclude main ambassadors
        supporting_ambassadors = [ambassador for ambassador in country_ambassadors if not ambassador.is_main_contact]
        countries_ambassadors.append(
            (code, readable_name, supporting_ambassadors, main_ambassadors, facebook(readable_name)))

    countries_ambassadors.sort(key=lambda country: country[1], reverse=False)

    return countries_ambassadors


def get_ambassadors_for_country(country):
    ambassadors = User.objects.filter(
        groups__name='ambassadors',
        userprofile__country=country)
    return ambassadors


def update_user_email(user_id, new_email):
    user = User.objects.get(id=user_id)
    user.email = new_email
    user.save(update_fields=["email"])
    return user
