// loading init data if exist
function init_data() {
    $('#number').attr('value', localStorage.number)
    $('#input_date').attr('value', localStorage.input_date)
    $('#personal_account').attr('value', localStorage.personal_account)
    $('#status option[value="' + localStorage.status + '"]').prop('selected', true)
    $('#apartment option[value="' + localStorage.apartment + '"]').prop('selected', true)
    $('#owner option[value="' + localStorage.owner + '"]').prop('selected', true)
    $('#is_held option[value="' + localStorage.is_held + '"]').prop('selected', true)
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

$('#apartment').change(function () {
    localStorage.apartment = $(this).val()
    $('#form').submit()
})

$('#owner').change(function () {
    localStorage.owner = $(this).val()
    $('#form').submit()
})

$('#is_held').change(function () {
    localStorage.is_held = $(this).val()
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







