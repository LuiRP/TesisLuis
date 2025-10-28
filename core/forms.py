from django import forms


class ExpandedSignUpForm(forms.Form):
    is_tutor = forms.BooleanField(required=False, label="Tutor")
    full_name = forms.CharField(
        max_length=150,
        required=True,
        label="Nombre",
        widget=forms.TextInput(attrs={"placeholder": "Nombre"}),
    )
    field_order = ["full_name", "email", "password1", "password2", "is_tutor"]

    def signup(self, request, user):
        user.full_name = self.cleaned_data["full_name"]
        user.is_tutor = self.cleaned_data["is_tutor"]
        user.save()


class TutorshipForm(forms.Form):
    name = forms.CharField(label="Nombre", max_length=254, required=True)
    description = forms.CharField(label="Descripcion", widget=forms.Textarea)


class ReviewForm(forms.Form):
    body = forms.CharField(label="Descripcion", widget=forms.Textarea)
    rating = forms.IntegerField(label="Calificación", max_value=5, min_value=0)
