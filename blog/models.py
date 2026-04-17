from django.db import models
from wagtail.models import Page
from wagtail.fields import StreamField
from wagtail import blocks
from wagtail.admin.panels import FieldPanel
from wagtail.images.blocks import ImageChooserBlock
from wagtail.images.models import Image
from django.utils import timezone
from wagtail.snippets.models import register_snippet
from taggit.models import TaggedItemBase
from modelcluster.fields import ParentalKey, ParentalManyToManyField
from modelcluster.contrib.taggit import ClusterTaggableManager


@register_snippet
class BlogCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class BlogPageTag(TaggedItemBase):
    content_object = ParentalKey(
        'BlogPage',
        related_name='tagged_items',
        on_delete=models.CASCADE
    )


class BlogIndexPage(Page):
    """The parent listing page for all blog posts."""

    subpage_types = ['blog.BlogPage']  # ← only BlogPage can be created under this
    # max_count = 1                      # ← only ONE BlogIndexPage can ever exist site-wide
    template = "blog/blog_index_page.html"

    content_panels = Page.content_panels

    def get_context(self, request):
        context = super().get_context(request)
        context['blog_pages'] = BlogPage.objects.live().order_by('-date')
        return context


class BlogPage(Page):
    date = models.DateField("Post date", default=timezone.now)
    intro = models.CharField(max_length=250, blank=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content = StreamField([
        ('heading', blocks.CharBlock()),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ], use_json_field=True)

    categories = ParentalManyToManyField('blog.BlogCategory', blank=True)
    tags = ClusterTaggableManager(through=BlogPageTag, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('date'),
        FieldPanel('banner_image'),
        FieldPanel('intro'),
        FieldPanel('categories'),
        FieldPanel('tags'),
        FieldPanel('content'),
    ]

    promote_panels = Page.promote_panels

    parent_page_types = ['blog.BlogIndexPage']  # ← can only live under BlogIndexPage
    subpage_types = []                           # ← nothing can be created under a blog post
    template = "blog/blog_page.html"