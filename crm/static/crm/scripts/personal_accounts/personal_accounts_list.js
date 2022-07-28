// loading init data if exist
function init_data() {
    $('#number').attr('value', localStorage.number)
    $('#apartment').attr('value', localStorage.apartment)
    $('#status option[value="' + localStorage.status + '"]').prop('selected', true)
    $('#house option[value="' + localStorage.house + '"]').prop('selected', true)
    $('#section option[value="' + localStorage.section + '"]').prop('selected', true)
    $('#owner option[value="' + localStorage.owner + '"]').prop('selected', true)
    $('#debt option[value="' + localStorage.debt + '"]').prop('selected', true)
}

//filter data by input
$('#number').blur(function () {
    localStorage.number = $(this).val()
    $('#form').submit()
})

$('#status').change(function () {
    localStorage.status = $(this).val()
    $('#form').submit()
})

$('#apartment').blur(function () {
    localStorage.apartment = $(this).val()
    $('#form').submit()
})

$('#house').change(function () {
    localStorage.house = $(this).val()
    $('#form').submit()
})

$('#section').change(function () {
    localStorage.section = $(this).val()
    $('#form').submit()
})

$('#owner').change(function () {
    localStorage.owner = $(this).val()
    $('#form').submit()
})

$('#debt').change(function () {
    localStorage.debt = $(this).val()
    $('#form').submit()
})


//convertor HTML-table in Excel file (+download)
let tableToExcel = (function() {
  let uri = 'data:application/vnd.ms-excel;base64,',
    template = '<html xmlns:o="urn:schemas-microsoft-com:office:office" xmlns:x="urn:schemas-microsoft-com:office:excel" xmlns="http://www.w3.org/TR/REC-html40"><head><!--[if gte mso 9]><xml><x:ExcelWorkbook><x:ExcelWorksheets><x:ExcelWorksheet><x:Name>{worksheet}</x:Name><x:WorksheetOptions><x:DisplayGridlines/></x:WorksheetOptions></x:ExcelWorksheet></x:ExcelWorksheets></x:ExcelWorkbook></xml><![endif]--></head><body><table>{table}</table></body></html>',
    base64 = function(s) {
      return window.btoa(unescape(encodeURIComponent(s)))
    },
    format = function(s, c) {
      return s.replace(/{(\w+)}/g, function(m, p) {
        return c[p];
      })
    }
  return function(table, name) {
    if (!table.nodeType) table = document.getElementById(table)
    let ctx = {
      worksheet: name || 'Worksheet',
      table: table.innerHTML
    }
    window.location.href = uri + base64(format(template, ctx))
  }
})()





