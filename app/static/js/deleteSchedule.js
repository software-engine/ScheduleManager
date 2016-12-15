/**
 * Created by specific on 2016/12/10.
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

function deleteSchedule(id) {
    $('#deleteScheduleConfirm').click(function () {
        deleteScheduleFormSubmit(id);
    });
    $('#deleteScheduleModal').modal();
}

function deleteScheduleFormSubmit(id) {
    $('#deleteScheduleForm' + id).submit();
}

$(document).ready(function () {
    $('#deleteSchedulesConfirm').click(function () {
        $('#deleteSchedulesForm').submit();
    });

    $('#deleteSchedules').click(function () {
        if ($('.op_check').filter(':checked').size() > 0) {
            var schedules_id = [];
            $('.op_check:checked').each(function () {
                schedules_id.push($(this).val());
            });
            var schedule_id_json = JSON.stringify(schedules_id);
            $('#schedule_ids').val(schedule_id_json);
            $('#deleteSchedulesModal').modal();
        } else {
            $('#selectScheduleModal').modal();
        }
    })
})
