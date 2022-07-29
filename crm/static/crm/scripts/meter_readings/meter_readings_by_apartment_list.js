// loading init data if exist
function init_data() {
    $('#number').attr('value', localStorage.number)
    $('#input_date').attr('value', localStorage.input_date)
    $('#status option[value="' + localStorage.status + '"]').prop('selected', true)
    $('#meter option[value="' + localStorage.meter + '"]').prop('selected', true)
    if (localStorage.date == 1) {
        $('#sort-date-span').html('Дата <i class="fa fa-sort-alpha-up"></i>')
        $('#sort-month-span').html('Месяц <i class="fa fa-sort-alpha-up"></i>')
    }
    if (localStorage.date == 0) {
        $('#sort-date-span').html('Дата <i class="fa fa-sort-alpha-down"></i>')
        $('#sort-month-span').html('Месяц <i class="fa fa-sort-alpha-down"></i>')
    }
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

$(function (){
    $('.applyBtn').click(function () {
        setTimeout(function () {
            localStorage.input_date = $('#input_date').val()
            $('#form').submit()
        }, 100)
    })
})

$('#meter').change(function () {
    localStorage.meter = $(this).val()
    $('#form').submit()
})


// sort data by click
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

$('.sort-month').click(function () {
    if (localStorage.date == 1) {
        $('#sort-mouth-span').html('Месяц <i class="fa fa-sort-alpha-down"></i>')
        localStorage.date = 0
        $('#filter-date').attr('value', 0)
        $('#form').submit()
    } else {
        $('#sort-mouth-span').html('Месяц <i class="fa fa-sort-alpha-up"></i>')
        localStorage.date = 1
        $('#filter-date').attr('value', 1)
        $('#form').submit()
    }
})