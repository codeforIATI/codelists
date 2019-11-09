import xlsxwriter


class XLSXDictWriter:
    def __init__(self, filename, fieldnames, restval='', extrasaction='raise'):
        self.workbook = xlsxwriter.Workbook(filename)
        self.worksheet = self.workbook.add_worksheet()
        self.fieldnames = fieldnames
        self.restval = restval
        self.extrasaction = extrasaction
        self.rownum = 0

    def writeheader(self):
        for colnum, val in enumerate(self.fieldnames):
            self.worksheet.write(self.rownum, colnum, val)
        self.rownum += 1

    def writerow(self, row):
        if self.extrasaction == 'raise':
            for k in row.keys():
                if k not in self.fieldnames:
                    raise ValueError(k)
        for colnum, k in enumerate(self.fieldnames):
            self.worksheet.write(self.rownum, colnum, row.get(k, self.restval))
        self.rownum += 1

    def writerows(self, rows):
        for row in rows:
            self.writerow(row)

    def close(self):
        self.workbook.close()
