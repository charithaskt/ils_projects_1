from django.db import models
from django.urls import reverse #Used to generate urls by reversing the URL patterns
from django.contrib.auth import get_user_model
from django.utils import timezone
from accounts.models import Profile
from django.core.urlresolvers import reverse


itemtype_choices = ( 
       ('BK', 'Book'),
       ('PR', 'Project Report'),
       ('TD', 'Theses'),
       ('XM', 'Xerox Material'),
       ('RB', 'Reference Book'),
)

item_status_choices = (
       ('AV', 'Available'),
       ('OL', 'On Loan'),
       ('DM', 'Damaged'),
       ('LO', 'Lost'),
       ('LP', 'Lost and Paid for'),
       ('MI', 'Missing'),
       ('OD', 'Long Overdue'),
       ('WD', 'Withdrawn'),
       ('BD', 'In Bindery'),
)
location_choices = (
        ('GEN', 'General Shelf'),
        ('REF', 'Reference Shelf'),
        ('OD' , 'On-Display'),
        ('PROC','Processing Center'),
        ('SO',  'Staff Office'),
        ('BC',  'Book Cart'),
        ('NMS', 'New Materials Shelf'),
)
notforloan_choices = (
        ('1', 'Not for loan'),
        ('2', 'Staff Copy'),
        ('3', 'Ordered'),
)
typecode_choices = (
       ('ISSUE',  'issue'),
       ('RETURN', 'return'),
       ('RENEW',  'remew'),
       ('PAYMENT','payment'),
)
accounttype_choices = (
       ('F', 'Fine levied'),
       ('FU', 'Overdue Fine'),
       ('N', 'New Card'),
       ('FOR','Forgiven'),
       ('FFOR', 'Forgiven Overdue Fine'),
       ('M', 'Sundry'),
       ('PAY', 'Payment'),
       ('REP', 'Replacement Charge'),
       ('RES', 'Reserve Charge'),
       ('W', 'Written off'), 
       ('RENT', 'Rental Charge'),
)
module_choices = (
   ('CATALOGING', 'Cataloguing'),
   ('CIRCULATION', 'Circulation'),
   ('PATRONS', 'Patrons'),
   ('SYSTEMPREFERENCES', 'System Preferences'),
   ('FINES', 'Fines'), 
   ('REPORT', 'Report'),
   ('TOOLS', 'Tools'), #bulk import/export, backup/restore, global modiffs
   ('CALENDAR', 'Holiday Calendar'),
)

action_choices = (
  ('CREATE', 'Create'),
  ('ADD', 'Add child records'),
  ('MODIFY', 'Modify or edit record'),
  ('ISSUE', 'Issue'),
  ('RETURN', 'Return'),
  ('RENEW', 'Renew'),
  ('DELETE', 'Delete'),
  ('CHANGE PASS', 'Change Password Through Staff Client'),
  ('RESERVE', 'RESERVE through Staff Client'),
  ('FINE', 'Collect fine through Staff Client'),
  ('RUN', 'Run report'),
)

"""
Sample reasons:
moderator_reason_choices = (
  ('1',  'No author mentioned'),
  ('2',  'Library already has enough copies'),
  ('3',  'Expensive'),
  ('4',  'Not relevant for the course'),
  ('5',  'Institution policies do not permit the purchase'),
  ('6',  'Will be purchased soon'),
  ('7',  'Will be purchased later'),
  ('8',  'Out of print'),
  ('9',  'Can not get immediately as it has to be imported'),
  ('10', 'Single copy will be purchased'),
  ('11', 'Few copies will be purchased'),
  ('12', 'Publisher not known'),
  ('13', 'No such title'),
  ('14', 'Not immediately required'),
)
"""

suggestions_status_choices = (
   ('ASKED', 'User asked'),
   ('ACCEPTED', 'Suggestion has been accepted'),
   ('REJECTED', 'Suggestion has been rejected'),
   ('PENDING', 'Decision is kept pending'),
) 

holiday_type_choices = (
   ('WEEKEND', 'Weekend holiday'), # Sundays and (Saturdays if all are holidays)
   ('YEARLY', 'Yearly holidays on the same day'),
   ('ADHOC', 'Adhoc holidays'),
)

"""
Sample category codes. Individual library may like have their
own choices here.
This category is used for setting circulation rules
categorycode_choices = (
        ('SU' , 'Student - UG'),
        ('SP' , 'Student - PG'),
        ('SR' , 'Student - Research Scholar'),
        ('FT'   , 'Teaching Staff'),
        ('NT'   , 'Non-Teaching Staff'),
        ('LS'   , 'Library Staff'), #may be removed and categorized under 'NT'
        ('HA'   , 'Higher Authority'),
)

"""
#when a user self registers he will automatically become member of the library.
#But the user can't start borrowing untill categorized into one of the above 
#mentioned groups. 

class Categories(models.Model):
    categorycode = models.CharField(max_length=10,unique=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return "{} ({})".format(self.description, self.categorycode)

class Departments(models.Model):
    deptcode = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return "{} ({})".format(self.description, self.deptcode)



class Designations(models.Model):
    designation = models.CharField(max_length=50,unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return "{} ({})".format(self.description, self.designation)

class Borrowers(models.Model):
   borrower = models.ForeignKey(
      Profile,
      on_delete=models.SET_NULL,
      null=True
   )
   email = models.EmailField(max_length=255,
      unique=True,
   )
   cardnumber = models.CharField(max_length=16, unique=True) #should be unique field
   surname = models.CharField(max_length=100) #should be unique field
   firstname = models.CharField(max_length=100) #should be unique field
   mobile = models.CharField(max_length=32,blank=True,null=True)
   dateenrolled = models.DateField(auto_now_add=True)
   dateexpiry = models.DateField()
   gonenoaddress = models.BooleanField(default=False)
   lost = models.BooleanField(default=False)
   debarred = models.DateField(auto_now_add=True,blank=True, null=True)
   debarredcomment = models.CharField(max_length=100, blank=True, null=True)
   category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True)
   department = models.ForeignKey(Departments,on_delete=models.SET_NULL, null=True, blank=True)
   designation = models.ForeignKey(Designations, on_delete=models.SET_NULL, null=True, blank=True)
   borrowernote  =  models.CharField(max_length=255, null=True, blank=True)
   opacnote  =  models.CharField(max_length=255,null=True, blank=True)
   timestamp_lastupdated = models.DateTimeField(auto_now=True)
   timestamp_added = models.DateTimeField(auto_now_add=True)

   def __str__(self):
        return "{},{} ({}) - [{}]".format( self.firstname,self.surname,self.cardnumber, self.category.categorycode)

   def get_absolute_url(self):
        return reverse('borrower-detail', args=[self.id])

class PatronImages(models.Model):
   borrower = models.ForeignKey(Borrowers,on_delete=models.CASCADE)
   mimetype = models.CharField(max_length=15)
   imagefile = models.BinaryField()


class Genre(models.Model):
    name = models.CharField(max_length=60, unique=True, help_text='Enter the topic')
    
    def __str__(self):
        return self.name

class Language(models.Model):
    """
    Model representing a Language (e.g. English, Telugu, Tamil, Kannda, etc.)
    """
    name = models.CharField(max_length=30, unique=True,help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")
    def __str__(self):
       return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name

class Authors(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    def __str__(self):
        return "{}, {}".format(self.firstname, self.lastname)

class CorporateAuthor(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Biblio(models.Model):
    biblionumber = models.AutoField(primary_key=True)
    isbn = models.CharField('ISBN', max_length=13)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True),
    callnumber = models.CharField(max_length=15, blank=True, null=True)
    authors = models.ManyToManyField(Authors, blank=True,verbose_name="authors")
    corporateauthor = models.ForeignKey(CorporateAuthor, on_delete=models.SET_NULL, null=True),
    title = models.CharField(max_length=250)
    edition = models.CharField(max_length=50, null=True, blank=True)
    copyrightdate = models.PositiveSmallIntegerField(null=True, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL,null=True, blank=True, verbose_name="Publication details")
    series = models.CharField(max_length=250, null=True, blank=True)
    volume = models.CharField(max_length=20, null=True, blank=True)
    pages = models.CharField(max_length=10)
    size  = models.CharField(max_length=5)
    genre = models.ManyToManyField(Genre,blank=True,verbose_name="Topical Term")
    contents_url = models.URLField(max_length=200, blank=True, null=True)
    index_url = models.URLField(max_length=200, blank=True, null=True)
    itemtype = models.CharField(
       max_length = 2,
       choices = itemtype_choices,
       default = 'BK',
    ) 
    totalissues = models.IntegerField()  #system generated  
    timestamp_lastupdated = models.DateTimeField(auto_now=True) #system generated
    timestamp_added = models.DateTimeField(auto_now_add=True) #system generated

    def __str__(self):
        return "{} : {}".format(self.itemtype, self.title)

    def get_absolute_url(self):
        return reverse('biblio-detail', args=[self.biblionumber])
      
class Items(models.Model):
    itemnumber = models.AutoField(primary_key=True)
    biblionumber = models.ForeignKey(Biblio, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=25, unique=True)
    dateaccessined = models.DateField(auto_now_add=True)
    booksellerid = models.CharField(max_length=25, blank=True, null=True)  
    invoicenumber = models.CharField(max_length=15, blank=True, null=True)
    invoicedate = models.DateField(auto_now_add=True)
    totalissues = models.PositiveSmallIntegerField(null=True, blank=True)
    itemstatus = models.CharField(max_length=2,choices=item_status_choices,default='AV')  
    location = models.CharField(max_length=4,choices=location_choices,default='GEN')  
    notforloan = models.CharField(max_length=1,choices=notforloan_choices,blank=True, null=True)  
    price  = models.DecimalField(decimal_places=2,max_digits=7, blank=True, null=True)
    replacementprice  = models.DecimalField(decimal_places=2,max_digits=7,blank=True, null=True)
    timestamp_lastupdated = models.DateTimeField(auto_now=True) #this field is set by the app
    timestamp_added = models.DateTimeField(auto_now_add=True)   #this field is set by the app

    def __str__(self):
        return self.barcode

    def get_absolute_url(self):
        return reverse('item-detail', args=[self.itemnumber])


class BiblioImages(models.Model):
    imagenumber = models.AutoField(primary_key=True),
    biblionumber = models.ForeignKey(Biblio, on_delete=models.CASCADE)
    mimetype = models.CharField(max_length=15) 
    imagefile = models.BinaryField()
    
    def get_absolute_url(self):
       return reverse('biblioimage-detail', args=[self.imagenumber])

class Issues(models.Model):
   borrower = models.ForeignKey(Borrowers, on_delete=models.CASCADE)
   itemnumber  = models.ForeignKey(Items, on_delete=models.CASCADE)
   date_due = models.DateTimeField()
   issuedate = models.DateTimeField(default=timezone.now)
   renewals = models.PositiveSmallIntegerField(null=True, blank=True) #system sets this value
   returndate = models.DateTimeField(auto_now_add=True, blank=True, null=True) #system sets this value
   timestamp_lastupdated = models.DateTimeField(auto_now=True)

#System addes records to statistics table - no manual entries
class Statistics(models.Model):
   borrower = models.ForeignKey(Borrowers, on_delete=models.CASCADE)
   itemnumber = models.ForeignKey(Items, on_delete=models.CASCADE)
   usercode = models.IntegerField(null=True,blank=True)   #system puts borrowernumber of the staff
   typecode = models.CharField(max_length=7,choices=typecode_choices) 
   value  = models.DecimalField(decimal_places=2,max_digits=7,null=True, blank=True)
   datetime = models.DateTimeField(auto_now_add=True) 
   

class Reserves(models.Model):
    reserveid = models.AutoField(primary_key=True)
    borrower = models.ForeignKey(Borrowers, on_delete=models.CASCADE)
    biblionumber = models.ForeignKey(Biblio, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    reservedate = models.DateTimeField(auto_now_add=True)
    cancellationdate = models.DateTimeField(auto_now_add=True) 
    priority = models.PositiveSmallIntegerField(null=True, blank=True)
    found = models.BooleanField(default=False)
    notificationdate = models.DateTimeField(auto_now_add=True)
    waitingdate = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now) 

#system automatically adds records to this table. No manual entry.
class AccountOffsets(models.Model):
   borrower = models.ForeignKey(Borrowers, on_delete = models.CASCADE)
   amountoutstanding  = models.DecimalField(decimal_places=2,max_digits=7)

#system automatically adds records to this table. No manual entry.
class AccountLines(models.Model):
   accountlines_id = models.AutoField(primary_key=True)
   borrower = models.ForeignKey(Borrowers,on_delete=models.CASCADE)
   itemnumber = models.ForeignKey(Items, on_delete=models.CASCADE)
   date = models.DateField(auto_now_add=True)
   amount  = models.DecimalField(decimal_places=2,max_digits=7)
   description = models.CharField(max_length=255, null=True, blank=True)
   accounttype = models.CharField(max_length=4,choices = accounttype_choices)
   manager_id = models.IntegerField()

#note -ve values for payments and +ve values for levies 

#system automatically adds records to this table when the visitor's id card is scanned at the entrace and exit
class EntryExitLogs(models.Model):
   borrower = models.ForeignKey(Borrowers, on_delete=models.CASCADE,null=True, blank=True)
   cardnumber = models.CharField(max_length=16, unique=True)
   timeofentry = models.DateTimeField(auto_now_add=True)
   timeofexit = models.DateTimeField(auto_now_add=True)

#system generated records
class ActionLogs(models.Model):
   action_id = models.AutoField(primary_key=True)
   timestamp = models.DateTimeField(auto_now_add=True)
   usercode = models.ForeignKey(Borrowers,on_delete = models.CASCADE)
   module = models.CharField(max_length=17,choices=module_choices)
   action = models.CharField(max_length=11,choices=action_choices)

class SystemPreferences(models.Model):
   variable = models.CharField(max_length=50,unique=True)
   value = models.CharField(max_length=255)
   options = models.CharField(max_length=255) #options separated by '|' symbol
   descriptive_options = models.CharField(max_length=1000) #separated by '|' symbol
   explanation = models.CharField(max_length=255)
   vartype = models.CharField(max_length=20) #YesNo - Choice - TextInput

class ModeratorReasons(models.Model):
   reason = models.CharField(max_length=255)

class Suggestions(models.Model):
   suggestionid = models.AutoField(primary_key=True)
   suggestedby = models.ForeignKey(Borrowers,on_delete = models.CASCADE)
   suggesteddate = models.DateField(auto_now_add=True,blank=True,null=True)
   acceptedby = models.CharField(max_length=16, unique=True) #card number
   #acceptedby = models.IntegerField(blank=True, null=True)
   accepteddate = models.DateField(auto_now_add=True,blank=True,null=True)
   rejectedby = models.CharField(max_length=16, unique=True) #card number
   #rejectedby = models.IntegerField(blank=True, null=True)
   rejecteddate = models.DateField(auto_now_add=True,blank=True,null=True)
   status = models.CharField(max_length=8,choices=suggestions_status_choices, default='ASKED')
   note = models.TextField(blank=True,null=True)
   author = models.CharField(max_length=100,blank=True,null=True)
   title  = models.CharField(max_length=255)
   copyrightdate = models.PositiveSmallIntegerField(null=True, blank=True)
   publishercode = models.CharField(max_length=100,blank=True,null=True)
   isbn = models.CharField(max_length=13,blank=True,null=True)
   reason = models.ForeignKey(ModeratorReasons,on_delete=models.SET_NULL,blank=True, null=True)
   price = models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)
   total = models.DecimalField(max_digits=7,decimal_places=2,blank=True,null=True)

class Tags(models.Model):
   tag = models.CharField(max_length=100)
   approved = models.NullBooleanField(null=True,blank=True)
   date_moderated = models.DateTimeField(auto_now_add=True,null=True, blank=True)
   approved_by = models.ForeignKey(Borrowers, on_delete=models.SET_NULL,null=True, blank=True)

class Holidays(models.Model):
   day = models.PositiveSmallIntegerField()
   month = models.PositiveSmallIntegerField()
   year = models.PositiveSmallIntegerField()
   isexception = models.BooleanField(default=True)
   title = models.CharField(max_length=100)
   holiday_type = models.CharField(max_length=7,choices=holiday_type_choices)

from django.shortcuts import reverse

itemtype_choices = ( 
       ('BK', 'Book'),
       ('PR', 'Project Report'),
       ('TD', 'Theses'),
       ('XM', 'Xerox Material'),
       ('RB', 'Reference Book'),
)
item_status_choices = (
       ('AV', 'Available'),
       ('OL', 'On Loan'),
       ('DM', 'Damaged'),
       ('LO', 'Lost'),
       ('LP', 'Lost and Paid for'),
       ('MI', 'Missing'),
       ('OD', 'Long Overdue'),
       ('WD', 'Withdrawn'),
       ('BD', 'In Bindery'),
)
location_choices = (
        ('GEN', 'General Shelf'),
        ('REF', 'Reference Shelf'),
        ('OD' , 'On-Display'),
        ('PROC','Processing Center'),
        ('SO',  'Staff Office'),
        ('BC',  'Book Cart'),
        ('NMS', 'New Materials Shelf'),
)
notforloan_choices = (
        ('1', 'Not for loan'),
        ('2', 'Staff Copy'),
        ('3', 'Ordered'),
)
typecode_choices = (
       ('ISSUE',  'issue'),
       ('RETURN', 'return'),
       ('RENEW',  'remew'),
       ('PAYMENT','payment'),
)
accounttype_choices = (
       ('F', 'Fine levied'),
       ('FU', 'Overdue Fine'),
       ('N', 'New Card'),
       ('FOR','Forgiven'),
       ('FFOR', 'Forgiven Overdue Fine'),
       ('M', 'Sundry'),
       ('PAY', 'Payment'),
       ('REP', 'Replacementi Charge'),
       ('RES', 'Reserve Charge'),
       ('W', 'Written off'), 
       ('RENT', 'Rental Charge'),
)
module_choices = (
   ('CATALOGING', 'Cataloguing'),
   ('CIRCULATION', 'Circulation'),
   ('PATRONS', 'Patrons'),
   ('SYSTEMPREFERENCES', 'System Preferences'),
   ('FINES', 'Fines'), 
   ('REPORT', 'Report'),
   ('TOOLS', 'Tools'), #bulk import/export, backup/restore, global modiffs
   ('CALENDAR', 'Holiday Calendar'),
)

action_choices = (
  ('CREATE', 'Create'),
  ('ADD', 'Add child records'),
  ('MODIFY', 'Modify or edit record'),
  ('ISSUE', 'Issue'),
  ('RETURN', 'Return'),
  ('RENEW', 'Renew'),
  ('DELETE', 'Delete'),
  ('CHANGE PASS', 'Change Password Through Staff Client'),
  ('RESERVE', 'RESERVE through Staff Client'),
  ('FINE', 'Collect fine through Staff Client'),
  ('RUN', 'Run report'),
)

"""
Sample reasons:
moderator_reason_choices = (
  ('1',  'No author mentioned'),
  ('2',  'Library already has enough copies'),
  ('3',  'Expensive'),
  ('4',  'Not relevant for the course'),
  ('5',  'Institution policies do not permit the purchase'),
  ('6',  'Will be purchased soon'),
  ('7',  'Will be purchased later'),
  ('8',  'Out of print'),
  ('9',  'Can not get immediately as it has to be imported'),
  ('10', 'Single copy will be purchased'),
  ('11', 'Few copies will be purchased'),
  ('12', 'Publisher not known'),
  ('13', 'No such title'),
  ('14', 'Not immediately required'),
)
"""

suggestions_status_choices = (
   ('ASKED', 'User asked'),
   ('ACCEPTED', 'Suggestion has been accepted'),
   ('REJECTED', 'Suggestion has been rejected'),
   ('PENDING', 'Decision is kept pending'),
) 

holiday_type_choices = (
   ('WEEKEND', 'Weekend holiday'), # Sundays and (Saturdays if all are holidays)
   ('YEARLY', 'Yearly holidays on the same day'),
   ('ADHOC', 'Adhoc holidays'),
)

"""
Sample category codes. Individual library may like have their
own choices here.
This category is used for setting circulation rules
categorycode_choices = (
        ('SU' , 'Student - UG'),
        ('SP' , 'Student - PG'),
        ('SR' , 'Student - Research Scholar'),
        ('FT'   , 'Teaching Staff'),
        ('NT'   , 'Non-Teaching Staff'),
        ('LS'   , 'Library Staff'), #may be removed and categorized under 'NT'
        ('HA'   , 'Higher Authority'),
)

"""
#when a user self registers he will automatically become member of the library.
#But the user can't start borrowing untill categorized into one of the above 
#mentioned groups. 

class Categories(models.Model):
    categorycode = models.CharField(max_length=10,unique=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return "{} ({})".format(self.description, self.categorycode)

class Departments(models.Model):
    deptcode = models.CharField(max_length=10, unique=True)
    description = models.CharField(max_length=50)

    def __str__(self):
        return "{} ({})".format(self.description, self.deptcode)

class Designations(models.Model):
    designation = models.CharField(max_length=50,unique=True)
    description = models.CharField(max_length=100)

    def __str__(self):
        return "{} ({})".format(self.description, self.designation)

class Borrowers(models.Model):
   borrower = models.ForeignKey(
      Profile,
      on_delete=models.SET_NULL,
      null=True
   )
   email = models.EmailField(max_length=255,
      unique=True,
   )
   cardnumber = models.CharField(max_length=16, unique=True) #should be unique field
   surname = models.CharField(max_length=100) #should be unique field
   firstname = models.CharField(max_length=100) #should be unique field
   mobile = models.CharField(max_length=32,blank=True,null=True)
   dateenrolled = models.DateField(auto_now_add=True)
   dateexpiry = models.DateField()
   gonenoaddress = models.BooleanField(default=False)
   lost = models.BooleanField(default=False)
   debarred = models.DateField(auto_now_add=True,blank=True, null=True)
   debarredcomment = models.CharField(max_length=100, blank=True, null=True)
   category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True, blank=True)
   department = models.ForeignKey(Departments,on_delete=models.SET_NULL, null=True, blank=True)
   designation = models.ForeignKey(Designations, on_delete=models.SET_NULL, null=True, blank=True)
   borrowernote  =  models.CharField(max_length=255, null=True, blank=True)
   opacnote  =  models.CharField(max_length=255,null=True, blank=True)
   timestamp_lastupdated = models.DateTimeField(auto_now=True)
   timestamp_added = models.DateTimeField(auto_now_add=True)

   def __str__(self):
        return "{},{} ({}) - [{}]".format( self.firstname,self.surname,self.cardnumber, self.category.categorycode)

   def get_absolute_url(self):
        return reverse('borrower-detail', args=[self.id])

class PatronImages(models.Model):
   borrower = models.ForeignKey(Borrowers,on_delete=models.CASCADE)
   mimetype = models.CharField(max_length=15)
   imagefile = models.BinaryField()


class Genre(models.Model):
    name = models.CharField(max_length=60, unique=True, help_text='Enter the topic')
    
    def __str__(self):
        return self.name

class Language(models.Model):
    """
    Model representing a Language (e.g. English, Telugu, Tamil, Kannda, etc.)
    """
    name = models.CharField(max_length=30, unique=True,help_text="Enter the book's natural language (e.g. English, French, Japanese etc.)")
    def __str__(self):
       return self.name


class Publisher(models.Model):
    name = models.CharField(max_length=200, unique=True)
    
    def __str__(self):
        return self.name

class Authors(models.Model):
    firstname = models.CharField(max_length=200)
    lastname = models.CharField(max_length=200)
    def __str__(self):
        return "{}, {}".format(self.firstname, self.lastname)

class CorporateAuthor(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name

class Biblio(models.Model):
    biblionumber = models.AutoField(primary_key=True)
    isbn = models.CharField('ISBN', max_length=13)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, null=True),
    callnumber = models.CharField(max_length=15, blank=True, null=True)
    authors = models.ManyToManyField(Authors, blank=True,null=True)
    corporateauthor = models.ForeignKey(CorporateAuthor, on_delete=models.SET_NULL, null=True),
    title = models.CharField(max_length=250)
    edition = models.CharField(max_length=50, null=True, blank=True)
    copyrightdate = models.PositiveSmallIntegerField(null=True, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL,null=True, blank=True, verbose_name="Publication details")
    series = models.CharField(max_length=250, null=True, blank=True)
    volume = models.CharField(max_length=20, null=True, blank=True)
    pages = models.CharField(max_length=10)
    size  = models.CharField(max_length=5)
    genre = models.ManyToManyField(Genre, blank=True, null=True,verbose_name="Topical Term")
    contents_url = models.URLField(max_length=200, blank=True, null=True)
    index_url = models.URLField(max_length=200, blank=True, null=True)
    itemtype = models.CharField(
       max_length = 2,
       choices = itemtype_choices,
       default = 'BK',
    ) 
    totalissues = models.IntegerField()  #system generated  
    timestamp_lastupdated = models.DateTimeField(auto_now=True) #system generated
    timestamp_added = models.DateTimeField(auto_now_add=True) #system generated

    def __str__(self):
        return "{} : {}".format(self.itemtype, self.title)

    def get_absolute_url(self):
        return reverse('biblio-detail', args=[self.biblionumber])
      
class Items(models.Model):
    itemnumber = models.AutoField(primary_key=True)
    biblionumber = models.ForeignKey(Biblio, on_delete=models.CASCADE)
    barcode = models.CharField(max_length=25, unique=True)
    dateaccessined = models.DateField(auto_now_add=True)
    booksellerid = models.CharField(max_length=25, blank=True, null=True)  
    invoicenumber = models.CharField(max_length=15, blank=True, null=True)
    invoicedate = models.DateField(auto_now_add=True)
    totalissues = models.PositiveSmallIntegerField(null=True, blank=True)
    itemstatus = models.CharField(max_length=2,choices=item_status_choices,default='AV')  
    location = models.CharField(max_length=4,choices=location_choices,default='GEN')  
    notforloan = models.CharField(max_length=1,choices=notforloan_choices,blank=True, null=True)  
    price  = models.DecimalField(decimal_places=2,max_digits=7, blank=True, null=True)
    replacementprice  = models.DecimalField(decimal_places=2,max_digits=7,blank=True, null=True)
    timestamp_lastupdated = models.DateTimeField(auto_now=True) #this field is set by the app
    timestamp_added = models.DateTimeField(auto_now_add=True)   #this field is set by the app

    def __str__(self):
        return self.barcode

    def get_absolute_url(self):
        return reverse('item-detail', args=[self.itemnumber])


class BiblioImages(models.Model):
    imagenumber = models.AutoField(primary_key=True),
    biblionumber = models.ForeignKey(Biblio, on_delete=models.CASCADE)
    mimetype = models.CharField(max_length=15) 
    imagefile = models.BinaryField()
    
    def get_absolute_url(self):
       return reverse('biblioimage-detail', args=[self.imagenumber])

class Issues(models.Model):
   borrower = models.ForeignKey(Borrowers, on_delete=models.CASCADE)
   itemnumber  = models.ForeignKey(Items, on_delete=models.CASCADE)
   date_due = models.DateTimeField()
   issuedate = models.DateTimeField(default=timezone.now)
   renewals = models.PositiveSmallIntegerField(null=True, blank=True) #system sets this value
   returndate = models.DateTimeField(auto_now_add=True, blank=True, null=True) #system sets this value
   timestamp_lastupdated = models.DateTimeField(auto_now=True)

#System addes records to statistics table - no manual entries
class Statistics(models.Model):
   borrower = models.ForeignKey(Borrowers, on_delete=models.CASCADE)
   itemnumber = models.ForeignKey(Items, on_delete=models.CASCADE)
   usercode = models.IntegerField(null=True,blank=True)   #system puts borrowernumber of the staff
   typecode = models.CharField(max_length=7,choices=typecode_choices) 
   value  = models.DecimalField(decimal_places=2,max_digits=7,null=True, blank=True)
   datetime = models.DateTimeField(auto_now_add=True) 
   

class Reserves(models.Model):
    reserveid = models.AutoField(primary_key=True)
    borrower = models.ForeignKey(Borrowers, on_delete=models.CASCADE)
    biblionumber = models.ForeignKey(Biblio, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    reservedate = models.DateTimeField(auto_now_add=True)
    cancellationdate = models.DateTimeField(auto_now_add=True) 
    priority = models.PositiveSmallIntegerField(null=True, blank=True)
    found = models.BooleanField(default=False)
    notificationdate = models.DateTimeField(auto_now_add=True)
    waitingdate = models.DateTimeField(auto_now_add=True)
    timestamp = models.DateTimeField(default=timezone.now) 

#system automatically adds records to this table. No manual entry.
class AccountOffsets(models.Model):
   borrower = models.ForeignKey(Borrowers, on_delete = models.CASCADE)
   amountoutstanding  = models.DecimalField(decimal_places=2,max_digits=7)

#system automatically adds records to this table. No manual entry.
class AccountLines(models.Model):
   accountlines_id = models.AutoField(primary_key=True)
   borrower = models.ForeignKey(Borrowers,on_delete=models.CASCADE)
   itemnumber = models.ForeignKey(Items, on_delete=models.CASCADE)
   date = models.DateField(auto_now_add=True)
   amount  = models.DecimalField(decimal_places=2,max_digits=7)
   description = models.CharField(max_length=255, null=True, blank=True)
   accounttype = models.CharField(max_length=4,choices = accounttype_choices)
   manager_id = models.IntegerField()

#note -ve values for payments and +ve values for levies 

#system automatically adds records to this table when the visitor's id card is scanned at the entrace and exit
class EntryExitLogs(models.Model):
   borrower = models.ForeignKey(Borrowers, on_delete=models.CASCADE,null=True, blank=True)
   cardnumber = models.CharField(max_length=16, unique=True)
   timeofentry = models.DateTimeField(auto_now_add=True)
   timeofexit = models.DateTimeField(auto_now_add=True)

#system generated records
class ActionLogs(models.Model):
   action_id = models.AutoField(primary_key=True)
   timestamp = models.DateTimeField(auto_now_add=True)
   usercode = models.ForeignKey(Borrowers,on_delete = models.CASCADE)
   module = models.CharField(max_length=17,choices=module_choices)
   action = models.CharField(max_length=11,choices=action_choices)

class SystemPreferences(models.Model):
   variable = models.CharField(max_length=50,unique=True)
   value = models.CharField(max_length=255)
   options = models.CharField(max_length=255) #options separated by '|' symbol
   descriptive_options = models.CharField(max_length=1000) #separated by '|' symbol
   explanation = models.CharField(max_length=255)
   vartype = models.CharField(max_length=20) #YesNo - Choice - TextInput

class ModeratorReasons(models.Model):
   reason = models.CharField(max_length=255)

class Suggestions(models.Model):
   suggestionid = models.AutoField(primary_key=True)
   suggestedby = models.ForeignKey(Borrowers,on_delete = models.CASCADE)
   suggesteddate = models.DateField(auto_now_add=True,blank=True,null=True)
   acceptedby = models.CharField(max_length=16, unique=True) #card number
   #acceptedby = models.IntegerField(blank=True, null=True)
   accepteddate = models.DateField(auto_now_add=True,blank=True,null=True)
   rejectedby = models.CharField(max_length=16, unique=True) #card number
   #rejectedby = models.IntegerField(blank=True, null=True)
   rejecteddate = models.DateField(auto_now_add=True,blank=True,null=True)
   status = models.CharField(max_length=8,choices=suggestions_status_choices, default='ASKED')
   note = models.TextField(blank=True,null=True)
   author = models.CharField(max_length=100,blank=True,null=True)
   title  = models.CharField(max_length=255)
   copyrightdate = models.PositiveSmallIntegerField(null=True, blank=True)
   publishercode = models.CharField(max_length=100,blank=True,null=True)
   isbn = models.CharField(max_length=13,blank=True,null=True)
   reason = models.ForeignKey(ModeratorReasons,on_delete=models.SET_NULL,blank=True, null=True)
   price = models.DecimalField(max_digits=6,decimal_places=2,blank=True,null=True)
   total = models.DecimalField(max_digits=7,decimal_places=2,blank=True,null=True)

class Tags(models.Model):
   tag = models.CharField(max_length=100)
   approved = models.NullBooleanField(null=True,blank=True)
   date_moderated = models.DateTimeField(auto_now_add=True,null=True, blank=True)
   approved_by = models.ForeignKey(Borrowers, on_delete=models.SET_NULL,null=True, blank=True)

class Holidays(models.Model):
   day = models.PositiveSmallIntegerField()
   month = models.PositiveSmallIntegerField()
   year = models.PositiveSmallIntegerField()
   isexception = models.BooleanField(default=True)
   title = models.CharField(max_length=100)
   holiday_type = models.CharField(max_length=7,choices=holiday_type_choices)

class Stopwords(models.Model):
   word = models.CharField(max_length=255)

class SearchHistory(models.Model):
   user = models.ForeignKey(Profile, on_delete=models.CASCADE)
   sessionid = models.CharField(max_length=32),
   query_desc = models.CharField(max_length=255)
   query_url = models.CharField(max_length=1000)
 
class Quotations(models.Model):
   source = models.CharField(max_length=255)
   text = models.CharField(max_length=1500)  
   timestamp = models.DateTimeField(auto_now_add=True)

class News(models.Model):
   title = models.CharField(max_length=250)
   language = models.CharField(max_length=25)
   timestamp = models.DateTimeField(auto_now_add=True)
   expirationdate = models.DateField(null=True, blank=True)
   number = models.PositiveSmallIntegerField(null=True, blank=True)

class RentalCharges(models.Model):
   itemtype = models.CharField(choices=itemtype_choices, max_length=2)
   rentalcharge =  models.DecimalField(decimal_places=2,max_digits=7, blank=True, null=True)

class IssuingRules(models.Model):
   categorycode = models.CharField(max_length=10)
   itemtype = models.CharField(max_length=10)
   maxissueqty = models.PositiveSmallIntegerField()
   issuelength = models.PositiveSmallIntegerField()
   renewalsallowed = models.PositiveSmallIntegerField(default=0)
   reservesallowed = models.PositiveSmallIntegerField(default=0)
   overduefinescap =  models.DecimalField(decimal_places=2,max_digits=7, blank=True, null=True)
   rentaldiscount  =  models.DecimalField(decimal_places=2,max_digits=7, blank=True, null=True)
   fine =  models.DecimalField(decimal_places=2,max_digits=7, blank=True, null=True)
   finedays = models.PositiveSmallIntegerField(default=0)
   chargeperiod = models.PositiveSmallIntegerField(default=0)

#system automatically adds records to this table. No manual entry.
class AccountOffsets(models.Model):
   borrower = models.ForeignKey(Borrowers, on_delete = models.CASCADE) #this field should also be unique
   amountoutstanding  = models.DecimalField(decimal_places=2,max_digits=7) #default=0 should be added

#system automatically adds records to this table. No manual entry.
class AccountLines(models.Model):
   accountlines_id = models.AutoField(primary_key=True)
   borrower = models.ForeignKey(Borrowers,on_delete=models.CASCADE)
   itemnumber = models.ForeignKey(Items, on_delete=models.CASCADE)
   date = models.DateField(auto_now_add=True)
   amount  = models.DecimalField(decimal_places=2,max_digits=7)
   description = models.CharField(max_length=255, null=True, blank=True)
   accounttype = models.CharField(max_length=4,choices = accounttype_choices)
   manager_id = models.IntegerField()

