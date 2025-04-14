$(document).ready(function() {
	$('.dateMask').mask('9999-99-99');
	var hrefs = {
		"Реестр полей" : "../fields",
		"Пользователи" : "../users",
		"Задачи" : "../tasks",
		};
	
	if ($('.username_header').length) $('.username_header').text(getUser()["fio"]);
	if ($('.nav').length) {
		for (var elem in hrefs) {
			$('.nav').append('<a href = ' + hrefs[elem] + '>' + elem + '</a>');
		}
	}
});