from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth import get_user_model



User = get_user_model()


class RegistrationUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Şifrə', widget=forms.PasswordInput(attrs={"placeholder": "Şifrə"}))
    password2 = forms.CharField(label='Təkrar şifrə', widget=forms.PasswordInput(attrs={"placeholder": "Təkrar şifrə"}))


    class Meta:
        model = User
        fields = ("name", "email", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super(RegistrationUserForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].required = True
        self.fields["name"].widget.attrs.update({"placeholder": "Adınızı daxil edin", "id":"form3Example1c"})
        self.fields["email"].widget.attrs.update({"placeholder": "E-poçtunuzu daxil edin", "id": "form3Example3c"})

    def clean(self):
        email = self.cleaned_data.get("email")
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")



        if not (password1 and password2 and password1 == password2):
            raise forms.ValidationError("Şifrələr uyğun deyil")

        if len(password1) < 8:
            raise forms.ValidationError("Şifrənin uzunluğu minimum 8 simvoldan ibarət olmalıdır.")

        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Bu nömrə ilə hesab mövcuddur")

        return self.cleaned_data