// generate and show passwords
$(document).ready(function() {
	function str_rand() {
		var result       = '';
		var words        = '0123456789qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM';
		var max_position = words.length - 1;
			for( i = 0; i < 10; ++i ) {
				position = Math.floor ( Math.random() * max_position );
				result = result + words.substring(position, position + 1);
			}
		return result;
	}
	$('.showPassword').click(function(){
		var inputPsw = $('#id_password1');
		if (inputPsw.attr('type') == 'password') {
			document.getElementById('id_password1').setAttribute('type', 'text');
			document.getElementById('id_password2').setAttribute('type', 'text');
		} else {
			document.getElementById('id_password1').setAttribute('type', 'password');
			document.getElementById('id_password2').setAttribute('type', 'password');
		}
	});
	$('.generatePassword').click(function() {
		document.getElementById('id_password1').setAttribute('type', 'text');
		$('#id_password1').attr('value', str_rand());
		$('#id_password2').attr('value', $('#id_password1').val())
		document.getElementById('id_password1').setAttribute('type', 'password');
		document.getElementById('id_password2').setAttribute('type', 'password');
	});
});


// Mask for telephone
$(function(){
  $("#id_telephone, #id_viber").mask("+380(099) 999-99-99");
});

// preview avatar
$('input[type=file]').change(function (event){
	console.log('ghbdtn')
    $('img[id="' + this.id + '"]').attr('src', URL.createObjectURL(event.target.files[0]))
})