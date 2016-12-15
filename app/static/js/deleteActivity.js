/**
 * Created by specific on 2016/12/9.
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

function deleteActivity(id) {
    $('#deleteActivityConfirm').click(function () {
        deleteActivityFormSubmit(id);
    });
    $('#deleteActivityModal').modal();
}
function deleteActivityFormSubmit(id) {
    $('#deleteActivityForm' + id).submit();
}

$(document).ready(function () {
    $('#deleteActivitiesConfirm').click(function () {
        $('#deleteActivitiesForm').submit();
    });

    $('#deleteActivities').click(function () {
        if ($('.op_check').filter(':checked').size() > 0) {
            var activities_id = [];
            $('.op_check:checked').each(function () {
                activities_id.push($(this).val());
            });
            var activities_id_json = JSON.stringify(activities_id);
            $('#activity_ids').val(activities_id_json);
            $('#deleteActivitiesModal').modal();
        } else {
            $('#selectActivityModal').modal();
        }
    });
});
