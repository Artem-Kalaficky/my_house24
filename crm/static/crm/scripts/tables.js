// link on all strind(td)
$('td[data-href]').on("click", function() {
    document.location = $(this).data('href');
});


// clear filter data in local storage
function clear() {
    delete localStorage.user
    delete localStorage.role
    delete localStorage.telephone
    delete localStorage.email
    delete localStorage.status
    delete localStorage.income_expense
    delete localStorage.tariff
    delete localStorage.name
    delete localStorage.address
    delete localStorage.input_name
    delete localStorage.input_address
    delete localStorage.id
    delete localStorage.date
    delete localStorage.sort_date
    delete localStorage.number
    delete localStorage.input_number
    delete localStorage.apartment
    delete localStorage.house
    delete localStorage.input_house
    delete localStorage.section
    delete localStorage.input_section
    delete localStorage.floor
    delete localStorage.input_floor
    delete localStorage.owner
    delete localStorage.input_owner
    delete localStorage.debt
    delete localStorage.meter
    delete localStorage.input_date
    delete localStorage.type
    delete localStorage.input_type
    delete localStorage.description
    delete localStorage.master
    delete localStorage.personal_account
    delete localStorage.income
    delete localStorage.is_held
}

