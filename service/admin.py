from django.contrib import admin
from service.models import GlobalContactDump, User, UserRelationship
from django import forms

@admin.register(GlobalContactDump)
class QuestionDisplay(admin.ModelAdmin):
    list_display = ('name','phone_number','email','registered')


class UserRelationshipInlineForm(forms.ModelForm):
    class Meta:
        model = UserRelationship
        fields = '__all__'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['to_user'].queryset = User.objects.all().order_by('id', 'name', 'phone_number')

class UserRelationshipInline(admin.TabularInline):
    model = UserRelationship
    form = UserRelationshipInlineForm
    fk_name = 'from_user'
    extra = 1

class UserAdmin(admin.ModelAdmin):
    inlines = [UserRelationshipInline]
    ordering = ('id',)
    search_fields = ('name', 'phone_number')



admin.site.register(User, UserAdmin)