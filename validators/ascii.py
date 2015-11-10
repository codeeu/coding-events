from django.core.validators import ValidationError

def is_ascii(text):
    try:
        text.encode('ascii')
    except UnicodeEncodeError:
        return False
    else:
        return True

def validate_ascii_text(text):
    "Check if text is a text with ASCII-only characters."

    if not is_ascii(text):
        raise ValidationError(
            'Please use only ASCII (Latin) letters.',
            code='invalid',
            params={'text': text},
        )
