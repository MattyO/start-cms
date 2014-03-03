from cms.models import Page
def nav():
    return { 'pages': Page.objects.filter(active=True) }
