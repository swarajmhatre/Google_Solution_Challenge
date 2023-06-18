from django import forms

from .models import Adoption, lostandfound

class AdoptionForm(forms.ModelForm):
    class Meta:
        model = Adoption
        fields = "__all__"
class LAFform(forms.ModelForm):
    class Meta:
        model = lostandfound
        fields = "__all__"