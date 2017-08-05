"use strict";

var asix = "",
    outP = 0,
    outI = 0,
    outD = 0,
    critical_reset = 0.045;

function setParamForRangeSpeed() {
    var speed_min = 0.04,
        speed_max = 0.095,
        step_for_speed = 0.0025;
    $('#speed_control_range').attr({
        max: speed_max,
        min: speed_min,
        step: step_for_speed,
        value: speed_min,
        disabled: false
    });

}

function funDicIncBut(id) {
    switch (id) {
        case "inc_but_p":
            funClickButIncDic(id, "p"); //send to fun id and "p"-p_term
            break;
        case "inc_but_i":
            funClickButIncDic(id, "i");
            break;
        case "inc_but_d":
            funClickButIncDic(id, "d");
            break;
        case "dic_but_p":
            funClickButIncDic(id, "p");
            break;
        case "dic_but_i":
            funClickButIncDic(id, "i");
            break;
        case "dic_but_d":
            funClickButIncDic(id, "d");
            break;
        default:
            console.error("[error] In funDicIncBut() function. Invalid ID");
            break;
    }
}

function funClickButIncDic(id, range) {
    var step = "",
        valRange = "",
        newValRange = null,
        tmpRange = range + "_term",
        tmpId = id,
        tmpConditionInc = "inc_but_" + range,
        tmpConditionDic = "dic_but_" + range;

    step = $("#" + tmpRange).attr("step");
    valRange = $("#" + tmpRange).attr("value");

    if (tmpId == tmpConditionDic) {
        newValRange = parseStringNum(valRange) - parseStringNum(step);
    } else if (tmpId == tmpConditionInc) {
        newValRange = parseStringNum(step) + parseStringNum(valRange);
    } else {
        console.error("[ERROR] In funClickButP() function. Invalid argument");
    }

    newValRange = parseStringNum(newValRange);
    $("#" + tmpRange).attr("value", newValRange);
    funRangeOutPID(newValRange, tmpRange);
    funRangeChangePID();
}

function funRangeOutPID(val_pid, id) {
    switch (id) {
        case "p_term":
            outP = val_pid;
            $('#out_p').val(outP);
            $('#p_term').attr("value", outP);
            break;
        case "i_term":
            outI = val_pid;
            $('#out_i').val(outI);
            $('#i_term').attr("value", outI);
            break;
        case "d_term":
            outD = val_pid;
            $('#out_d').val(outD);
            $('#d_term').attr("value", outD);
            break;
        default:
            console.error("[ERROR] In funRangeOutPID() function. Invalid argument");
            break;
    }
}

function funCheckSave() {
    if ($('#check_save').prop('checked')) {
        $('#save_but').prop('disabled', false);
    } else {
        $('#save_but').prop('disabled', true);
    }
}

function funTextAxisChange() {
    var asix = $('#input_asix').val().toLowerCase();
    if (asix == "ox" || asix == "oy") {
        $('#input_but').prop('disabled', false);
    } else {
        $('#input_but').prop('disabled', true);
    }
}

function setDataFromPy(macro, args, res) {
    var p = 0,
        i = 0,
        d = 0,
        iVal = 0,
        pVal = 0,
        dVal = 0,
        tmp = res.split(";");

    for (var j = 0; j < tmp.length; j++) {
        var tempSplit = "",
            max = 0,
            iter = tmp[j].split("=");
        if (iter[0] == "i") {
            i = parseInt(iter[1]);
            tempSplit = iter[1].split(":");
            iVal = parseFloat(tempSplit[1]);
            outI = iVal;
            i = buildStep(i);
            max = iVal * 2;
            funRangeOutPID(iVal, "i_term");
            $('#i_term').attr({
                step: i,
                max: max,
                value: iVal
            });
        } else if (iter[0] == "p") {
            p = parseInt(iter[1]);
            tempSplit = iter[1].split(":");
            pVal = parseFloat(tempSplit[1]);
            outP = pVal;
            p = buildStep(p);
            max = pVal * 2;
            funRangeOutPID(pVal, "p_term");
            $('#p_term').attr({
                step: p,
                max: max,
                value: pVal
            });
        } else if (iter[0] == "d") {
            d = parseInt(iter[1]);
            tempSplit = iter[1].split(":");
            dVal = parseFloat(tempSplit[1]);
            outD = dVal;
            d = buildStep(d);
            max = dVal * 2;
            funRangeOutPID(dVal, "d_term");
            $('#d_term').attr({
                step: d,
                max: max,
                value: dVal
            });
        } else {
            console.error("[ERROR] In setDataFromPy() function. Invalid argument");
        }
    }
}

function buildStep(val) {
    var tmpVal = val;
    if (val == 0) {
        tmpVal = 1;
    }
    var outVal = 0.1;
    for (var i = 0; i < (tmpVal - 1); i++) {
        outVal /= 10;
        outVal = outVal.toFixed(10);
    }
    outVal = parseStringNum(outVal);
    return outVal;
}

function funSelectAxis() {
    asix = $('#input_asix').val();
    setParamForRangeSpeed();
    webiopi().callMacro("get_param", [asix.toLowerCase()], setDataFromPy);
}

function funChangeCoef(valueOutP, valueOutI, valueOutD) {
    if (asix == "") {
        alert("Необходима ось");
    } else {
        webiopi().callMacro("debug_pid", [valueOutP, valueOutI, valueOutD]);
    }
}

function funSpeedControl(valSpeed) {
    var power_pwm = valSpeed;
    $('#out_speed').val(valSpeed);
    webiopi().callMacro("start_debug_motors", [power_pwm]);
    if (power_pwm == critical_reset) {
        webiopi().callMacro("critical_stop", []);
    }
}

function funClickButSave() {
    webiopi().callMacro("critical_stop", []);
    webiopi().callMacro("set_mode", ["realise"]);
    document.location.href = "index.html";
}

function parseStringNum(stNum) {
    var tmp = stNum;
    if (typeof(tmp) == "string" && tmp != undefined) {
        tmp = parseFloat(tmp);
    }
    tmp = tmp.toFixed(10);
    tmp = tmp.toString();
    var size = tmp.length,
        newStNum = "";
    for (var i = (size - 1); i >= 0; i--) {
        if (tmp[i] != '0' && tmp[i] != undefined) {
            size = i + 1
            break;
        }
    }
    newStNum = tmp.substr(0, size);
    newStNum = parseFloat(newStNum);
    return newStNum;
}

function funRangeChangePID() {
    funChangeCoef(outP, outI, outD);
}