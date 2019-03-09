$("#comment-form").submit(function () {
    event.preventDefault()
    var report_id = $(".commentId").val()
    var form = $("#comment-form")

    $.ajax({
        'url': '/manager/report/'+report_id+'/newcomment',
        'type': 'POST',
        'data': form.serialize(),
        'dataType': 'json',
        'success': function (data) {
            alert(data['success'])
        },
    })

})


$("#farm-crop-form").submit(function () {
    event.preventDefault()
    var report_id = $(".farm-cropId").val()
    var form = $("#farm-crop-form")

    $.ajax({
        'url': '/manager/report/' + report_id + '/cropInfo',
        'type': 'POST',
        'data': form.serialize(),
        'dataType': 'json',
        'success': function (data) {
            alert(data['success'])

        },
    })

})


$("#farm-manage-form").submit(function () {
    event.preventDefault()
    var report_id = $(".manageId").val()
    var form = $("#farm-manage-form")

    $.ajax({
        'url': '/manager/report/' + report_id + '/cropManage',
        'type': 'POST',
        'data': form.serialize(),
        'dataType': 'json',
        'success': function (data) {
            alert(data['success'])

        },
    })

})


$("#farm-input-form").submit(function () {
    event.preventDefault()
    var report_id = $(".inputId").val()
    var form = $("#farm-input-form")

    $.ajax({
        'url': '/manager/report/' + report_id + '/cropInput',
        'type': 'POST',
        'data': form.serialize(),
        'dataType': 'json',
        'success': function (data) {
            alert(data['success'])

        },
    })

})

$("#farm-request-form").submit(function () {
    event.preventDefault()
    var report_id = $(".requestId").val()
    var form = $("#farm-request-form")

    $.ajax({
        'url': '/manager/report/' + report_id + '/newRequest',
        'type': 'POST',
        'data': form.serialize(),
        'dataType': 'json',
        'success': function (data) {
            alert(data['success'])

        },
        "error":function(err){
            console.log(err)
        }
    })

})