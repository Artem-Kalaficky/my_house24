// loading init data if exist
function init_data() {
    $('#id').attr('value', localStorage.id)
    $('#name').attr('value', localStorage.input_name)
    $('#telephone').attr('value', localStorage.telephone)
    $('#email').attr('value', localStorage.email)
    $('#apartment').attr('value', localStorage.apartment)
    $('#date').attr('value', localStorage.date)
    $('#status option[value="' + localStorage.status + '"]').prop('selected', true)
    $('#house option[value="' + localStorage.house + '"]').prop('selected', true)
    $('#debt option[value="' + localStorage.debt + '"]').prop('selected', true)
    if (localStorage.sort_date == 1) {
        $('#sort-date-span').html('Добавлен <i class="fa fa-sort-alpha-up"></i>')
    }
    if (localStorage.sort_date == 0) {
        $('#sort-date-span').html('Добавлен <i class="fa fa-sort-alpha-down"></i>')
    }
    if (localStorage.name == 1) {
        $('#sort-name-span').html('ФИО <i class="fa fa-sort-alpha-up"></i>')
    }
    if (localStorage.name == 0) {
        $('#sort-name-span').html('ФИО <i class="fa fa-sort-alpha-down"></i>')
    }
}

//filter data by input
$('#id').blur(function () {
    localStorage.id = $(this).val()
    $('#form').submit()
})

$('#name').blur(function () {
    localStorage.input_name = $(this).val()
    $('#form').submit()
})

$('#telephone').blur(function () {
    localStorage.telephone = $(this).val()
    $('#form').submit()
})

$('#email').blur(function () {
    localStorage.email = $(this).val()
    $('#form').submit()
})

$('#house').change(function () {
    localStorage.house = $(this).val()
    $('#form').submit()
})

$('#apartment').blur(function () {
    localStorage.apartment = $(this).val()
    $('#form').submit()
})

$('#date').blur(function () {
    localStorage.date = $(this).val()
    $('#form').submit()
})

$('#status').change(function () {
    localStorage.status = $(this).val()
    $('#form').submit()
})

$('#debt').change(function () {
    localStorage.debt = $(this).val()
    $('#form').submit()
})


// sort data by click
$('.sort-name').click(function () {
    if (localStorage.name == 1) {
        $('#sort-name-span').html('ФИО <i class="fa fa-sort-alpha-down"></i>')
        localStorage.name = 0
        $('#filter-name').attr('value', 0)
        $('#form').submit()
    } else {
        $('#sort-name-span').html('ФИО <i class="fa fa-sort-alpha-up"></i>')
        localStorage.name = 1
        $('#filter-name').attr('value', 1)
        $('#form').submit()
    }
})

$('.sort-date').click(function () {
    if (localStorage.sort_date == 1) {
        $('#sort-date-span').html('Добавлен <i class="fa fa-sort-alpha-down"></i>')
        localStorage.sort_date = 0
        $('#filter-date').attr('value', 0)
        $('#form').submit()
    } else {
        $('#sort-date-span').html('Добавлен <i class="fa fa-sort-alpha-up"></i>')
        localStorage.sort_date = 1
        $('#filter-date').attr('value', 1)
        $('#form').submit()
    }
})


// if debt YES or NO - get YES
$(function (){
    $('.debt').each(function (index, element){
        if ($(element).text().indexOf('Да') >= 0) {
            $(element).text('Да')
        }
        if ($(element).text().indexOf('Нет') >= 0) {
            $(element).text('Нет')
        }
    })
})


