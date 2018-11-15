# -*- coding: utf-8 -*-

from django import forms
from django.forms import Form
from django.forms import widgets
from django.forms import fields
from django.forms import ModelForm
from skuapp.models import *

class t_product_survey_ing_Form(ModelForm):

    #Keywords = forms.CharField(initial='like oldrss',widget=forms.Textarea(attrs={'class':'vLargeTextField'}))
    #image = forms.ImageField()
    #Keywords2 = forms.CharField(initial=0,widget=forms.TextInput(attrs={'style':'border:3px solid #ccc;'}),)
    #Name = forms.CharField(initial=0, widget=forms.TextInput(attrs={'readonly':'true'}))
    SurveyRemark = forms.CharField(widget=forms.Textarea(attrs={'width':'400px','heigth':'400px'}))
    class Meta:
        model = t_product_survey_ing
        fields = '__all__'
