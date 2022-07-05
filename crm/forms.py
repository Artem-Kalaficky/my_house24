from django.forms import ModelForm, modelformset_factory

from users.models import Role


class RoleForm(ModelForm):
    class Meta:
        model = Role
        exclude = ('role',)


RoleFormSet = modelformset_factory(Role, form=RoleForm, extra=0)
