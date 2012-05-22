# django-salesforce
#
# by Phil Christensen
# (c) 2012 Working Today
# See LICENSE.md for details
#

"""
Django models for accessing Salesforce objects.

The Salesforce database is somewhat un-UNIXy or non-Pythonic, in that
column names are all in CamelCase. No attempt is made to work around this
issue, but normal use of `db_column` and `table_name` parameters should work.
"""

import logging, urllib

from django.conf import settings
from django.db import models
from django.db.models.sql import compiler

from salesforce.backend import base, manager
from salesforce import fields

log = logging.getLogger(__name__)

class SalesforceModel(models.Model):
	"""
	Abstract model class for Salesforce objects.
	
	For convenience, this is encapsulated as a superclass, but if you
	need to inherit from another model class for some reason, you'll need
	override the 'objects' manager instance with the SalesforceManager,
	as well as create some kind of solution for routing to the proper
	database connection (salesforce.router.ModelRouter only looks for
	SalesforceModel subclasses).
	"""
	_base_manager = objects = manager.SalesforceManager()
	
	class Meta:
		abstract = True
		managed = False
	
	Id = fields.SalesforceIdField(primary_key=True)

class Account(SalesforceModel):
	"""
	Default Salesforce Account model.
	"""
	SALUTATIONS = [
		'Mr.', 'Ms.', 'Mrs.', 'Dr.', 'Prof.'
	]
	
	TYPES = [
		'Analyst', 'Competitor', 'Customer', 'Integrator', 'Investor',
		'Partner', 'Press', 'Prospect', 'Reseller', 'Other'
	]
	
	INDUSTRIES = [
		'Agriculture', 'Apparel', 'Banking', 'Biotechnology', 'Chemicals',
		'Communications', 'Construction', 'Consulting', 'Education',
		'Electronics', 'Energy', 'Engineering', 'Entertainment', 'Environmental',
		'Finance', 'Food & Beverage', 'Government', 'Healthcare', 'Hospitality',
		'Insurance', 'Machinery', 'Manufacturing', 'Media', 'Not For Profit',
		'Other', 'Recreation', 'Retail', 'Shipping', 'Technology', 'Telecommunications',
		'Transportation', 'Utilities'
	]
	
	Name = models.CharField(max_length=255)
	LastName = models.CharField(max_length=80)
	FirstName = models.CharField(max_length=40)
	Salutation = models.CharField(max_length=100, choices=[(x, x) for x in SALUTATIONS])
	Type = models.CharField(max_length=100, choices=[(x, x) for x in TYPES])
	BillingStreet = models.CharField(max_length=255)
	BillingCity = models.CharField(max_length=40)
	BillingState = models.CharField(max_length=20)
	BillingPostalCode = models.CharField(max_length=20)
	BillingCountry = models.CharField(max_length=40)
	ShippingStreet = models.CharField(max_length=255)
	ShippingCity = models.CharField(max_length=40)
	ShippingState = models.CharField(max_length=20)
	ShippingPostalCode = models.CharField(max_length=20)
	ShippingCountry = models.CharField(max_length=40)
	Phone = models.CharField(max_length=255)
	Fax = models.CharField(max_length=255)
	Website = models.CharField(max_length=255)
	Industry = models.CharField(max_length=100, choices=[(x, x) for x in INDUSTRIES])
	
	PersonEmail = models.CharField(max_length=100)
	
	def __unicode__(self):
		return self.Name

class Lead(SalesforceModel):
	"""
	Default Salesforce Lead model.
	"""
	FirstName = models.CharField(max_length=100)
	LastName = models.CharField(max_length=100)
	Email = models.CharField(max_length=100)
	
	def __unicode__(self):
		return self.FirstName + ' ' + self.LastName
