from odoo import http
from odoo.http import content_disposition, request
import io
import xlsxwriter

class ReportExcelBook(http.Controller):
    @http.route(
        ['/report_Book/report_excel_book/<model("library.book"):data>'],
        type="http", auth="user", csrf=False
    )
    def get_report_excel_book(self, data=None, **args):
        # Buat response kosong
        output = io.BytesIO()
        workbook = xlsxwriter.Workbook(output, {'in_memory': True})
        worksheet = workbook.add_worksheet("Book Report")

        # Style
        header_style = workbook.add_format({
            'font_name': 'Times', 'bold': True,
            'border': 1, 'align': 'center'
        })
        text_style = workbook.add_format({
            'font_name': 'Times', 'border': 1
        })

        # Header kolom
        headers = ['Title', 'Author', 'Published Date', 'Quantity']
        for col, header in enumerate(headers):
            worksheet.write(0, col, header, header_style)

        # Isi data (karena <model()> mengirim single record, bungkus jadi iterable)
        books = data if isinstance(data, list) else [data]
        for row, book in enumerate(books, start=1):
            worksheet.write(row, 0, book.name or '', text_style)
            worksheet.write(row, 1, book.author or '', text_style)
            worksheet.write(row, 2, book.published_date.strftime('%Y-%m-%d') if book.published_date else '', text_style)
            worksheet.write(row, 3, book.quantity or 0, text_style)

        # Selesai
        workbook.close()
        output.seek(0)

        # Buat response
        response = request.make_response(
            output.read(),
            headers=[
                ('Content-Type', 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'),
                ('Content-Disposition', content_disposition('report_book.xlsx'))
            ]
        )
        return response
