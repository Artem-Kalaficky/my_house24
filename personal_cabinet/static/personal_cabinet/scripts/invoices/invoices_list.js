// loading init data if exist
function init_data() {
    $('#input_date').attr('value', localStorage.input_date)
    $('#status option[value="' + localStorage.status + '"]').prop('selected', true)
    if (localStorage.date == 1) {
        $('#sort-date-span').html('Дата <i class="fa fa-sort-alpha-up"></i>')
    }
    if (localStorage.date == 0) {
        $('#sort-date-span').html('Дата <i class="fa fa-sort-alpha-down"></i>')
    }
}

//filter data by input
$('#status').change(function () {
    localStorage.status = $(this).val()
    $('#form').submit()
})

$('#input_date').blur(function () {
    localStorage.input_date = $(this).val()
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








