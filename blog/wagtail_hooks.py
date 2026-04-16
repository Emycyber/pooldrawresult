from wagtail import hooks
from wagtail.admin import messages
from django.utils.html import format_html


@hooks.register('before_delete_page')
def before_delete_page(request, page):
    from blog.models import BlogIndexPage
    if isinstance(page, BlogIndexPage):
        messages.error(
            request,
            format_html(
                '<b>Cannot delete the Blog index page.</b> '
                'Unpublish it instead if you want to hide it.'
            )
        )
        from django.shortcuts import redirect
        return redirect('wagtailadmin_explore', page.get_parent().id)