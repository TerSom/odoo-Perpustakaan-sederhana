from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Book Master'

    name = fields.Char(string='Title', required=True)
    author = fields.Char(string='Author')
    published_date = fields.Date(string='Published Date')
    cover_image = fields.Binary(string='Cover Image', attachment=True)
    quantity = fields.Integer(string='Quantity', default=1)