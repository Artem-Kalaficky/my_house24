// loading init data if exist
function init_data() {
    $('#input_number').attr('value', localStorage.input_number)
    $('#input_date').attr('value', localStorage.input_date)
    $('#description').attr('value', localStorage.description)
    $('#apartment').attr('value', localStorage.apartment)
    $('#telephone').attr('value', localStorage.telephone)
    $('#input_type option[value="' + localStorage.input_type + '"]').prop('selected', true)
    $('#owner option[value="' + localStorage.owner + '"]').prop('selected', true)
    $('#master option[value="' + localStorage.master + '"]').prop('selected', true)
    $('#status option[value="' + localStorage.status + '"]').prop('selected', true)
    if (localStorage.number == 1) {
        $('#sort-number-span').html('№ <i class="fa fa-sort-alpha-up"></i>')
    }
    if (localStorage.number == 0) {
        $('#sort-number-span').html('№ <i class="fa fa-sort-alpha-down"></i>')
    }
    if (localStorage.date == 1) {
        $('#sort-date-span').html('Удобное время <i class="fa fa-sort-alpha-up"></i>')
    }
    if (localStorage.date == 0) {
        $('#sort-date-span').html('Удобное время <i class="fa fa-sort-alpha-down"></i>')
    }
    if (localStorage.type == 1) {
        $('#sort-master-span').html('Тип мастера <i class="fa fa-sort-alpha-up"></i>')
    }
    if (localStorage.type == 0) {
        $('#sort-master-span').html('Тип мастера <i class="fa fa-sort-alpha-down"></i>')
    }
}


//filter data by input
$('#input_number').blur(function () {
    localStorage.input_number = $(this).val()
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

$('#input_type').change(function () {
    localStorage.input_type = $(this).val()
    $('#form').submit()
})

$('#description').blur(function () {
    localStorage.description = $(this).val()
    $('#form').submit()
})

$('#apartment').blur(function () {
    localStorage.apartment = $(this).val()
    $('#form').submit()
})

$('#owner').change(function () {
    localStorage.owner = $(this).val()
    $('#form').submit()
})

$('#telephone').blur(function () {
    localStorage.telephone = $(this).val()
    $('#form').submit()
})

$('#master').change(function () {
    localStorage.master = $(this).val()
    $('#form').submit()
})

$('#status').change(function () {
    localStorage.status = $(this).val()
    $('#form').submit()
})


// sort data by click
$('.sort-number').click(function () {
    if (localStorage.number == 1) {
        $('#sort-number-span').html('№ <i class="fa fa-sort-alpha-down"></i>')
        localStorage.number = 0
        $('#filter-number').attr('value', 0)
        $('#form').submit()
    } else {
        $('#sort-number-span').html('№ <i class="fa fa-sort-alpha-up"></i>')
        localStorage.number = 1
        $('#filter-number').attr('value', 1)
        $('#form').submit()
    }
})

$('.sort-date').click(function () {
    if (localStorage.date == 1) {
        $('#sort-date-span').html('Удобное время <i class="fa fa-sort-alpha-down"></i>')
        localStorage.date = 0
        $('#filter-date').attr('value', 0)
        $('#form').submit()
    } else {
        $('#sort-date-span').html('Удобное время <i class="fa fa-sort-alpha-up"></i>')
        localStorage.date = 1
        $('#filter-date').attr('value', 1)
        $('#form').submit()
    }
})

$('.sort-master').click(function () {
    if (localStorage.type == 1) {
        $('#sort-master-span').html('Тип мастера <i class="fa fa-sort-alpha-down"></i>')
        localStorage.type = 0
        $('#filter-master').attr('value', 0)
        $('#form').submit()
    } else {
        $('#sort-master-span').html('Тип мастера <i class="fa fa-sort-alpha-up"></i>')
        localStorage.type = 1
        $('#filter-master').attr('value', 1)
        $('#form').submit()
    }
})