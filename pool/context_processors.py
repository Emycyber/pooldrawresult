from .models import FooterLink

def footer_links(request):
    return {
        'footer_links': FooterLink.objects.filter(is_active=True),
    }