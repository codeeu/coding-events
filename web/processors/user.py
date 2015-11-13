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


def get_ambassadors_for_countries():
    ambassadors = get_ambassadors()
    countries_ambassadors = []
    # list countries minus two CUSTOM_COUNTRY_ENTRIES
    for code, name in list(countries)[2:]:
        readable_name = unicode(name)
        country_ambassadors = [ambassador for ambassador in ambassadors if ambassador.country == code]
        # load main ambassadors
        main_ambassadors =  [ambassador for ambassador in country_ambassadors if ambassador.is_main_contact]
        # exclude main ambassadors
        supporting_ambassadors = [ambassador for ambassador in country_ambassadors if not ambassador.is_main_contact]
        countries_ambassadors.append(
            (code, readable_name, supporting_ambassadors, main_ambassadors))

    countries_ambassadors.sort()
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
