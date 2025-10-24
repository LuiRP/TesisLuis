from django import forms


class ExpandedSignUpForm(forms.Form):
    is_tutor = forms.BooleanField(required=False)
    first_name = forms.CharField(
        max_length=150, 
        required=True,
        label=('Nombre'),
        widget=forms.TextInput(attrs={'placeholder': 'Nombre'})
    )
    
    last_name = forms.CharField(
        max_length=150, 
        required=True,
        label=('Apellido'),
        widget=forms.TextInput(attrs={'placeholder': 'Apellido'})
    )

    def signup(self, request, user):
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.is_tutor = self.cleaned_data['is_tutor']
        user.save()