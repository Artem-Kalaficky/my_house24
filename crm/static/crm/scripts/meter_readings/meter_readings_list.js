// loading init data if exist
function init_data() {
    $('#input_number').attr('value', localStorage.input_number)
    $('#input_house option[value="' + localStorage.input_house + '"]').prop('selected', true)
    $('#input_section option[value="' + localStorage.input_section + '"]').prop('selected', true)
    $('#input_floor option[value="' + localStorage.input_floor + '"]').prop('selected', true)
    $('#input_owner option[value="' + localStorage.input_owner + '"]').prop('selected', true)
    $('#debt option[value="' + localStorage.debt + '"]').prop('selected', true)
    if (localStorage.number == 1) {
        $('#sort-number-span').html('№квартиры <i class="fa fa-sort-alpha-up"></i>')
    }
    if (localStorage.number == 0) {
        $('#sort-number-span').html('№квартиры <i class="fa fa-sort-alpha-down"></i>')
    }
    if (localStorage.house == 1) {
        $('#sort-house-span').html('Дом <i class="fa fa-sort-alpha-up"></i>')
    }
    if (localStorage.house == 0) {
        $('#sort-house-span').html('Дом <i class="fa fa-sort-alpha-down"></i>')
    }
    if (localStorage.section == 1) {
        $('#sort-section-span').html('Секция <i class="fa fa-sort-alpha-up"></i>')
    }
    if (localStorage.section == 0) {
        $('#sort-section-span').html('Секция <i class="fa fa-sort-alpha-down"></i>')
    }
    if (localStorage.floor == 1) {
        $('#sort-floor-span').html('Этаж <i class="fa fa-sort-alpha-up"></i>')
    }
    if (localStorage.floor == 0) {
        $('#sort-floor-span').html('Этаж <i class="fa fa-sort-alpha-down"></i>')
    }
    if (localStorage.owner == 1) {
        $('#sort-owner-span').html('Владелец <i class="fa fa-sort-alpha-up"></i>')
    }
    if (localStorage.owner == 0) {
        $('#sort-owner-span').html('Владелец <i class="fa fa-sort-alpha-down"></i>')
    }
}


//filter data by input
$('#input_number').blur(function () {
    localStorage.input_number = $(this).val()
    $('#form').submit()
})

$('#input_house').change(function () {
    localStorage.input_house = $(this).val()
    $('#form').submit()
})

$('#input_section').change(function () {
    localStorage.input_section = $(this).val()
    $('#form').submit()
})

$('#input_floor').change(function () {
    localStorage.input_floor = $(this).val()
    $('#form').submit()
})

$('#input_owner').change(function () {
    localStorage.input_owner = $(this).val()
    $('#form').submit()
})

$('#debt').change(function () {
    localStorage.debt = $(this).val()
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