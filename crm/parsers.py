import openpyxl
import pdfkit
from openpyxl.styles import Side, Border, NamedStyle
from xlsx2html import xlsx2html


def parse(path, data):
    book = openpyxl.load_workbook(path)
    sheet = book.active
    for row in range(1, 20):
        for i in range(1, 10):
            if sheet[row][i].value == 'payCompany':
                sheet[row][i].value = 'Мой Дом 24'
            if sheet[row][i].value == 'invoiceAddress':
                sheet[row][i].value = data['invoiceAddress']
            if sheet[row][i].value == 'total':
                sheet[row][i].value = data['total']
            if sheet[row][i].value == 'totalDebt':
                sheet[row][i].value = data['total']
            if sheet[row][i].value == 'accountBalance':
                sheet[row][i].value = data['accountBalance']
            if sheet[row][i].value == 'invoiceDate':
                sheet[row][i].value = data['invoiceDate']
            if sheet[row][i].value == 'invoiceMonth':
                sheet[row][i].value = data['invoiceMonth']
            if sheet[row][i].value == 'accountNumber':
                sheet[row][i].value = data['accountNumber']
            if sheet[row][i].value == 'invoiceNumber':
                sheet[row][i].value = data['invoiceNumber']
    row = 19
    for service in data['services']:
        sheet[row][0].value = service['service']
        sheet[row][2].value = service['tariff']
        sheet[row][4].value = service['unit']
        sheet[row][6].value = service['expense']
        sheet[row][8].value = service['full_cost']
        row += 1
    sheet[row][6].value = 'РАЗОМ:'
    sheet[row][8].value = data['total']

    # styles
    cols = 10
    line = Side(style='thin', color='000000')
    border = Border(top=line, bottom=line, left=line, right=line)
    style = NamedStyle(name='style', border=border)
    for r in range(19, row + 1):
        for c in range(1, cols + 1):
            sheet.cell(r, c).style = style

    temp_path = 'media/temp_files/invoice.xlsx'
    book.save(temp_path)
    return temp_path
