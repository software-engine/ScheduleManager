/**
 * Created by specific on 2016/12/1.
 */

$(document).ready(function () {
    $('#select-all').click(function () {
        if ($(this).prop('checked')) {
            $('.op_check').prop('checked', true);
        } else {
            $('.op_check').prop('checked', false);
        }
    });
});

function addActivity(id) {
    addFormSubmit(id)
}

function addFormSubmit(id) {
    $('#addForm' + id).submit()
}

$(document).ready(function () {
    $('#addActivities').click(function () {
        if ($('.op_check').filter(':checked').size() > 0) {
            var messages = [];
            $('.op_check:checked').each(function () {
                messages.push($(this).val());
            });
            var messagesJson = JSON.stringify(messages);
            $('#activity_ids').val(messagesJson);
            $('#addActivitiesForm').submit()
        } else {
            $('#selectActivityFormModal').modal()
        }
    });
});
