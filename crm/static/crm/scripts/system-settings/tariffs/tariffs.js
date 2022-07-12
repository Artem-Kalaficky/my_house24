// sort data by click
$('.sort').click(function () {
    if (localStorage.tariff == 1) {
        $('#sort-span').html('Название тарифа <i class="fa fa-sort-alpha-down"></i>')
        localStorage.tariff = 0
        $('#filter').attr('value', 0)
        $('#form').submit()
    } else {
        $('#sort-span').html('Название тарифа <i class="fa fa-sort-alpha-up"></i>')
        localStorage.tariff = 1
        $('#filter').attr('value', 1)
        $('#form').submit()
    }
})

// loading init data if exist
function init_data() {
    if (localStorage.tariff == 1) {
        $('#sort-span').html('Название тарифа <i class="fa fa-sort-alpha-up"></i>')
    }
    if (localStorage.tariff == 0) {
        $('#sort-span').html('Название тарифа <i class="fa fa-sort-alpha-down"></i>')
    }
}