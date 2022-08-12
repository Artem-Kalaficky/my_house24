import openpyxl


def parse(path, data):
    book = openpyxl.load_workbook(path)
    sheet = book.active
    for row in range(1, 20):
        for i in range(1, 10):
            if sheet[row][i].value == 'payCompany':
                sheet[row][i].value = 'Мой Дом 24'
            if sheet[row][i].value == 'invoiceAddress':
                sheet[row][i].value = data['invoiceAddress']
            if sheet[row][i].value == ('total' or 'totalDebt'):
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
    sheet[row+1][6].value = 'РАЗОМ:'
    sheet[row+1][8].value = data['total']
    book.save(path)
