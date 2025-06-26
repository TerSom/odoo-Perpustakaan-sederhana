from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryStudent(models.Model):
    _name = 'library.student'
    _description = 'Student Master'

    name = fields.Char(string='Name', required=True)
    nis = fields.Char(string='NIS')
    tanggalPinjam = fields.Date(string='Tanggal Pinjam')
    tanggalKembali = fields.Date(string='Tanggal Kembali')
    phone = fields.Char(string='Phone')

    borrowed_book_ids = fields.Many2many(
        'library.book',
        'library_book_student_rel',
        'student_id',
        'book_id',
        string='Borrowed Books'
    )

    @api.model
    def create(self, vals):
        student = super().create(vals)

        if vals.get('borrowed_book_ids'):
            commands = vals['borrowed_book_ids']
            book_ids = []

            for cmd in commands:
                if cmd[0] == 4:  # add single book
                    book_ids.append(cmd[1])
                elif cmd[0] == 6:  # replace all
                    book_ids = cmd[2]

            new_books = self.env['library.book'].browse(book_ids)
            for book in new_books:
                if book.quantity <= 0:
                    raise ValidationError(f"Buku '{book.name}' tidak tersedia.")
                book.quantity -= 1

        return student

    def write(self, vals):
        for student in self:
            if vals.get('borrowed_book_ids'):
                current_books = student.borrowed_book_ids
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