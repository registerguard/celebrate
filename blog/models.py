from __future__ import unicode_literals

from django.db import models
from django.forms import modelformset_factory
from django.shortcuts import render

from modelcluster.models import ClusterableModel

from wagtail.wagtailadmin.edit_handlers import FieldPanel, InlinePanel, StreamFieldPanel
from wagtail.wagtailcore.models import Page
from wagtail.wagtailcore.fields import RichTextField, StreamField
from wagtail.wagtailcore import blocks
from wagtail.wagtailforms.edit_handlers import FormSubmissionsPanel
from wagtail.wagtailimages.blocks import ImageChooserBlock


class BlogIndexPage(Page):
    intro = RichTextField(blank=True)

    content_panels = Page.content_panels + [
        FieldPanel('intro', classname="full"),
    ]


class BlogPage(Page):
    author = models.CharField(max_length=255)
    date = models.DateField("Post date")
    body = StreamField([
        ('heading', blocks.CharBlock(classname="full title")),
        ('paragraph', blocks.RichTextBlock()),
        ('image', ImageChooserBlock()),
    ])

    content_panels = Page.content_panels + [
        FieldPanel('author'),
        FieldPanel('date'),
        StreamFieldPanel('body'),
    ]


class RegisterGuardMemory(ClusterableModel):
    text = models.TextField()

    content_panels = [
        FieldPanel('text'),
        InlinePanel('registerguardmemoryimages', label='RG memory images'),
    ]

    def __str__(self):
        return self.text

    class Meta:
        verbose_name_plural = 'register-guard memories'


class RegisterGuardMemoryImage(models.Model):
    registerguardmemory = models.ForeignKey(RegisterGuardMemory, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='/rginfo/oper/celebrate/media/celebrate_images', blank=True)

    def __str__(self):
        return self.image.name


class SubmitMemory(Page):
    intro = RichTextField(blank=True)
    thankyou_page_title = models.CharField(
        max_length=255, help_text=u"Title text to use for the 'thank you' page"
    )
    
    # Note that there's nothing here specifying the form fields, those are
    # defined in forms.py. There's no benefit to making these editable from
    # within the Wagtail admin, since you'd need to make changes to the code
    # in order for them to work.
    
    content_panels = Page.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro', classname="full"),
        FieldPanel('thankyou_page_title'),
    ]
    
    def serve(self, request):
        # From http://stackoverflow.com/questions/34006994/how-to-upload-multiple-images-to-a-blog-post-in-django
        
        # Dropzone: http://stackoverflow.com/questions/36558502/how-to-upload-multiple-images-in-django-using-dropzone-and-saving-path-dynamical
        
        # If you want to keep attached files after failed validation:
        # https://github.com/un1t/django-file-resubmit
        from blog.forms import SubmitMemoryForm, SubmitMemoryImageForm

        ImageFormSet = modelformset_factory(RegisterGuardMemoryImage, form=SubmitMemoryImageForm, extra=3)
        
        if request.method == 'POST':
            form = SubmitMemoryForm(request.POST)
            formset = ImageFormSet(request.POST, request.FILES, queryset=RegisterGuardMemoryImage.objects.none())
            if form.is_valid() and formset.is_valid():
                memory = form.save()
                # for post_form in formset.cleaned_data:
                for post_form in formset:
                    if 'image' in post_form.cleaned_data:
                        image = post_form.cleaned_data['image']
                    else:
                        image = ''
                    photo = RegisterGuardMemoryImage(registerguardmemory=memory, image=image)
                    photo.save()
                return render(request, 'blog/thankyou.html', {
                    'page': self,
                    'memory': memory,
                })
        else:
            form = SubmitMemoryForm()
            formset = ImageFormSet(queryset=RegisterGuardMemoryImage.objects.none())
        
        return render(request, 'blog/submitmemory.html', {
            'page': self,
            'form': form,
            'formset': formset,
        })
