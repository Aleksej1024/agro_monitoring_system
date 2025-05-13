//var pathToBackend = window.location.hostname;

var pathToBackend = "192.168.2.2:8000";

$('#auth').on('submit', function(e) {
	e.preventDefault();
	$.ajax({
            url: 'http://' + pathToBackend + '/token',
		method: 'POST',
		dataType: 'json',
		contentType: "application/x-www-form-urlencoded",
		data: $(this).serialize(),
		success: function(data){
			$('.error_base').css('display','none');
			sessionStorage.setItem('token', data["access_token"]);
			window.location.href="/fields";
		},
		error: function(data){
			var error = data["responseJSON"]["detail"] || "Произошла ошибка при обращении к API";
			$('.error_base').text(error);
			$('.error_base').css('display','block');
		}
	});
	return false;
});

function getUser() {
	var f = null;
	$.ajax({
		'async': false,
		url: 'http://' + pathToBackend + '/users/me/',
		method: 'GET',
		headers: {
		Authorization : "Bearer " + sessionStorage.getItem("token"),
		accept : "application/json"
		},
		success: function(data){
			f = data;
		}
	});
	return f;
}