from django.http          import HttpResponse
from django.views.generic import ListView , DetailView , CreateView , UpdateView
from .models              import Sleep
from .forms               import SleepAdminForm
from datetime             import datetime as dtt


'''
I have to write a custom class which helps 
in DRY principle in create-update views.
'''


class SleepCreateView( CreateView ):
    model         = Sleep
    template_name = 'sleep_new.html'
    form_class    = SleepAdminForm


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
            
            # Recursion
            return self.adding_date( ready_time )
        else:
            return None
    

    def post( self,request,*args,**kwargs ):
        '''Modifying the input data before validation.'''

        FORM = request.POST.copy()
        
        FORM['sleep_at']      = self.make_time( FORM['sleep_at_hour'],      FORM['sleep_at_minute'],      FORM['sleep_at_interval'] ) 
        FORM['arise_at']      = self.make_time( FORM['arise_at_hour'],      FORM['arise_at_minute'],      FORM['arise_at_interval'] ) 
        FORM['noon_arise_at'] = self.make_time( FORM['noon_arise_at_hour'], FORM['noon_arise_at_minute'], FORM['noon_arise_at_interval'] ) 
        FORM['noon_sleep_at'] = self.make_time( FORM['noon_sleep_at_hour'], FORM['noon_sleep_at_minute'], FORM['noon_sleep_at_interval'] ) 


        #[ print( x , ' <--MODIFIED--> ', y ) for x,y in FORM.items()  ]

        # function variable.
        #noon_sleep_at , noon_arise_at = FORM.get('noon_sleep_at') , FORM.get('noon_arise_at')
        #    
        #if noon_sleep_at and noon_arise_at :
        #    FORM['noon_sleep_at'] = self.adding_date( noon_sleep_at )
        #    FORM['noon_arise_at'] = self.adding_date( noon_arise_at )

       
        form = self.form_class( FORM )

        #[ print( x , ' --> ', y ) for x,y in  form.data.items() ]
        
        if form.is_valid():
            #print('\nIt\'s passes test \n')
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


    def form_valid( self,form ):
        #print('\n\n----------------Form is valid not problem at all---------------- \n\n')

        form_unsave           = form.save( commit=False )
        form_unsave.user_name = self.request.user
        #print( 'Form unsave - ',vars( form_unsave ), end='\n\n')

        return super( SleepCreateView,self ).form_valid( form )


    def form_invalid( self,form ):
        print( 'form_invalid error name - ',form.errors.as_json() )

        #[ print( 'Form invalid data views.py - ',x,' ',y,' ',type(y) ) for x,y in dict(form.data).items()  ]
        #return render_to_response( form )
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



class SleepUpdateView( UpdateView ):
    model         = Sleep
    template_name = 'sleep_edit.html'
    form_class    = SleepAdminForm

    def get( self,request,*args,**kwargs ):
        self.object = self.get_object()

        '''Data directly from the database'''
        #[ print( x,' - ', y ) for x,y in vars(self.object).items() ]  

        return super( SleepUpdateView,self ).get( request,*args,**kwargs )


    def get_context_data( self,**kwargs ):

        '''Insert model's data to the update form'''

        context = super( SleepUpdateView , self ).get_context_data( **kwargs )
        
        context['form'].fields['sleep_at_hour'].initial          = '01'
        context['form'].fields['sleep_at_minute'].initial        = '50'
        context['form'].fields['sleep_at_interval'].initial      = 'AM'

        context['form'].fields['arise_at_hour'].initial          = '01'
        context['form'].fields['arise_at_minute'].initial        = '50'
        context['form'].fields['arise_at_interval'].initial      = 'AM'
 
        context['form'].fields['noon_sleep_at_hour'].initial     = '01'
        context['form'].fields['noon_sleep_at_minute'].initial   = '50'
        context['form'].fields['noon_sleep_at_interval'].initial = 'AM'
        
        context['form'].fields['noon_arise_at_hour'].initial     = '01'
        context['form'].fields['noon_arise_at_minute'].initial   = '50'
        context['form'].fields['noon_arise_at_interval'].initial = 'AM'

        return context


    
    #def am_pm_converter( self , datetime_input ):
    #    '''Return valid datetime format as str object.'''

    #    return str( dtt.strptime( datetime_input,'%Y-%m-%d %I:%M %p') )

    #
    #def adding_date( self , data ):
    #    '''Adding dates with the time for datetime conversion.'''
    #    
    #    if data:
    #        return self.am_pm_converter( '2001-01-01 ' + data )

    #
    #def make_time( self , hour , minute , interval ):
    #    '''Returns a valid time pattern.'''

    #    if hour and minute and interval:
    #        ready_time =  hour + ':' + minute + ' ' + interval 
    #        
    #        # Recursion
    #        return self.adding_date( ready_time )
    #    else:
    #        return None
    #

    #def post( self,request,*args,**kwargs ):
    #    '''Modifying the input data before validation.'''

    #    FORM = request.POST.copy()
    #    
    #    FORM['sleep_at']      = self.make_time( FORM['sleep_at_hour'],      FORM['sleep_at_minute'],      FORM['sleep_at_interval'] ) 
    #    FORM['arise_at']      = self.make_time( FORM['arise_at_hour'],      FORM['arise_at_minute'],      FORM['arise_at_interval'] ) 
    #    FORM['noon_arise_at'] = self.make_time( FORM['noon_arise_at_hour'], FORM['noon_arise_at_minute'], FORM['noon_arise_at_interval'] ) 
    #    FORM['noon_sleep_at'] = self.make_time( FORM['noon_sleep_at_hour'], FORM['noon_sleep_at_minute'], FORM['noon_sleep_at_interval'] ) 


    #    #[ print( x , ' <--MODIFIED--> ', y ) for x,y in FORM.items()  ]

    #    # function variable.
    #    #noon_sleep_at , noon_arise_at = FORM.get('noon_sleep_at') , FORM.get('noon_arise_at')
    #    #    
    #    #if noon_sleep_at and noon_arise_at :
    #    #    FORM['noon_sleep_at'] = self.adding_date( noon_sleep_at )
    #    #    FORM['noon_arise_at'] = self.adding_date( noon_arise_at )

    #   
    #    form = self.form_class( FORM )

    #    #[ print( x , ' --> ', y ) for x,y in  form.data.items() ]
    #    
    #    if form.is_valid():
    #        #print('\nIt\'s passes test \n')
    #        return self.form_valid(form)
    #    else:
    #        return self.form_invalid(form)


    #def form_valid( self,form ):
    #    #print('\n\n----------------Form is valid not problem at all---------------- \n\n')

    #    form_unsave           = form.save( commit=False )
    #    form_unsave.user_name = self.request.user
    #    #print( 'Form unsave - ',vars( form_unsave ), end='\n\n')

    #    return super( SleepCreateView,self ).form_valid( form )


    #def form_invalid( self,form ):
    #    print( 'form_invalid error name - ',form.errors.as_json() )

    #    #[ print( 'Form invalid data views.py - ',x,' ',y,' ',type(y) ) for x,y in dict(form.data).items()  ]
    #    #return render_to_response( form )
    #    error = form.errors.as_ul()
    #    return HttpResponse('<h1>{}</h1>'.format(error) )


