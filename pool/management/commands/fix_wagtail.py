from django.core.management.base import BaseCommand


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        from wagtail.models import Page, Site

        # Check current structure
        self.stdout.write('Current page structure:')
        for page in Page.objects.all().order_by('path'):
            self.stdout.write(
                f'  ID:{page.id} Depth:{page.depth} '
                f'Title:{page.title} Slug:{page.slug} '
                f'Type:{page.specific_class.__name__}'
            )

        # Check current sites
        self.stdout.write('\nCurrent sites:')
        for site in Site.objects.all():
            self.stdout.write(
                f'  {site.hostname}:{site.port} '
                f'Root:{site.root_page.title} '
                f'Default:{site.is_default_site}'
            )

        # Get root page
        root = Page.objects.get(depth=1)
        self.stdout.write(f'\nRoot page: {root.id} - {root.title}')

        # Check if Home exists
        home = Page.objects.filter(slug='home', depth=2).first()
        if not home:
            self.stdout.write('Creating Home page...')
            home = Page(title='Home', slug='home')
            root.add_child(instance=home)
            self.stdout.write(f'Home created with ID: {home.id}')
        else:
            self.stdout.write(f'Home already exists: {home.id}')

        # Fix or create Site
        Site.objects.all().delete()
        Site.objects.create(
            hostname='pooldrawresult.com',
            port=443,
            root_page=home,
            is_default_site=True,
            site_name='PoolDrawResult'
        )
        self.stdout.write('Site configured correctly.')

        # Move Blog under Home if it exists at wrong level
        blog = Page.objects.filter(slug='blog').first()
        if blog:
            if blog.get_parent().id != home.id:
                self.stdout.write(f'Moving Blog under Home...')
                blog.move(home, pos='last-child')
                self.stdout.write('Blog moved successfully.')
            else:
                self.stdout.write('Blog is already under Home.')
        else:
            self.stdout.write('No Blog page found - create it in Wagtail admin after this runs.')

        self.stdout.write('\nDone! Wagtail structure fixed.')