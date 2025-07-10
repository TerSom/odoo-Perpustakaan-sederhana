from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Book Master'

    name = fields.Char(string='Title', required=True)
    author = fields.Char(string='Author')
    published_date = fields.Date(string='Published Date')
    cover_image = fields.Binary(string='Cover Image', attachment=True)
    quantity = fields.Integer(string='Quantity', default=1)
    
    def download_excel_book(self):
        return {
            'type': 'ir.actions.act_url',
            'name': 'Download Excel Book',
            'url': f'/report_Book/report_excel_book/{self.id}',
            'target': 'new',
        }