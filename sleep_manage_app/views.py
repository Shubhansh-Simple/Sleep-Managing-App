from django.http          import HttpResponse
from django.views.generic import ListView , DetailView , CreateView , UpdateView
from .models              import Sleep
from .forms               import SleepAdminForm
from datetime             import datetime as dtt


'''
I have to write a custom class which helps 
in DRY principle in create-update views.
'''

class TimeFormatManager():
    '''
    Self Help Class for DRY principle
    Purpose - Convert forms input then 
    returns valid 12hrs time format
    '''

    def am_pm_converter( self , datetime_input ):
        '''Return valid datetime format as str object.'''

        return str( dtt.strptime( datetime_input,'%Y-%m-%d %I:%M %p') )

    
    def adding_date( self , data ):
        '''Adding dates with the time for datetime conversion.'''
        
        if data:
            return self.am_pm_converter( '2001-01-01 ' + data )

    
    def make_time( self , hour , minute , interval ):
        '''Returns a valid time pattern.'''

        if hour and minute and interval:
            ready_time =  hour + ':' + minute + ' ' + interval 
                 
            return self.adding_date( ready_time )
        else:
            return None


class SleepCreateView( CreateView,TimeFormatManager ):
    model         = Sleep
    template_name = 'sleep_new.html'
    form_class    = SleepAdminForm

   
    def post( self,request,*args,**kwargs ):
        '''Modifying the input data before validation.'''

        FORM = request.POST.copy()
        
        FORM['sleep_at']      = self.make_time( FORM['sleep_at_hour'],      FORM['sleep_at_minute'],      FORM['sleep_at_interval'] ) 
        FORM['arise_at']      = self.make_time( FORM['arise_at_hour'],      FORM['arise_at_minute'],      FORM['arise_at_interval'] ) 
        FORM['noon_arise_at'] = self.make_time( FORM['noon_arise_at_hour'], FORM['noon_arise_at_minute'], FORM['noon_arise_at_interval'] ) 
        FORM['noon_sleep_at'] = self.make_time( FORM['noon_sleep_at_hour'], FORM['noon_sleep_at_minute'], FORM['noon_sleep_at_interval'] ) 

        form = self.form_class( FORM )

        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def form_valid( self,form ):

        form_unsave           = form.save( commit=False )
        form_unsave.user_name = self.request.user

        return super( SleepCreateView,self ).form_valid( form )


    def form_invalid( self,form ):
        print( 'form_invalid error name - ',form.errors.as_json() )
        
        error = form.errors.as_ul()
        return HttpResponse('<h1>{}</h1>'.format(error) )


class SleepDetailView( DetailView ):
    model               = Sleep
    template_name       = 'sleep_detail.html'
    context_object_name = 'sleep_detail'


class SleepListView( ListView ):
    model               = Sleep
    template_name       = 'sleep_list.html'
    context_object_name = 'sleep_list'


class SleepUpdateView( UpdateView,TimeFormatManager ):
    model         = Sleep
    template_name = 'sleep_edit.html'
    form_class    = SleepAdminForm

    
    def get_object( self ):
        '''Modify readed model field data with localtime.'''

        obj = super( SleepUpdateView,self ).get_object()
        obj.sleep_at      = obj.sleep_at_local
        obj.arise_at      = obj.arise_at_local
        obj.noon_sleep_at = obj.noon_sleep_at_local
        obj.noon_arise_at = obj.noon_arise_at_local
        return obj


    def get_context_data( self,**kwargs ):
        '''Insert into custom-form by breaking the models data'''

        context = super( SleepUpdateView , self ).get_context_data( **kwargs )
        self.object = self.get_object()

        # Modify initial form.
       
        context['form'].fields['sleep_at_hour'].initial          = self.object.sleep_at.strftime('%-I')
        context['form'].fields['sleep_at_minute'].initial        = self.object.sleep_at.minute
        context['form'].fields['sleep_at_interval'].initial      = self.object.sleep_at.strftime('%p')

        context['form'].fields['arise_at_hour'].initial          = self.object.arise_at.strftime('%-I')
        context['form'].fields['arise_at_minute'].initial        = self.object.arise_at.minute
        context['form'].fields['arise_at_interval'].initial      = self.object.arise_at.strftime('%p')
 
        context['form'].fields['noon_sleep_at_hour'].initial     = str( self.object.noon_sleep_at.hour )
        context['form'].fields['noon_sleep_at_minute'].initial   = self.object.noon_sleep_at.minute
        context['form'].fields['noon_sleep_at_interval'].initial = self.object.noon_sleep_at.strftime('%p')
        
        context['form'].fields['noon_arise_at_hour'].initial     = str( self.object.noon_arise_at.hour )
        context['form'].fields['noon_arise_at_minute'].initial   = self.object.noon_arise_at.minute
        context['form'].fields['noon_arise_at_interval'].initial = self.object.noon_arise_at.strftime('%p')

        return context

   
    def post( self,request,*args,**kwargs ):
        '''Modifying the input data before validation.'''

        FORM = request.POST.copy()

        #[ print( x , '<--BEFORE-->', y ) for x,y in FORM.items()  ]
        
        FORM['sleep_at']      = self.make_time( FORM['sleep_at_hour'], FORM['sleep_at_minute'], FORM['sleep_at_interval'] ) 
        FORM['arise_at']      = self.make_time( FORM['arise_at_hour'], FORM['arise_at_minute'], FORM['arise_at_interval'] ) 
        FORM['noon_arise_at'] = self.make_time( FORM['noon_arise_at_hour'], FORM['noon_arise_at_minute'], FORM['noon_arise_at_interval'] ) 
        FORM['noon_sleep_at'] = self.make_time( FORM['noon_sleep_at_hour'], FORM['noon_sleep_at_minute'], FORM['noon_sleep_at_interval'] ) 

        request.POST = FORM

        return super( SleepUpdateView,self ).post( request,*args,**kwargs )


