from django.shortcuts import render
from django.shortcuts import get_object_or_404, redirect
from .models import BlogPage, BlogComment

def add_comment(request, page_id):
    if request.method == 'POST':
        page = get_object_or_404(BlogPage, id=page_id)
        BlogComment.objects.create(
            page=page,
            name=request.POST.get('name', '').strip(),
            email=request.POST.get('email', '').strip(),
            body=request.POST.get('body', '').strip(),
            is_approved=False
        )
    return redirect(page.url)