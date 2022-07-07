//load data in filter form
$('#user').attr('value', localStorage.user)
$('#role option[value="' + localStorage.role + '"]').prop('selected', true)
$('#telephone').attr('value', localStorage.telephone)
$('#email').attr('value', localStorage.getItem('email'))
$('#status option[value="' + localStorage.status + '"]').prop('selected', true)


$('#user').blur(function () {
    localStorage.user = $(this).val()
    $('#form').submit()
})


$('#role').change(function () {
    localStorage.role = $(this).val()
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


$('#status').change(function () {
    localStorage.status = $(this).val()
    $('#form').submit()
})