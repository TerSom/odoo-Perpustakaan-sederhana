# -*- coding: utf-8 -*-
{
    'name': "perpustakaan_custom",

    'summary': "Short (1 phrase/line) summary of the module's purpose",

    'description': """
Long description of module's purpose
    """,

    'author': "My Company",
    'website': "https://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','web'],

    # always loaded
    'data': [
        'security/ir.model.access.csv',
        'views/book_views.xml',
        'views/student_views.xml',
        'views/Teacher_views.xml',
        'report/perpustakaan_student_report_template.xml',
        'report/perpustakaan_student_report_views.xml',
        "data/ir_sequence_Student.xml",
        'data/ir_sequence_Teacher.xml',
        'report/perpustakaan_teacher_report_template.xml',
        'report/perpustakaan_teacher_report_views.xml',
        'data/email_template_student.xml'
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}

