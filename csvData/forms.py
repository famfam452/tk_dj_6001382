from django import forms
class Nameform(forms.Form):
    your_name = forms.CharField(label='',widget=forms.TextInput(
        attrs={
            'class':'form-control',
            'placeholder':"Name",
            'name':"your_name",
            'id':"your_name",
        }
    ))

class FileCSVform(forms.Form):
    CSV_file = forms.FileField(label='',widget=forms.ClearableFileInput(
        attrs={
            'class':"custom-file-input",
            'id':"inputGroupFile01",
            'accept':".csv",
        }
    ))