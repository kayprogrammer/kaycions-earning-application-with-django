$(document).ready(function() {
    var loadForm = function () {
        var btn = $(this);
        $.ajax({
            url: btn.attr("data-url"),
            type: 'get',
            dataType: 'json',
            beforeSend: function (e) {
                $("#modal-task .modal-content").html("");
                $("#modal-task").modal("show");
            },
            success: function (data) {

                $("#modal-task .modal-content").html(data.html_form);
            }
        });
    };

    var saveForm = function () {
        var form = $(this);
        $.ajax({
          url: form.attr("action"),
          data: form.serialize(),
          type: form.attr("method"),
          dataType: 'json',
          beforeSend: function(){
            $('.spinner').show()
          },
          success: function (data) {
            data.preventDefault;
            if (data.form_is_valid) {
              Swal.fire({
                icon: 'success',
                title: 'Success',
                text: 'Task has been added',
                button :'Ok',
                timer : 2500
              });
              $("#task-table").html(data.html_task_list);
              $("#modal-task").modal("hide");
            }

            else {
              $("#modal-task .modal-content").html(data.html_form);
            }
          }
        });
        return false;
    };

    var updateForm = function () {
        var form = $(this);
        $.ajax({
          url: form.attr("action"),
          data: form.serialize(),
          type: form.attr("method"),
          dataType: 'json',
          beforeSend: function(){
            $('.spinner').show()
          },
          success: function (data) {
            data.preventDefault;
            if (data.form_is_valid) {
              Swal.fire({
                icon: 'success',
                title: 'Success',
                text: 'Task has been updated',
                button :'Ok',
                timer : 2500
              });
              $("#task-table").html(data.html_task_list);
              $("#modal-task").modal("hide");
            }

            else {
              $("#modal-task .modal-content").html(data.html_form);
            }
          }
        });
        return false;
    };

    var delForm = function () {
        var form = $(this);
        $.ajax({
          url: form.attr("action"),
          data: form.serialize(),
          type: form.attr("method"),
          dataType: 'json',
          beforeSend: function(){
            $('.spinner').show()
          },
          success: function (data) {
            data.preventDefault;
            if (data.form_is_valid) {
              Swal.fire({
                icon: 'success',
                title: 'Success',
                text: 'Task has been deleted',
                button :'Ok',
                timer : 2500
              });
              $("#task-table").html(data.html_task_list);
              $("#modal-task").modal("hide");
            }

            else {
              $("#modal-task .modal-content").html(data.html_form);
            }
          }
        });
        return false;
    };

    /* Binding */
    $(".js-create-task").click(loadForm);
    $("#modal-task").on("submit", ".js-task-create-form", saveForm);

    // Update task
    $("#task-table").on("click", ".js-update-task", loadForm);
    $("#modal-task").on("submit", ".js-task-update-form", updateForm);

    // Delete task
    $("#task-table").on("click", ".js-delete-task", loadForm);
    $("#modal-task").on("submit", ".js-task-delete-form", delForm);
});