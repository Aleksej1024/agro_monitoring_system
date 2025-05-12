//var pathToBackend = window.location.hostname;

var pathToBackend = "192.168.2.2:8000";

function errorPushWindow(data) {
    alert("Произошла ошибка");
}
function modal_window_controller(elem, action, row=null) {
	if (action == 1) {
		$('.modal_wrap_lk').css("display", "block");
		$('#' + elem).css("display", "block");
		if ($('#' + elem + ' input[name=id]').length) {
			$('#' + elem + ' input[name=id]').val(row);
		}
	}
	else {
		$('.modal_wrap_lk').css("display", "none");
		$('#' + elem).css("display", "none");
	}
}


function getSeazonsTable() {
	$.ajax({
			url: 'http://' + pathToBackend + '/fields/',
			method: 'GET',
			dataType: 'json',
			headers: {
                Authorization : "Bearer " + sessionStorage.getItem("token"),
                accept : "application/json"
            },
			success: function(data) {
				if (data != undefined) {
					$('#seazonsListTable>tbody').empty();
					for (var i = 0; i < data.length; i++) {
						var id = data[i]["id"];
						if (data[i]["status"] != 0) {
                            $('#seazonsListTable>tbody').append(
                                "<tr><td>" + id + "</td>"
                                + "<td id='row1_"+ data[i]["id"]+"'>" + data[i]["location"] + "</td>"
                                + "<td id='row2_"+ data[i]["id"]+"'>" + data[i]["area"] + "</td>"
                                + "<td><img onclick = 'field_card_window(\"" + data[i]["id"] + "\"); modal_window_controller(\"infoField_window\", 1, \"" + data[i]["id"] + "\")' title = ' Карта поля' src = 'design/services.svg'></td>"
                                + "</tr>"
                            );
						}
					}
				}
			}
		});
}

$(document).ready(function() {
	$('.dateMask').mask('9999-99-99');
	var hrefs = {
		"Пользователи" : "../users",
		"Задачи" : "../tasks",
		"Реестр полей и сезоны" : "../fields",
		};
	
	if ($('.username_header').length) $('.username_header').text(getUser()["fio"]);
	if ($('.nav').length) {
		for (var elem in hrefs) {
			$('.nav').append('<a href = ' + hrefs[elem] + '>' + elem + '</a>');
		}
	}

	if ($('#seazonsListTable').length) {
		getSeazonsTable();
	}
});

$('#create_field_form').on('submit', function(e) {
	e.preventDefault();
	$.ajax({
			url: 'http://' + pathToBackend + '/fields/',
			method: 'POST',
			dataType: 'json',
			contentType: "application/json",
			data: JSON.stringify({
			    location: $("#create_field_form [name=location]").val(),
			    area: Number($("#create_field_form [name=area]").val()),
			    status: Number($("#create_field_form [name=status]").val()),
			}),
			headers: {
                Authorization : "Bearer " + sessionStorage.getItem("token")
            },
			success: function(data){
				window.location.reload();
			},
			error: function(data) {
				errorPushWindow(data);
			}
		});
	return false;
});

$('#edit_field_form').on('submit', function(e) {
	e.preventDefault();
	$.ajax({
			url: 'http://' + pathToBackend + '/fields/' + $("#infoField_window [name=id]").val(),
			method: 'PUT',
			dataType: 'json',
			contentType: "application/json",
			data: JSON.stringify({
			    location: $("#edit_field_form [name=location]").val(),
			    area: Number($("#edit_field_form [name=area]").val()),
			    status: Number($("#edit_field_form [name=status]").val()),
			}),
			headers: {
                Authorization : "Bearer " + sessionStorage.getItem("token")
            },
			success: function(data){
				window.location.reload();
			},
			error: function(data) {
				errorPushWindow(data);
			}
		});
	return false;
});


function delete_field() {
    $.ajax({
        url: 'http://' + pathToBackend + '/fields/' + Number($("#infoField_window [name=id]").val()),
        method: 'DELETE',
        dataType: 'json',
        contentType: "application/json",
        headers: {
            Authorization : "Bearer " + sessionStorage.getItem("token")
        },
        success: function(data){
            window.location.reload();
        },
        error: function(data) {
            errorPushWindow(data);
        }
    });
}

function field_card_window(fid) {
    $("#card_name").text("Карточка поля c ID #" + fid);
    $("#edit_field_form [name=location]").val($("#row1_" + fid).text());
    $("#edit_field_form [name=area]").val($("#row2_" + fid).text());
}