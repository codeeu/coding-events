from django.conf import settings
from hashlib import sha1
from os import system
from os import unlink
from os.path import dirname
from os.path import realpath

def certificate_name_for(event_id):
    obfuscated_part = sha1(settings.SECRET_KEY + str(event_id)).hexdigest()

    return str(event_id) + '-' + obfuscated_part + '.pdf'

def generate_certificate_for(event_id, name_of_certificate_holder):
    resources_path             = dirname(realpath(__file__)) + '/resources/'
    static_files_path          = dirname(dirname(realpath(__file__))) + '/static/certificates/'

    generic_template_path      = resources_path + 'template.tex'
    personalized_template_path = resources_path + str(event_id) + '.tex'
    resulting_certificate_path = static_files_path + certificate_name_for(event_id)

    with open(generic_template_path) as template:
        personalized_certificate_content = template.read().replace(
            '<CERTIFICATE_HOLDER_NAME>', name_of_certificate_holder)

    with open(personalized_template_path, 'w') as personalized_template:
        personalized_template.write(personalized_certificate_content)

    commands = [
        'cd ' + resources_path,
        'pdflatex -interaction=nonstopmode -output-directory ' + resources_path + ' ' + personalized_template_path,
        'mv -f ' + personalized_template_path.replace('.tex', '.pdf') + ' ' + resulting_certificate_path,
        'rm -rf ' + resources_path + str(event_id) + '.*',
    ]

    if system(' && '.join(commands)) != 0:
        return False

    return resulting_certificate_path
