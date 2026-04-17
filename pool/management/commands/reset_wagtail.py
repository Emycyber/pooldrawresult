from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        from wagtail.models import Page, Site, PageLogEntry
        from wagtail.images.models import Image, Rendition

        self.stdout.write('Starting Wagtail reset...')

        try:
            PageLogEntry.objects.all().delete()
            self.stdout.write('Cleared page log entries')
        except Exception as e:
            self.stdout.write(f'Log entries: {e}')

        try:
            Rendition.objects.all().delete()
            self.stdout.write('Cleared renditions')
        except Exception as e:
            self.stdout.write(f'Renditions: {e}')

        try:
            Image.objects.all().delete()
            self.stdout.write('Cleared images')
        except Exception as e:
            self.stdout.write(f'Images: {e}')

        try:
            Site.objects.all().delete()
            self.stdout.write('Cleared sites')
        except Exception as e:
            self.stdout.write(f'Sites: {e}')

        try:
            Page.objects.filter(depth__gt=1).delete()
            self.stdout.write('Cleared all pages except root')
        except Exception as e:
            self.stdout.write(f'Pages: {e}')

        # Get root
        root = Page.objects.get(depth=1)
        self.stdout.write(f'Root page exists: {root.id}')

        # Create Home page under root
        home = Page(title='Home', slug='home')
        root.add_child(instance=home)
        self.stdout.write(f'Home page created: {home.id}')

        # Create Site pointing to Home
        Site.objects.create(
            hostname='pooldrawresult.com',
            port=443,
            root_page=home,
            is_default_site=True,
            site_name='PoolDrawResult'
        )
        self.stdout.write('Site created pointing to Home')
        self.stdout.write('Reset complete! Now create Blog Index Page under Home in Wagtail admin.')