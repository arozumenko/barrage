function validateUrls() {
    $("#validateBtn").html('<i class="fas fa-sync fa-spin">')
    $("#validateBtn").prop('disabled', true)
    $.ajax({
      type: "POST",
      url: '/api/validate',
      contentType:"application/json; charset=utf-8",
      data: JSON.stringify({"urls": $("#urls").val()}),
      success: function(result){
        $('#results .card-body').children().remove()
        $("#validateBtn").html('<i class="fas fa-play">')
        $("#validateBtn").prop('disabled', false)
        var dropitems = []
        result.forEach((item, index) => {
            var button = ''
            if(item.status) {
                button = `<button type="button" class="btn btn-sm btn-primary btn-outline btn-wrap-text m-2" data-url="${item.url}" onclick="barrage(event)"><i class="fas fa-check-circle mr-1"></i>${item.url}</button>`
                dropitems.push(item.url)
            } else {
                button = `<button type="button" class="btn btn-sm btn-secondary btn-outline btn-wrap-text m-2" data-url="${item.url}" onclick="barrage(event)" disabled><i class="fas fa-times-circle mr-1"></i>${item.url}</button>`
            }
            $('#results .card-body').append(button)
        })
        console.log(dropitems)
        if (dropitems.length > 0) {
            $("#target option").remove()
            dropitems.forEach((item) => {
                $("#target").append(`<option value="${item}">${item}</option>`)
            })
        }

      }
    });
}

var interval;

function scheduleRecurringJob() {
    $("#setRecurring").hide()
    $("#removeRecurring").show()
    interval = setInterval(function() {
        validateUrls();
    }, 300000);
}

function removeInterval() {
    $("#setRecurring").show()
    $("#removeRecurring").hide()
    clearInterval(interval);
}

var barrageInterval;
var barragedTargets = []
function scheduleRecurringBarrage() {
    $("#recurringBarrage").hide()
    $("#removeRecurringBarrage").show()
    barrageInterval = setInterval(function() {
        if ($("#target option").length == 0) {
            barragedTargets = []
        } else {
            $("#target option").each((index, item)=>{
                if (barragedTargets.indexOf(item.value) == -1) {
                    barragedTargets.push(item.value)
                    _barrage(item.value, $("#vUsers").val(), $("#TTR").val())
                    return false;
                } else if (index == $("#target option").length - 1 ) {
                    barragedTargets = []
                    barragedTargets.push(item.value)
                    _barrage(item.value, $("#vUsers").val(), $("#TTR").val())
                    return false;
                }
            })
        }
    }, parseInt($("#TTR").val())*1000);
}

function removeRecurringBarrage() {
    $("#recurringBarrage").show()
    $("#removeRecurringBarrage").hide()
    clearInterval(barrageInterval);
}

function barrageBt() {
    return _barrage($("#target").val(), $("#vUsers").val(), $("#TTR").val())
}

function barrage(ev){
    return _barrage($(ev.target).attr('data-url'), $("#vUsers").val(), $("#TTR").val())
}

function _barrage(target, vus, dur){
$.ajax({
      type: "POST",
      url: '/api/barrage',
      contentType:"application/json; charset=utf-8",
      data: JSON.stringify({
        "url": target,
        "vus": vus,
        "dur": dur
      }),
      success: function(result) {
        console.log(result)
      }
    })
}