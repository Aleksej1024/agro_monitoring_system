//var pathToBackend = window.location.hostname;

var pathToBackend = "192.168.2.2:8000";

var mode = 1;

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


function exitLK() {
	sessionStorage.clear();
	window.location.reload();
}

$(document).ready(function() {
	$('.dateMask').mask('9999-99-99');
	var hrefs = {
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
	if ($('#create_task_form').length) {
		getFieldList();
		getUsersList();
	}
    if ($('#tasksListTable').length) {
		getTasksTable();
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
			    location: $("#create_field_form input[name=location]").val(),
			    area: Number($("#create_field_form input[name=area]").val()),
			    status: Number($("#create_field_form input[name=status]").val()),
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
			url: 'http://' + pathToBackend + '/fields/' + $("#infoField_window input[name=id]").val(),
			method: 'PUT',
			dataType: 'json',
			contentType: "application/json",
			data: JSON.stringify({
			    location: $("#edit_field_form input[name=location]").val(),
			    area: Number($("#edit_field_form input[name=area]").val()),
			    status: Number($("#edit_field_form input[name=status]").val()),
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

$('#seazon_field_form').on('submit', function(e) {
	e.preventDefault();
	$.ajax({
			url: 'http://' + pathToBackend + '/seasons/',
			method: 'POST',
			dataType: 'json',
			contentType: "application/json",
			data: JSON.stringify({
			    year: Number($("#historyListTable input[name=year]").val()),
			    culture: $("#historyListTable input[name=culture]").val(),
			    start_date: $("#historyListTable input[name=start_date]").val(),
			    end_date: $("#historyListTable input[name=end_date]").val(),
			    field_id: Number($("#infoField_window input[name=id]").val()),
			    start_volume: Number($("#historyListTable input[name=start_volume]").val()),
			    end_volume: Number($("#historyListTable input[name=end_volume]").val()),
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
        url: 'http://' + pathToBackend + '/fields/' + Number($("#infoField_window input[name=id]").val()),
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
    $("#edit_field_form input[name=location]").val($("#row1_" + fid).text());
    $("#edit_field_form input[name=area]").val($("#row2_" + fid).text());
    getHistoryTable()
}

function add_seazon(element) {
    if (mode == 1) {
        $(element).text('Удалить сезон');
        $(element).addClass('activated');
        $("#historyListTable").append("<tr>"
        + "<td><input name = 'year'></td>"
        + "<td><input name = 'culture'></td>"
        + "<td><input name = 'start_date' type='date'></td>"
        + "<td><input name = 'end_date' type='date'></td>"
        + "<td><input style = 'width: 60px' name = 'start_volume' type='number' min='0'></td>"
        + "<td><input style = 'width: 60px' name = 'end_volume' type='number'</td>"
        + "<td><img src = 'design/ok.svg' style = 'width: 30px; cursor: pointer' onclick = '$(\"#seazon_field_form\").submit()'></td>"
        + "</tr>");
        mode = 0;
    }
    else {
         $("#historyListTable tr").eq($("#historyListTable tr").length - 1).remove();
         $(element).text('Добавить сезон');
         mode = 1;
    }
}

function getHistoryTable() {
	$.ajax({
			url: 'http://' + pathToBackend + '/seasons/',
			method: 'GET',
			dataType: 'json',
			headers: {
                Authorization : "Bearer " + sessionStorage.getItem("token"),
                accept : "application/json"
            },
			success: function(data) {
				if (data != undefined) {
					$('#history_table tbody').empty();
					for (var i = 0; i < data.length; i++) {
						var id = data[i]["id"];
						if (data[i]["field_id"] == Number($("#infoField_window input[name=id]").val())) {
                            $("#historyListTable").append("<tr>"
                                + "<td>" + data[i]["year"] + "</td>"
                                + "<td>" + data[i]["culture"] + "</td>"
                                + "<td>" + data[i]["start_date"] + "</td>"
                                + "<td>" + data[i]["end_date"] + "</td>"
                                + "<td style = 'width: 50px'>" + data[i]["start_volume"] + "</td>"
                                + "<td>" + data[i]["end_volume"] + "</td>"
                                + "<td></td>"
                                + "</tr>");
						}
					}
				}
			}
		});
}

function getUsersTable() {
	$.ajax({
			url: 'http://' + pathToBackend + '/users/',
			method: 'GET',
			dataType: 'json',
			headers: {
                Authorization : "Bearer " + sessionStorage.getItem("token"),
                accept : "application/json"
            },
			success: function(data) {
				if (data != undefined) {
					$('#users_table').empty();
					var role;
					for (var i = 0; i < data.length; i++) {
					    console.log(data[i]);
					    switch(data[i]["role"]) {
					        case 1:
					            role = "Главный агроном";
					            break;
					        case 2:
					            role = "Агроном";
					            break;
					        case 3:
					            role = "Лаборант";
					            break;
					    }

					    var del = "";
					    if (data[i]["id"] != getUser()["id"])
					        del = "<img onclick = 'delete_account(\""+data[i]["id"]+"\")' title = 'Удалить аккаунт' src = 'design/delete.svg'>";

                        var temp_password = random_number(1111,9999);

                        $("#users_table").append("<tr>"
                            + "<td>" + data[i]["fio"] + "</td>"
                            + "<td>" + data[i]["login"] + "</td>"
                            + "<td>" + role + "</td>"
                            + "<td>" + del + "</td>"
                            + "<td><img onclick = 'alert(\"Новый пароль для пользователя " + data[i]["fio"] + ": " + temp_password + "\"); change_account(\""+data[i]["id"]+"\", { password: \"" + temp_password + "\" })' title = 'Сбросить пароль' src = 'design/invite.svg'></td>"
                            + "</tr>");
						}
				}
			}
		});
}

function add_staff(element) {
    if (mode == 1) {
        $(element).text('Отменить добавление');
        $(element).addClass('activated');
        $("#users_table").append("<tr>"
        + "<td><input name = 'fio' placeholder='ФИО'></td>"
        + "<td><input name = 'login' placeholder='Логин'></td>"
        + "<td ><select style = 'width: 170px;' name = 'role'><option value = '2'>Агроном</option><option value = '3'>Лаборант</option></select></td>"
        + "<td><input name = 'password' placeholder='Пароль' value = '"+ random_number(1111,9999) + "'></td>"
        + "<td><img src = 'design/ok.svg' style = 'width: 30px; cursor: pointer' title = 'Подтвердить' onclick = '$(\"#new_user_field_form\").submit()'></td>"
        + "</tr>");
        mode = 0;
    }
    else {
         $("#users_table tr").eq($("#users_table tr").length - 1).remove();
         $(element).text('Добавить сотрудника');
         mode = 1;
    }
}

function random_number(min, max) {
      return Math.floor(Math.random() * (max - min) + min)
  }

$('#new_user_field_form').on('submit', function(e) {
	e.preventDefault();
	$.ajax({
			url: 'http://' + pathToBackend + '/users/',
			method: 'POST',
			dataType: 'json',
			contentType: "application/json",
			data: JSON.stringify({
			    fio: $("#users_table input[name=fio]").val(),
			    login: $("#users_table input[name=login]").val(),
			    role: $("#users_table select[name=role]").val(),
			    password: $("#users_table input[name=password]").val(),
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

function delete_account(id) {
    $.ajax({
        url: 'http://' + pathToBackend + '/users/' + id,
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

function change_account(id, data) {
    $.ajax({
        url: 'http://' + pathToBackend + '/users/' + id,
        method: 'PUT',
        dataType: 'json',
        contentType: "application/json",
        data: JSON.stringify(data),
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

$('#create_task_form').on('submit', function(e) {
	e.preventDefault();
	$.ajax({
			url: 'http://' + pathToBackend + '/tasks/',
			method: 'POST',
			dataType: 'json',
			contentType: "application/json",
			data: JSON.stringify({
			    field_id: Number($("#create_task_form select[name=field_id]").val()),
			    user_id: Number($("#create_task_form select[name=user_id]").val()),
			    description: $("#create_task_form input[name=description]").val(),
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

function getFieldList() {
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
					$('#fields_dir').empty();
					for (var i = 0; i < data.length; i++) {
					    if (data[i]["status"] == 1) {
                            $("#fields_dir").append("<option value=\"" + data[i]["id"] + "\">" + data[i]["location"] + "</option>");
                            $("#fields_dir_edit").append("<option value=\"" + data[i]["id"] + "\">" + data[i]["location"] + "</option>");
					    }
					}
				}
			}
		});
}
function getUsersList() {
	$.ajax({
			url: 'http://' + pathToBackend + '/users/',
			method: 'GET',
			dataType: 'json',
			headers: {
                Authorization : "Bearer " + sessionStorage.getItem("token"),
                accept : "application/json"
            },
			success: function(data) {
				if (data != undefined) {
					$('#employee_dir').empty();
					for (var i = 0; i < data.length; i++) {
                        $("#employee_dir").append("<option value=\"" + data[i]["id"] + "\">" + data[i]["fio"] + "</option>");
                        $("#employee_dir_edit").append("<option value=\"" + data[i]["id"] + "\">" + data[i]["fio"] + "</option>");
					}
				}
			}
		});

}

function get_assesment_info(task_id, field_id) {
	$.ajax({
		url: 'http://' + pathToBackend + '/assessments/',
		method: 'GET',
		headers: {
		Authorization : "Bearer " + sessionStorage.getItem("token"),
		accept : "application/json"
		},
		success:  function(data) {
            if (data != undefined) {
                for (var i = 0; i < data.length; i++) {
                    if (data[i]["field_id"] == field_id && data[i]["type"] == task_id ) {
                        $("#row4_" + task_id).html("<div style = 'color: green; font-weight: 700'>Оценено</div>");
                        break;
                    }
                    else {
                        $("#row4_" + task_id).html("<div style = 'color: red; font-weight: 700'>Не оценено</div>");
                    }
                }
            }
		}
	});
}


function getTasksTable() {
	$.ajax({
			url: 'http://' + pathToBackend + '/tasks/',
			method: 'GET',
			dataType: 'json',
			headers: {
                Authorization : "Bearer " + sessionStorage.getItem("token"),
                accept : "application/json"
            },
			success: function(data) {
				if (data != undefined) {
					$('#tasksListTable>tbody').empty();
					for (var i = 0; i < data.length; i++) {
						var id = data[i]["id"];
						get_assesment_info(data[i]["id"], data[i]["field_id"]);

						if (getUser()["role"] == 2 && data[i]["user_id"] == getUser()["id"]) {
                            $('#tasksListTable > tbody').append(
                                "<tr>"
                                + "<td id='row1_"+ data[i]["id"]+"'>" + data[i]["id"] + "</td>"
                                + "<td id='row2_"+ data[i]["id"]+"'>" + data[i]["description"] + "</td>"
                                + "<td id='row2_"+ data[i]["id"]+"'>" + get_user_info(data[i]["user_id"])["fio"] + "</td>"
                                + "<td id='row3_"+ data[i]["id"]+"'>" + get_field_info(data[i]["id"])["location"] + "</td>"
                                + "<td id='row4_"+ data[i]["id"]+"'></td>"
                               + "<td><img onclick = 'assesment(\"" + data[i]["id"] + "\", \"" + data[i]["field_id"] + "\"); modal_window_controller(\"infoTask_window\", 1, \"" + data[i]["id"] + "\")' title = ' Оценивание' src = 'design/services.svg'></td>"
                                + "<td><img onclick = 'results(\"" + data[i]["id"] + "\"); modal_window_controller(\"infoTask_window\", 1, \"" + data[i]["id"] + "\")' title = ' Результаты оценки' src = 'design/showed.svg'></td>"
                                + "</tr>"
                            );
						}
						else if (getUser()["role"] == 1 || getUser()["role"] == 3) {

						   $('#tasksListTable > tbody').append(
                                "<tr>"
                                + "<td id='row1_"+ data[i]["id"]+"'>" + data[i]["id"] + "</td>"
                                + "<td id='row2_"+ data[i]["id"]+"'>" + data[i]["description"] + "</td>"
                                + "<td id='row2_"+ data[i]["id"]+"'>" + get_user_info(data[i]["user_id"])["fio"] + "</td>"
                                + "<td id='row3_"+ data[i]["id"]+"'>" + get_field_info(data[i]["id"])["location"] + "</td>"
                                + "<td id='row4_"+ data[i]["id"]+"'></td>"
                               + "<td><img onclick = 'assesment(\"" + data[i]["id"] + "\", \"" + data[i]["field_id"] + "\"); modal_window_controller(\"infoTask_window\", 1, \"" + data[i]["id"] + "\")' title = ' Оценивание' src = 'design/services.svg'></td>"
                                + "<td><img onclick = 'results(\"" + data[i]["id"] + "\"); modal_window_controller(\"infoTask_window\", 1, \"" + data[i]["id"] + "\")' title = ' Результаты оценки' src = 'design/showed.svg'></td>"
                                + "</tr>"
                            );
						}
					}
				}
			}
		});
}

function get_field_info(id) {
    var f = null;
	$.ajax({
		'async': false,
		url: 'http://' + pathToBackend + '/fields/' + id,
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

function get_user_info(id) {
    var f = null;
	$.ajax({
		'async': false,
		url: 'http://' + pathToBackend + '/users/' + id,
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

var dt = new DataTransfer();

$('.input-file input[type=file]').on('change', function(){
	let $files_list = $(this).closest('.input-file').next();
	$files_list.empty();

	for(var i = 0; i < this.files.length; i++){
		let file = this.files.item(i);
		dt.items.add(file);

		let reader = new FileReader();
		reader.readAsDataURL(file);
		reader.onloadend = function(){
			let new_file_input = '<div class="input-file-list-item">' +
				'<img class="input-file-list-img" src="' + reader.result + '">' +
				'<span class="input-file-list-name">' + file.name + '</span>' +
				'<a href="#" onclick="removeFilesItem(this); return false;" class="input-file-list-remove">x</a>' +
			'</div>';
			$files_list.append(new_file_input);
		}
	};
	this.files = dt.files;
});

function removeFilesItem(target){
	let name = $(target).prev().text();
	let input = $(target).closest('.input-file-row').find('input[type=file]');
	$(target).closest('.input-file-list-item').remove();
	for(let i = 0; i < dt.items.length; i++){
		if(name === dt.items[i].getAsFile().name){
			dt.items.remove(i);
		}
	}
	input[0].files = dt.files;
}

function delete_task() {
    $.ajax({
        url: 'http://' + pathToBackend + '/tasks/' + Number($("#infoTask_window input[name=id]").val()),
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


function assesment(task_id, field_id) {
    var now = new Date();
    var dateStr = `${now.getFullYear()}-${String(now.getMonth() + 1).padStart(2, '0')}-${String(now.getDate()).padStart(2, '0')}`;
    $("#asses_field").val(field_id);
    $("#asses_date").val(dateStr);
    $("#asses_type").val(task_id);
}

$('#asses_task_form').on('submit', function(e) {
	e.preventDefault();
	$.ajax({
			url: 'http://' + pathToBackend + '/assessments/',
			method: 'POST',
			data: new FormData(this),
			headers: {
                Authorization : "Bearer " + sessionStorage.getItem("token")
            },
			success: function(data){
				window.location.reload();
			},
			error: function(data) {
				errorPushWindow(data);
			},
            cache: false,
            contentType: false,
            processData: false
		});
	return false;
});