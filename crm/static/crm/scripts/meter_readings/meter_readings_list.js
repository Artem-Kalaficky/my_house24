// loading init data if exist
function init_data() {
    $('#input_number').attr('value', localStorage.input_number)
    $('#house option[value="' + localStorage.house + '"]').prop('selected', true)
    $('#section option[value="' + localStorage.section + '"]').prop('selected', true)
    $('#meter option[value="' + localStorage.meter + '"]').prop('selected', true)
    if (localStorage.number == 1) {
        $('#sort-number-span').html('№квартиры <i class="fa fa-sort-alpha-up"></i>')
    }
    if (localStorage.number == 0) {
        $('#sort-number-span').html('№квартиры <i class="fa fa-sort-alpha-down"></i>')
    }
}


//filter data by input
$('#house').change(function () {
    localStorage.house = $(this).val()
    $('#form').submit()
})

$('#section').change(function () {
    localStorage.section = $(this).val()
    $('#form').submit()
})

$('#input_number').blur(function () {
    localStorage.input_number = $(this).val()
    $('#form').submit()
})

$('#meter').change(function () {
    localStorage.meter = $(this).val()
    $('#form').submit()
})


// sort data by click
$('.sort-number').click(function () {
    if (localStorage.number == 1) {
        $('#sort-number-span').html('№квартиры <i class="fa fa-sort-alpha-down"></i>')
        localStorage.number = 0
        $('#filter-number').attr('value', 0)
        $('#form').submit()
    } else {
        $('#sort-number-span').html('№квартиры <i class="fa fa-sort-alpha-up"></i>')
        localStorage.number = 1
        $('#filter-number').attr('value', 1)
        $('#form').submit()
    }
})