from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryStudent(models.Model):
    _name = 'library.student'
    _description = 'Student Master'
    _rec_name = 'reference'

    reference = fields.Char(
        string="No",
        readonly=True,
        default='Kosong',
        copy=False
    )
    name = fields.Char(string='Name', required=True)
    nis = fields.Char(string='NIS', required=True)
    tanggalPinjam = fields.Date(string='Tanggal Pinjam', required=True)
    tanggalKembali = fields.Date(string='Tanggal Kembali', required=True)
    phone = fields.Char(string='Phone', required=True)

    durasiPinjaman = fields.Integer(
        string="Lama Peminjaman (hari)",
        compute='durasiHari',
        store=True
    )

    borrowed_book_ids = fields.Many2many(
        'library.book',
        'library_book_student_rel',
        'student_id',
        'book_id',
        string='Borrowed Books'
    )

    @api.depends('tanggalPinjam', 'tanggalKembali')
    def durasiHari(self):   
        for rec in self:
            if rec.tanggalPinjam and rec.tanggalKembali:
                if rec.tanggalPinjam > rec.tanggalKembali:
                    raise ValidationError("Tanggal kembali harus setelah tanggal pinjam.")
                rec.durasiPinjaman = (rec.tanggalKembali - rec.tanggalPinjam).days
            else:
                rec.durasiPinjaman = 0

    @api.model
    def create(self, vals):
        if vals.get('reference', 'Kosong') == 'Kosong':
            vals['reference'] = self.env['ir.sequence'].next_by_code('Student.Request') or '/'

        # Buat student record
        student = super().create(vals)

        # Kurangi stok buku yang dipinjam
        if vals.get('borrowed_book_ids'):
            commands = vals['borrowed_book_ids']
            book_ids = []

            for cmd in commands:
                if cmd[0] == 4:  # link ke buku existing
                    book_ids.append(cmd[1])
                elif cmd[0] == 6:  # replace semua
                    book_ids = cmd[2]

            books = self.env['library.book'].browse(book_ids)
            for book in books:
                if book.quantity <= 0:
                    raise ValidationError(f"Buku '{book.name}' tidak tersedia.")
                book.quantity -= 1

        return student
