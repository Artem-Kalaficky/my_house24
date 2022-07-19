// loading init data if exist
function init_data() {
    $('#name').attr('value', localStorage.input_name)
    $('#address').attr('value', localStorage.input_address)
    if (localStorage.address == 1) {
        $('#sort-address-span').html('Адрес <i class="fa fa-sort-alpha-up"></i>')
    }
    if (localStorage.address == 0) {
        $('#sort-address-span').html('Адрес <i class="fa fa-sort-alpha-down"></i>')
    }
    if (localStorage.name == 1) {
        $('#sort-name-span').html('Название <i class="fa fa-sort-alpha-up"></i>')
    }
    if (localStorage.name == 0) {
        $('#sort-name-span').html('Название <i class="fa fa-sort-alpha-down"></i>')
    }
}


// sort data by click
$('.sort-name').click(function () {
    if (localStorage.name == 1) {
        $('#sort-name-span').html('Название <i class="fa fa-sort-alpha-down"></i>')
        localStorage.name = 0
        $('#filter-name').attr('value', 0)
        $('#form').submit()
    } else {
        $('#sort-name-span').html('Название <i class="fa fa-sort-alpha-up"></i>')
        localStorage.name = 1
        $('#filter-name').attr('value', 1)
        $('#form').submit()
    }
})

$('.sort-address').click(function () {
    if (localStorage.address == 1) {
        $('#sort-address-span').html('Адрес <i class="fa fa-sort-alpha-down"></i>')
        localStorage.address = 0
        $('#filter-address').attr('value', 0)
        $('#form').submit()
    } else {
        $('#sort-address-span').html('Адрес <i class="fa fa-sort-alpha-up"></i>')
        localStorage.address = 1
        $('#filter-address').attr('value', 1)
        $('#form').submit()
    }
})


//filter data by input
$('#name').blur(function () {
    localStorage.input_name = $(this).val()
    $('#form').submit()
})


$('#address').blur(function () {
    localStorage.input_address = $(this).val()
    $('#form').submit()
})

