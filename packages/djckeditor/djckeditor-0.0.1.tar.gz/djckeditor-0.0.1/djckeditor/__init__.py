
def setup_settings(settings, is_prod, **kwargs):

    settings['CKEDITOR_UPLOAD_PATH'] = 'uploads/'

    settings['INSTALLED_APPS'] = [
        app for app in [
            'ckeditor',
            'ckeditor_uploader'
        ] if app not in settings['INSTALLED_APPS']
    ] + settings['INSTALLED_APPS']
