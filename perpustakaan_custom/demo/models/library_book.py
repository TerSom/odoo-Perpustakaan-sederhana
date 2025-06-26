from odoo import models, fields, api

class LibraryBook(models.Model):
    _name = 'library.book'
    _description = 'Book Master'

    name = fields.Char(string='Title', required=True)
    author = fields.Char(string='Author')
    published_date = fields.Date(string='Published Date')
    cover_image = fields.Binary(string='Cover Image', attachment=True)
    quantity = fields.Integer(string='Quantity', default=1)

    borrowed_by_student_ids = fields.Many2many(
        'library.student',
        'library_book_student_rel',
        'book_id',
        'student_id',
        string='Borrowed By Students'
    )

    borrowed_by_teacher_ids = fields.Many2many(
        'library.teacher',
        'library_book_teacher_rel',
        'book_id',
        'teacher_id',
        string='Borrowed By Teachers'
    )

    borrowed_by_names = fields.Char(
        string='Borrowed By',
        compute='_compute_borrowed_by_names',
        store=False
    )

    @api.depends('borrowed_by_student_ids.name', 'borrowed_by_teacher_ids.name')
    def _compute_borrowed_by_names(self):
        for book in self:
            student_names = book.borrowed_by_student_ids.mapped('name')
            teacher_names = book.borrowed_by_teacher_ids.mapped('name')
            all_names = student_names + teacher_names
            book.borrowed_by_names = ', '.join(all_names)
