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
}

