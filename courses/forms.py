from django import forms
from .models import  Course, Video, Lecture



class LectureAdminForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = [
            'order',
            'title',
            'video',
            'description',
            'slug',
        ]

    def __init__(self,*args,**kwargs):
        super(LectureAdminForm, self).__init__(*args,**kwargs)
        obj = kwargs.get('instance')
        qs = Video.objects.filter(lecture__isnull=True)
        if obj:
            if obj.video:
                this_ = Video.objects.filter(pk=obj.video.pk)
                qs = (qs | this_)
            self.fields['video'].queryset = qs
        else:
            self.fields['video'].queryset = qs





class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = [
            'title',
            'description',
            'slug',
            'price',
        ]


    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        qs = Course.objects.filter(slug=slug)
        if qs.count() > 1:
            raise forms.ValidationError("Slug must be unique")
        return slug