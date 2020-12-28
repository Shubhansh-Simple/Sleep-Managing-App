from .models              import Sleep
from datetime             import date,time,timedelta
from datetime             import datetime as dtt
from django               import forms
from django.utils         import timezone as tz
from .choices             import HOUR_LIST, TIME_LIST, TIME_INTERVAL


class SleepAdminForm( forms.ModelForm ):
    
    # for re-using it inside any method :]
    date_copy = date(2000,1,1)   # default initialization

    sleep_at_hour     =  forms.ChoiceField( choices=TIME_LIST , help_text='Last Night Sleep Hours')
    sleep_at_minute   =  forms.ChoiceField( choices=HOUR_LIST )
    sleep_at_interval =  forms.ChoiceField( choices=TIME_INTERVAL )
    
    arise_at_hour     =  forms.ChoiceField( choices=TIME_LIST )
    arise_at_minute   =  forms.ChoiceField( choices=HOUR_LIST )
    arise_at_interval =  forms.ChoiceField( choices=TIME_INTERVAL )
    
    noon_sleep_at_hour     =  forms.ChoiceField( choices=TIME_LIST,     required=False )
    noon_sleep_at_minute   =  forms.ChoiceField( choices=HOUR_LIST,     required=False )
    noon_sleep_at_interval =  forms.ChoiceField( choices=TIME_INTERVAL, required=False )
    
    noon_arise_at_hour     =  forms.ChoiceField( choices=TIME_LIST,     required=False )
    noon_arise_at_minute   =  forms.ChoiceField( choices=HOUR_LIST,     required=False )
    noon_arise_at_interval =  forms.ChoiceField( choices=TIME_INTERVAL, required=False )

    class Meta:

        model   = Sleep
        exclude = ( 'noon_sleep','user_name', )
        widgets = {

            'your_date'     : forms.widgets.SelectDateWidget(),
            'sleep_at'      : forms.widgets.HiddenInput(),
            'arise_at'      : forms.widgets.HiddenInput(),
            'noon_sleep_at' : forms.widgets.HiddenInput(),
            'noon_arise_at' : forms.widgets.HiddenInput(),
        }
   

    def clean_your_date( self ):
        '''Taking dates input for re-using,through class variable.'''

        self.date_copy = self.cleaned_data.get('your_date')
        return self.date_copy


    def custom_date_modification( self , timing , dates=None ):
        '''Add "your_date" value to the model's datetime fields.'''

        if not dates:
            return dtt.combine( self.date_copy , timing )
        return dtt.combine( dates, timing )

    
    def clean_sleep_at( self ):
        '''Balance AM-PM time interval'''

        sleep_at_input          = self.cleaned_data.get( 'sleep_at' )

        # Time 12:00:00 Noon with same date.
        midnight                = self.custom_date_modification( time(12,0) , sleep_at_input.date() )

        '''(00:00:00) MORNING AM < (12:00:00) NOON PM < (23:00:00) NIGHT PM'''

        if sleep_at_input.time() > midnight.time() :
            '''Comparing only time but with same date'''
            
            sleep_at_input_date = self.date_copy - timedelta( days=1 )
            sleep_at_input      = self.custom_date_modification( sleep_at_input.time() , sleep_at_input_date  )
        else:
            sleep_at_input      = self.custom_date_modification( sleep_at_input.time() )

        return sleep_at_input


    def clean( self ):
        '''Modify dates of multiple fields at once.'''

        all_input_data = self.cleaned_data

        if 'arise_at' in all_input_data.keys():
            all_input_data['arise_at']          = self.custom_date_modification( all_input_data['arise_at'].time() )

        # Clean Code
        condition_one , condition_two = 'noon_sleep_at' in all_input_data.keys() , 'noon_arise_at' in all_input_data.keys()

        if condition_one and condition_two:
            if all_input_data['noon_sleep_at'] and all_input_data['noon_arise_at']:
                '''I want both noon-fields otherwise None'''

                all_input_data['noon_sleep_at'] = self.custom_date_modification( all_input_data['noon_sleep_at'].time() )
                all_input_data['noon_arise_at'] = self.custom_date_modification( all_input_data['noon_arise_at'].time() )

            else:
                all_input_data['noon_arise_at'] , all_input_data['noon_sleep_at'] = None , None
            
            #[ print( 'Clean Method forms.py - ',x,' ',y,' ',type(y) ) for x,y in all_input_data.items() ]
        return all_input_data















