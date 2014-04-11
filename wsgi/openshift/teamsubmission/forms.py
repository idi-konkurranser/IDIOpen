from django import forms
from .models import Submission
from django.template.defaultfilters import filesizeformat
from django.core.exceptions import ValidationError
from execution.models import FileExtension, Resource
from execution.models import CompilerProfile

# 2.5MB - 2621440
# 5MB - 5242880
# 10MB - 10485760
# 20MB - 20971520
# 50MB - 5242880
# 100MB 104857600
# 250MB - 214958080
# 500MB - 429916160
#MAX_UPLOAD_SIZE = "5242880" # 5 MB

# Maybe not the best way, could get file extension for each compiler profile connected to a specific problem
def get_file_extensions():
    return FileExtension.objects.all()

def get_max_file_size(problem, cProfile):
    resource = Resource.objects.filter(problem=problem).filter(cProfile=cProfile)
    if resource:
        return resource[0].max_filesize
    else:
        return 0
    
class SubmissionForm(forms.ModelForm):
    compilerProfile = forms.ModelChoiceField(CompilerProfile.objects.all())
    
    class Meta:
        model = Submission  
        fields = ['submission']
        
    def clean(self):
        submission = self.cleaned_data.get('submission')
        cProfile = self.cleaned_data.get('compilerProfile')
        
        if not submission:
            self._errors['submission'] = self.error_class([("Please upload a file before submitting")])
            raise ValidationError('')
        # The file extension for the given submission
        content_type = submission.name.split('.')[-1]
        FILE_EXT = get_file_extensions()
        MAX_FILESIZE = get_max_file_size(self.instance.problem, cProfile) * 1024
        if (MAX_FILESIZE == 0):
            self._errors['compilerProfile'] = self.error_class([('Please contact support')])
            return self.cleaned_data
        # Check if submission has an allowed file extension
        if content_type in [str(x) for x in FILE_EXT]:
            if submission._size > MAX_FILESIZE:
                self._errors['submission'] = self.error_class([('Please keep filesize under %s. Current filesize %s') % (filesizeformat(MAX_FILESIZE), filesizeformat(submission._size))])
        else:
            self._errors['submission'] = self.error_class([('File type is not supported')])
        return self.cleaned_data
    
    def save(self):
        new_sub = Submission()
        new_sub.submission = self.cleaned_data.get('submission')
        new_sub.problem = self.instance.problem
        new_sub.validate = False
        new_sub.team = self.instance.team
        new_sub.save()

# EOF