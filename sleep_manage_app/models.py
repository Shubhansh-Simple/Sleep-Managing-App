from django.db                  import models
from django.core.exceptions     import ValidationError
from django.utils.timezone      import now
from datetime                   import date
from datetime                   import datetime as dtt
from django.conf                import settings



class Sleep(models.Model):
    '''Collecting Your Sleep Times'''

    user_name    = models.ForeignKey( settings.AUTH_USER_MODEL , on_delete=models.CASCADE )
    
    # Date
    your_date    = models.DateField( default=now , verbose_name = 'Day' )
    
    # Last-Night
    sleep_at      = models.DateTimeField( default = dtt(2000,1,1,22,0) , help_text = 'Your last night sleep time & Forget about Dates.' , verbose_name = 'Sleep At' )
    arise_at      = models.DateTimeField( default = dtt(2000,1,1,4,0) , verbose_name = 'Wake Up At ')
    
    # Noon
    noon_sleep    = models.BooleanField( default=False )
    noon_sleep_at = models.DateTimeField( blank=True, null=True , verbose_name = 'Noon Sleeps At ' )
    noon_arise_at = models.DateTimeField( blank=True, null=True , verbose_name = 'Noon Wakeup At ' )

    class Meta:
        unique_together = ( 'user_name','your_date', )


    def date_format( self,dates ):
        '''Improves dates format'''

        return dates.strftime('%d-%b-%Y')


    def decide_noon_sleep( self ):
        '''Are you sleeping at noon.'''

        if self.noon_sleep_at and self.noon_arise_at:
            self.noon_sleep = True


    def sry_future_date( self ):
        '''You can't edit future dates'''
        
        if self.your_date > date.today():
            return True


    def common_sense( self , input_time1 , input_time2 ):
        '''Check,arise time greater than sleep time (Time Interval)'''
        
        if not input_time1 < input_time2:
            return True

    def raise_error( self , error_define ):
        raise ValidationError( error_define )


    def wakeup_noon_night( self , time_sleep , time_arise ):
        '''Noon times must lies b/w wakeup and 00:00:00'''

        start_time , end_time = self.arise_at , self.arise_at.replace(hour=23,minute=59)

        # Clean Code
        condition_one = start_time < time_sleep < end_time
        condition_two = start_time < time_arise < end_time

        if not (condition_one and condition_two) : 
            return True
    
    
    def clean( self, *args , **kwargs ):
        '''Validate individuals fields,for raising error'''

        # initialize model varaible
        self.decide_noon_sleep()

        # Validation 1
        if self.sry_future_date():
            self.raise_error( 'Can\'t edit the future dates.' )

        # Clean Code
        condition_one = self.common_sense( self.sleep_at , self.arise_at ) 
        condition_two = self.common_sense( self.noon_sleep_at , self.noon_arise_at ) if self.noon_sleep else False

        # Validation 2
        if condition_one:
            self.raise_error( 'Kindly check the time intervals.' )

        if condition_two:
            self.raise_error( 'Kindly check the noon time intervals.' )

        # Validation 3
        if self.noon_sleep:
            if self.wakeup_noon_night( self.noon_sleep_at , self.noon_arise_at ):
                self.raise_error( 'Make sure noon sleep time entered correctly.' )
        
        super( Sleep,self ).clean( *args , **kwargs )
    

    def save( self, *args , **kwargs ):
        '''Call methods before save'''

        self.full_clean()           # calling above clean() method

        super( Sleep,self ).save( *args , **kwargs )


    def __str__(self):
        return str( self.date_format( self.your_date ) ) # I want to sort the result.





















