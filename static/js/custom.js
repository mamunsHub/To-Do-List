function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
var csrftoken = getCookie('csrftoken')

function csrfSafeMethod(method) {
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

$.ajaxSetup({
    beforeSend: function(xhr, settings) {
        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});

function openDeleteModal(task_id){
    $('#dlt-btn').val(task_id)
    $('#delete').modal()
}

function deleteTask(project_id){
    task_id = Number($('#dlt-btn').val())
    $.ajax({
        type: 'POST',
        url: '/projects/',
        data: { 'task_id': task_id, 'action': 'delete' },
        success: function(json){
            if (json.hasOwnProperty('deleted'))
                location.reload()
        }
    })
}

function addProject(){
    title = $('#p-title').val()
    if(title=='')
        return;
    $.ajax({
        type: 'POST',
        url: "/projects/",
        data: { 'title': title },
        success: function(json){
            if (json.hasOwnProperty('added'))
                location.reload()
        }
    })
}

function completeTask(project_id, task_id, el){
    console.log(project_id)
    $(el.parentNode.parentNode).fadeOut()
    $.ajax({
        type: 'POST',
        data: {'project_id': Number(project_id), 'task_id': Number(task_id)},
        url: '/projects/'+project_id+'/tasks/'+task_id+'/',
        success: function(json){
            if (json.hasOwnProperty('task'))
                location.reload()
        }
    })
}