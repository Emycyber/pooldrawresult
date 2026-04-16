from wagtail import hooks
from wagtail.admin import messages
from django.shortcuts import redirect


@hooks.register('before_delete_page')
def before_delete_page(request, page):
    from blog.models import BlogIndexPage, BlogPage

    # Only block deletion of Blog index page
    if isinstance(page, BlogIndexPage):
        messages.error(
            request,
            'Cannot delete the Blog index page. Unpublish it instead.'
        )
        return redirect('wagtailadmin_explore', page.get_parent().id)

    # For BlogPage — just clear related objects and let Wagtail handle the rest
    if isinstance(page, BlogPage):
        try:
            page.tagged_items.all().delete()
            page.categories.clear()
        except Exception:
            pass
        # Return None so Wagtail continues with normal deletion
        return None