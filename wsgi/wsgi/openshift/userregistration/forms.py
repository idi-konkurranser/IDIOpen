'''
Created on Feb 26, 2014

@author: filip
'''
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.core.exceptions import ValidationError;
from django import forms
from django.forms.util import ErrorList 
from userregistration.models import CustomUser
from django.utils.translation import ugettext_lazy as _
from contest.models import Invite 
from django.views.decorators.debug import sensitive_variables

import ipdb;

try:
    from django.contrib.auth import get_user_model
    User = get_user_model()
except ImportError:
    from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email","first_name","last_name")
        
class CustomStaffUserCreationForm(UserCreationForm):
    """
    A form that creates a user, with no privileges, from the given email and
    password.
    """

    def __init__(self, *args, **kargs):
        super(CustomStaffUserCreationForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        fields = ("email","first_name","last_name", "is_staff", "is_superuser")

class CustomUserChangeForm(UserChangeForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    password hash display field.
    """

    def __init__(self, *args, **kargs):
        super(CustomUserChangeForm, self).__init__(*args, **kargs)
        del self.fields['username']

    class Meta:
        model = CustomUser
        
        
class RegistrationForm(forms.Form):
    """
    Form for registering a new user account.
    
    Validates that the requested username is not already in use, and
    requires the password to be entered twice to catch typos.
    
    Subclasses should feel free to add any additional validation they
    need, but should avoid defining a ``save()`` method -- the actual
    saving of collected user data is delegated to the active
    registration backend.

    """
    required_css_class = 'required'
    
    email = forms.EmailField(label=_("E-mail"))
    first_name = forms.CharField(label=_("First Name"))
    last_name = forms.CharField(label=_("Last Name"))
    password1 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password"))
    password2 = forms.CharField(widget=forms.PasswordInput,
                                label=_("Password (again)"))
    
    def clean_email(self):
        """
        Validate that the username is alphanumeric and is not already
        in use.
        
        """
        existing = User.objects.filter(email__iexact=self.cleaned_data['email'])
        if existing.exists():
            raise forms.ValidationError(_("A user with that email already exists."))
        else:
            return self.cleaned_data['email']

    def clean(self):
        """
        Verifiy that the values entered into the two password fields
        match. Note that an error here will end up in
        ``non_field_errors()`` because it doesn't apply to a single
        field.
        
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                ipdb.set_trace()
                raise forms.ValidationError(_("The two password fields didn't match."))
        return self.cleaned_data
    
class Invites_Form(forms.Form):
    def clean(self):
        if 'id' in self.cleaned_data and 'submit' in self.cleaned_data:
            if self.cleaned_data['id'].isdigit():
                if self.cleaned_data['submit'] == 'accept':
                    self.cleaned_data['submit'] = True
                elif self.cleaned_data['submit'] == 'decline':
                    self.cleaned_data['submit'] = False
                
                return self.cleaned_data
        
        raise forms.ValidationError(_("The form did not validate"))
    
class PasswordForm(forms.ModelForm):
    password_validation = forms.CharField(widget=forms.PasswordInput(),
                                          label="Password (confirm)");
    
    def __init__(self, *args, **kwargs):
        super(PasswordForm, self).__init__(*args, **kwargs);
        self.fields.keyOrder = ['password', 'password_validation'];
        self.contextName = "userpw";
    
    @sensitive_variables('password', 'password_validation')
    def clean(self):
        if  'password'            in self.cleaned_data \
        and 'password_validation' in self.cleaned_data:
            pw = self.cleaned_data['password'];
            pw_validation = self.cleaned_data['password_validation'];
            
            if pw != pw_validation:
                    self.errors['password'] = ErrorList();
                    self.errors['password_validation'] = ErrorList();
                    self.errors['password'].append("%s do not match" % ("Passwords"));
                    self.errors['password_validation'].append("%s do not match" % ("Passwords"));
            else:
                super(PasswordForm, self).clean();
                return self.cleaned_data;

        raise ValidationError("Fields cannot be empty")

    def save(self):
        self.instance.set_password(self.cleaned_data['password']);
        super(PasswordForm, self).save();
                                          
    class Meta:
        model = CustomUser;
        fields = ['password'];
        help_texts = {
                      'password_validation': "Enter password again for validation",
                      };
        widgets = {
                   'password' : forms.PasswordInput()
            };


class EmailForm(forms.ModelForm):
    email_validation = forms.EmailField()

    def __init__(self, *args, **kwargs):
        super(EmailForm, self).__init__(*args, **kwargs);
        self.contextName = "useremail";
    
    def save(self):
        """self.instance.set_password(self.cleaned_data['password']);"""
        """super(ContestantForm, self).save();"""
        self.instance.add_new_email(email_validation)
        
    class Meta:
        model = CustomUser;
        fields =['email'];
                
class PIForm(forms.ModelForm):
    def save(self):
        pass

    def __init__(self, *args, **kwargs):
        super(PIForm, self).__init__(*args, **kwargs);
        self.contextName = "userpi";
    
    class Meta:
        model   = CustomUser
        fields  = ['first_name', 'last_name']
        help_text = {
                     'first_name': "First name",
                     'last_name':"Last name",
                     } 
                
# EOF