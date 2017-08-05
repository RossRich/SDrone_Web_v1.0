var sped_min = 0.04;
var sped_max = 0.095;
var angle_max = 45;
var angle_min = -45;
var steep_for_speed = 0.0025;
var steep_for_angle = 1;
var flag_two = true;
var critical_reset = 0.045;
var upTest = "";

function init() {
    var sliderSpeed = webiopi().createMySlider("speed", "outputUpdateSpeed", "listForRange", sped_min, sped_min, sped_max, steep_for_speed, set_stick_power_value);
    $("#leftStick").append(sliderSpeed);

    var myLabel = webiopi().createLabel("speed", "Скорость: ");
    $("#infoLeft").append(myLabel);

    var myOutput = webiopi().createOutput("speedOut", "speed", sped_min);
    $("#infoLeft").append(myOutput);

    var sliderAngle = webiopi().createMySlider("angle", "outputUpdateAngle", "listForRange", angle_min, 0, angle_max, steep_for_angle, set_stick_angle_value);
    $("#rightStick").append(sliderAngle);

    var myLabel = webiopi().createLabel("angle", "Угол: ");
    $("#infoRight").append(myLabel);

    var myOutput = webiopi().createOutput("angleOut", "angle", 0);
    $("#infoRight").append(myOutput);

//    var sliderBalance = webiopi().createMySlider("balance", "outputUpdateBalance", "listForRangeB", "0.05", "0.1", test_unit_motor);
//    $("#addition").append(sliderBalance);
//
//    var myOutputBalance = webiopi().createOutput("balanceOut", "balance", "0.05");
//    $("#p_for_out_ball").append(myOutputBalance);

    var stopButtonLeft = $(document.createElement("input")).attr({
        id: 'ch_one',
        name: 'ch',
        type: 'checkbox',
        checked: false
    });

    var myLabelForCh = webiopi().createLabel('ch_one', 'STOP');

    $("#leftStop").append(stopButtonLeft);
    $("#leftStop").append(myLabelForCh);

    var checkbox_for_info = $(document.createElement("input")).attr({
        id: 'checkbox_for_info',
        name: 'checkbox_for_info',
        type: 'checkbox',
        checked: false
    });
    $("#info").append(checkbox_for_info);

    var stopButtonRight = webiopi().createButton("stop_button_two", "stop", critical_stop_motor);
    stopButtonRight.attr('disabled', true);
    $("#rightStop").append(stopButtonRight);
}

function set_stick_power_value() {
    var stick_value = $("#speedOut").val();
    webiopi().callMacro("set_power", stick_value);

    if (get_flag_two() && stick_value == critical_reset) {
        set_flag_but_two(false);
        $("#stop_button_two").prop("disabled", false);
        webiopi().callMacro("critical_stop", []);
    }
}

function set_stick_angle_value() {
    var stick_value = $("#angleOut").val();
    if (stick_value > 0) {
        webiopi().callMacro("left", stick_value);
        webiopi().callMacro("right", 0);
    } else {
        webiopi().callMacro("right", stick_value);
        webiopi().callMacro("left", 0);
    }
}

function outputUpdateSpeed(volS) {
    document.querySelector("#speedOut").value = volS;

}

function outputUpdateAngle(volA) {
    document.querySelector("#angleOut").value = volA;

}

//function outputUpdateBalance(valB) {
//    document.querySelector("#balanceOut").value = valB;
//
//}

//function test_unit_motor() {
//    var name = $("#motorName").val();
//    var valBal = $("#balanceOut").val();
//    webiopi().callMacro("start_unit", [name, valBal]);
//}

function set_flag_but_two(val_flag) {
    this.flag_two = val_flag;
}

function get_flag_two() {
    return this.flag_two;
}

function critical_stop_motor() {
    if ($('#ch_one').prop('checked') && !$("#stop_button_two").prop("disabled")) {
        webiopi().callMacro("critical_stop", []);
        set_flag_but_two(true);
        $("#ch_one").prop("checked", false);
        $("#stop_button_two").prop("disabled", true);
    }
}

function clickDebugButton() {
    if ($("#stop_button_two").prop("disabled")) {
        console.log("debug mode");
        webiopi().callMacro("set_mode",["debug"]);
        document.location.href = "debug.html";
    } else {
        console.log("Необходимо заблокировать аппарат");
    }
}