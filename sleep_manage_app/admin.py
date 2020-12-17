from django.contrib import admin
from . import models,forms


class SleepAdmin( admin.ModelAdmin ):
    
    form         = forms.SleepAdminForm
    list_display = ( '__str__', 'noon_sleep' ) #,'sleep_at','arise_at')
    ordering     = ('your_date',)              # as per field order

    def get_queryset( self,request ):
        '''User can see his own data only'''

        query = super( SleepAdmin , self ).get_queryset( request )
        if request.user.is_superuser:
            self.list_display = ( '__str__','user_name' )
            return query
        return query.filter( user_name=request.user )  # Only owner's Data if not superuser

    def save_model( self, request, obj, form, change):
        obj.user_name = request.user
        super().save_model( request, obj, form, change )

admin.site.register( models.Sleep , SleepAdmin )

