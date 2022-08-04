// loading init data if exist
function init_data() {
    $('#number').attr('value', localStorage.number)
    $('#input_date').attr('value', localStorage.input_date)
    $('#personal_account').attr('value', localStorage.personal_account)
    $('#status option[value="' + localStorage.status + '"]').prop('selected', true)
    $('#type option[value="' + localStorage.type + '"]').prop('selected', true)
    $('#owner option[value="' + localStorage.owner + '"]').prop('selected', true)
    $('#income option[value="' + localStorage.income + '"]').prop('selected', true)
    if (localStorage.date == 1) {
        $('#sort-date-span').html('Дата <i class="fa fa-sort-alpha-up"></i>')
    }
    if (localStorage.date == 0) {
        $('#sort-date-span').html('Дата <i class="fa fa-sort-alpha-down"></i>')
    }
}

//filter data by input
$('#number').blur(function () {
    localStorage.number = $(this).val()
    $('#form').submit()
})

$(function (){
    $('.applyBtn').click(function () {
        setTimeout(function () {
            localStorage.input_date = $('#input_date').val()
            $('#form').submit()
        }, 100)
    })
})

$('#status').change(function () {
    localStorage.status = $(this).val()
    $('#form').submit()
})

$('#type').change(function () {
    localStorage.type = $(this).val()
    $('#form').submit()
})

$('#owner').change(function () {
    localStorage.owner = $(this).val()
    $('#form').submit()
})

$('#personal_account').blur(function () {
    localStorage.personal_account = $(this).val()
    $('#form').submit()
})

$('#income').change(function () {
    localStorage.income = $(this).val()
    $('#form').submit()
})


// ordering filter
$('.sort-date').click(function () {
    if (localStorage.date == 1) {
        $('#sort-date-span').html('Дата <i class="fa fa-sort-alpha-down"></i>')
        localStorage.date = 0
        $('#filter-date').attr('value', 0)
        $('#form').submit()
    } else {
        $('#sort-date-span').html('Дата <i class="fa fa-sort-alpha-up"></i>')
        localStorage.date = 1
        $('#filter-date').attr('value', 1)
        $('#form').submit()
    }
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





