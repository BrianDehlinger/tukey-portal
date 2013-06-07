from django import forms

class MyCheckboxSelectMultiple(forms.CheckboxSelectMultiple):
    def render(self, name, value, attrs=None, choices=()):
        html = super(MyCheckboxSelectMultiple, self).render(name, value, attrs, choices)
        return mark_safe(html.replace('<ul>', '<ul class="foobar">'))


class OSDCForm(forms.Form):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class' : 'span4'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class' : 'span4'}))
    organization = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class' : 'span4'}))
    webpage = forms.CharField(max_length=200,required=False,widget=forms.TextInput(attrs={'class' : 'span4'}))
    phonenumber = forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class' : 'span4'}))
    address = forms.CharField(required=False,widget=forms.Textarea(attrs={'class' : 'span4', 'rows' : '4'}))
    projectname = forms.CharField(widget=forms.TextInput(attrs={'class' : 'span4'}))
    projectlead = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class' : 'span4'}))
    projectlead_email = forms.EmailField(widget=forms.TextInput(attrs={'class' : 'span4'}))
    projectdescr = forms.CharField(widget=forms.Textarea(attrs={'class' : 'span5'}))
    #othercontacts = forms.CharField(required=False)
    resources = forms.CharField(widget=forms.Textarea(attrs={'class' : 'span5'}))
    pubkey = forms.FileField(widget=forms.ClearableFileInput(attrs={'class' : 'span4'}))

SYSTEM_CHOICES = (('occ-y', 'OCC-Y (A Hadoop-based data cloud)'), 
                  ('bionimbus_cc', 'Bionimbus Community Cloud (A community cloud for genomics data)'), 
                  ('bionimbus_uchicago', 'UChicago Bionimbus Cloud (A private cloud for genomics data)'),
                  ('matsu', 'Matsu Testbed (A cloud testbed for earth science data)'))

class OSDCInviteForm(forms.Form):
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class' : 'span4'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class' : 'span4'}))
    organization = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class' : 'span4'}))
    systems = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=SYSTEM_CHOICES)
    
    webpage = forms.CharField(max_length=200,required=False,widget=forms.TextInput(attrs={'class' : 'span4'}))
    phonenumber = forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class' : 'span4'}))
    address = forms.CharField(required=False,widget=forms.Textarea(attrs={'class' : 'span4', 'rows' : '4'}))
    projectname = forms.CharField(widget=forms.TextInput(attrs={'class' : 'span4'}))
    projectlead = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class' : 'span4'}))
    projectlead_email = forms.EmailField(widget=forms.TextInput(attrs={'class' : 'span4'}))
    projectdescr = forms.CharField(widget=forms.Textarea(attrs={'class' : 'span5'}))
    resources = forms.CharField(widget=forms.Textarea(attrs={'class' : 'span5'}))
    pubkey = forms.FileField(widget=forms.ClearableFileInput(attrs={'class' : 'span4'}))

class OSDCSupportForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea(attrs={'class' : 'span5'}))
    sender = forms.EmailField()

class PDCForm(forms.Form):
    eracommons = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class' : 'span4'}))
    name = forms.CharField(max_length=200, widget=forms.TextInput(attrs={'class' : 'span4'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'class' : 'span4'}))
    organization = forms.CharField(max_length=200,widget=forms.TextInput(attrs={'class' : 'span4'}))
    systems = forms.MultipleChoiceField(required=False, widget=forms.CheckboxSelectMultiple, choices=SYSTEM_CHOICES)
    
    webpage = forms.CharField(max_length=200,required=False,widget=forms.TextInput(attrs={'class' : 'span4'}))
    phonenumber = forms.CharField(max_length=100,required=False,widget=forms.TextInput(attrs={'class' : 'span4'}))
    address = forms.CharField(required=False,widget=forms.Textarea(attrs={'class' : 'span4', 'rows' : '4'}))
    projectdescr = forms.CharField(widget=forms.Textarea(attrs={'class' : 'span5'}))
    resources = forms.CharField(widget=forms.Textarea(attrs={'class' : 'span5'}))

