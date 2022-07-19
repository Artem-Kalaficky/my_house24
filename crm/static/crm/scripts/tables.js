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
}

