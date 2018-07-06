var login = $("#login");
var register = $("#register");
var button_login = $("#toggle-login");
var button_register = $("#toggle-register");
var box = $(".box");

$('#signup_assword, #confirm_password').on('keyup', function () {
  if ($('#signup_password').val() == $('#confirm_password').val()) {
    $('#message').html('Matching').css('color', 'green');
		$('#create_acc').prop( "disabled",false );
  }
	 else{
    $('#message').html('Not Matching').css('color', 'red');
		$('#create_acc').prop( "disabled", true );}
});

$(function() {
	register.hide();

	button_register.click(function() {
		login.slideUp(1000);
		register.slideDown(1000);
	});
	button_login.click(function() {
		register.slideUp(1000);
		login.slideDown(1000);
	});
});
