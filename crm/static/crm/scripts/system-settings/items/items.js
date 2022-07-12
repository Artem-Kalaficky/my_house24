//sort data by click
$('.sort').click(function () {
    if (localStorage.income_expense == 1) {
        $('#sort-span').html('Приход/Расход <i class="fa fa-sort-alpha-down"></i>')
        localStorage.income_expense = 0
        $('#filter').attr('value', 0)
        $('#form').submit()
    } else {
        $('#sort-span').html('Приход/Расход <i class="fa fa-sort-alpha-up"></i>')
        localStorage.income_expense = 1
        $('#filter').attr('value', 1)
        $('#form').submit()
    }
})

// loading init data if exist
function init_data() {
    if (localStorage.income_expense == 1) {
        $('#sort-span').html('Приход/Расход <i class="fa fa-sort-alpha-up"></i>')
    }
    if (localStorage.income_expense == 0) {
        $('#sort-span').html('Приход/Расход <i class="fa fa-sort-alpha-down"></i>')
    }
}