from django import forms

from .models import Booking, Detail

class DateInput(forms.DateInput):
	input_type = 'date'

class BookingForm(forms.ModelForm):
	class Meta:
		model = Booking
		fields = ('booking_date','city','event')
		widgets = {
			'booking_date': DateInput()
		}
	# def clean_city(self):
	# 	if not self.cleaned_data['city']:
	# 		raise forms.ValidationError('Enter the city for better results.')
	# def clean_event(self):
	# 	if not self.cleaned_data['event']:
	# 		raise forms.ValidationError('Enter the event field for better results.')

class CityForm(forms.ModelForm):
	class Meta:
		model = Booking
		fields = ('city',)

class EventForm(forms.ModelForm):
	class Meta:
		model = Booking
		fields = ('event',)

class DetailForm(forms.ModelForm):
	class Meta:
		model = Detail
		fields = ('decor','photography','people','DJ_Entertainment')

	# def clean_people(self):
	# 	people = self.cleaned_data.get('people')
	# 	if people < 0:
	# 		raise forms.ValidationError("No of People can't be negative")