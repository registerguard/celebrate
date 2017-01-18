from django import forms
from django.template.defaultfilters import filesizeformat
from django.utils.translation import ugettext_lazy as _

from blog.models import RegisterGuardMemory, RegisterGuardMemoryImage
from captcha.fields import ReCaptchaField


class SubmitMemoryForm(forms.ModelForm):
    captcha = ReCaptchaField()

    class Meta:
        model = RegisterGuardMemory
        fields = ['text', 'captcha',]


class SubmitMemoryImageForm(forms.ModelForm):

    class Meta:
        model = RegisterGuardMemoryImage
        fields = ['image',]

    # 2.5MB - 2621440
    # 5MB - 5242880
    # 10MB - 10485760
    # 20MB - 20971520
    # 50MB - 5242880
    # 100MB 104857600
    # 250MB - 214958080
    # 500MB - 429916160
    MAX_UPLOAD_SIZE = 5242880 #5MB

    def clean_image(self):
        image = self.cleaned_data['image']
        content_type = image.content_type.split('/')[0]
        if content_type == 'image':
            if image._size > self.MAX_UPLOAD_SIZE:
                raise forms.ValidationError(
                    _('File must be less than %s. Current filesize is %s.') %
                    (
                        filesizeformat(self.MAX_UPLOAD_SIZE),
                        filesizeformat(image._size)
                    )
                )
        else:
            raise forms.ValidationError(_('File type not supported.'))
        return image
