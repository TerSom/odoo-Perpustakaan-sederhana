from odoo import models, fields, api
from odoo.exceptions import ValidationError

class LibraryTeacher(models.Model):
    _name = 'library.teacher'
    _description = 'Teacher Master'
    _rec_name = 'reference'

    reference = fields.Char(string='No', readonly=True, default="Kosong", copy=False)
    name = fields.Char(string='Name', required=True)
    nip = fields.Char(string='NIP', required=True)
    tanggalPinjam = fields.Date(string='Tanggal Pinjam', required=True)
    tanggalKembali = fields.Date(string='Tanggal Kembali', required=True)
    phoneTeacher = fields.Char(string='Phone', required=True)

    durasiPinjaman = fields.Integer(
        string="Lama Peminjaman (hari)",
        compute='durasiHari',
        store=True
    )

    borrowed_book_ids = fields.Many2many(
        'library.book',
        'library_book_teacher_rel',
        'teacher_id',
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
            vals['reference'] = self.env['ir.sequence'].next_by_code('Teacher.Request') or '/'

        teacher = super().create(vals)

        # Kurangi stok buku yang dipinjam
        if vals.get('borrowed_book_ids'):
            book_ids = self._extract_book_ids(vals['borrowed_book_ids'])
            self._update_book_stock(book_ids, decrease=True)

        return teacher

    def write(self, vals):
        for rec in self:
            old_books = rec.borrowed_book_ids

            res = super(LibraryTeacher, rec).write(vals)

            if 'borrowed_book_ids' in vals:
                new_books = rec.borrowed_book_ids

                removed_books = old_books - new_books
                added_books = new_books - old_books

                # Tambah stok untuk buku yang dihapus
                for book in removed_books:
                    book.quantity += 1

                # Kurangi stok untuk buku yang ditambahkan
                for book in added_books:
                    if book.quantity <= 0:
                        raise ValidationError(f"Buku '{book.name}' tidak tersedia.")
                    book.quantity -= 1

        return True

    def _extract_book_ids(self, commands):
        """
        Ekstrak ID buku dari M2M command format
        """
        book_ids = []
        for cmd in commands:
            if cmd[0] == 4:
                book_ids.append(cmd[1])
            elif cmd[0] == 6:
                book_ids = cmd[2]
        return book_ids

    def _update_book_stock(self, book_ids, decrease=False):
        """
        Tambah atau kurangi stok buku
        """
        books = self.env['library.book'].browse(book_ids)
        for book in books:
            if decrease:
                if book.quantity <= 0:
                    raise ValidationError(f"Buku '{book.name}' tidak tersedia.")
                book.quantity -= 1
            else:
                book.quantity += 1
