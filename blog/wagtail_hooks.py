from wagtail import hooks
from wagtail.admin import messages
from django.shortcuts import redirect


@hooks.register('before_delete_page')
def before_delete_page(request, page):
    from blog.models import BlogIndexPage, BlogPage

    # Block deletion of Blog index page
    if isinstance(page, BlogIndexPage):
        messages.error(
            request,
            'Cannot delete the Blog index page. Unpublish it instead if you want to hide it.'
        )
        return redirect('wagtailadmin_explore', page.get_parent().id)

    # For blog posts clear related objects before deletion
    if isinstance(page, BlogPage):
        try:
            page.tagged_items.all().delete()
            page.categories.clear()
        except Exception:
            pass