from django import forms
from django.forms import widgets
from django.conf import settings


class UniversalUploaderWidget(widgets.ClearableFileInput):
    template_name = 'admin/widgets/universal_uploader_widget.html'

    def __init__(self, attrs=None):
        super(UniversalUploaderWidget, self).__init__(attrs=attrs)

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        return forms.Media(
            js=(
                'admin/js/universal-uploader-widget%s.js' % extra,
            ),
            css={
                'screen': (
                    'admin/css/universal-uploader-widget%s.css' % extra,
                ),
            },
        )


class ImageUploaderWidget(UniversalUploaderWidget):
    def get_context(self, name, value, attrs):
        context = super(ImageUploaderWidget, self).get_context(
            name, value, attrs)
        context['widget'].update({
            'file_type': 'image',
            'input_accept': '.jpg,.jpeg,.png'
        })
        return context


class AudioUploaderWidget(UniversalUploaderWidget):
    def get_context(self, name, value, attrs):
        context = super(AudioUploaderWidget, self).get_context(
            name, value, attrs)
        context['widget'].update({
            'file_type': 'audio',
            'input_accept': '.mp3'
        })
        return context


class VideoUploaderWidget(UniversalUploaderWidget):
    def get_context(self, name, value, attrs):
        context = super(VideoUploaderWidget, self).get_context(
            name, value, attrs)
        context['widget'].update({
            'file_type': 'video',
            'input_accept': '.mp4'
        })
        return context


class PdfUploaderWidget(UniversalUploaderWidget):
    def get_context(self, name, value, attrs):
        context = super(PdfUploaderWidget, self).get_context(
            name, value, attrs)
        context['widget'].update({
            'file_type': 'pdf',
            'input_accept': '.pdf'
        })
        return context

    @property
    def media(self):
        extra = '' if settings.DEBUG else '.min'
        return forms.Media(
            js=('admin/vendor/pdf.worker.min.js',
                'admin/js/universal-uploader-widget%s.js' % extra,
                ),
            css={
                'screen': (
                    'admin/css/universal-uploader-widget%s.css' % extra,
                ),
            },
        )
