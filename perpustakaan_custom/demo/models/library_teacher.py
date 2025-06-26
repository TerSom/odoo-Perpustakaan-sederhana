from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryTeacher(models.Model):
    _name = 'library.teacher'
    _description = 'Teacher Master'

    name = fields.Char(string='Name', required=True)
    nip = fields.Char(string='NIP')
    phoneTeacher = fields.Char(string='Phone')
    email = fields.Char(string='Email')

    borrowed_book_ids = fields.Many2many(
        'library.book',
        'library_book_teacher_rel',
        'teacher_id',
        'book_id',
        string='Borrowed Books'
    )

    @api.model
    def create(self, vals):
        teacher = super().create(vals)

        if vals.get('borrowed_book_ids'):
            book_ids = vals['borrowed_book_ids'][0][2] if isinstance(vals['borrowed_book_ids'][0], tuple) and vals['borrowed_book_ids'][0][0] == 6 else []
            new_books = self.env['library.book'].browse(book_ids)
            for book in new_books:
                if book.quantity <= 0:
                    raise ValidationError(f"Buku '{book.name}' tidak tersedia.")
                book.quantity -= 1

        return teacher

    def write(self, vals):
        for teacher in self:
            if vals.get('borrowed_book_ids'):
                current_books = teacher.borrowed_book_ids

                commands = vals['borrowed_book_ids']
                added_ids = []

                for cmd in commands:
                    if cmd[0] == 4:  # append
                        added_ids.append(cmd[1])
                    elif cmd[0] == 6:  # replace
                        new_books = self.env['library.book'].browse(cmd[2])
                        added_books = new_books - current_books
                        added_ids.extend(added_books.ids)

                books_to_reduce = self.env['library.book'].browse(added_ids)
                for book in books_to_reduce:
                    if book.quantity <= 0:
                        raise ValidationError(f"Buku '{book.name}' tidak tersedia.")
                    book.quantity -= 1

        return super().write(vals)
