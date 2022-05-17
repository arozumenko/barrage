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
                button = `<button type="button" class="btn btn-sm btn-primary btn-outline btn-wrap-text m-2" data-url="${item.url}" data-proxy="${item.proxy}" onclick="barrage(event)"><i class="fas fa-check-circle mr-1"></i>${item.url}</button>`
                dropitems.push(item.url)
            } else {
                button = `<button type="button" class="btn btn-sm btn-secondary btn-outline btn-wrap-text m-2" data-url="${item.url}" onclick="barrage(event)" disabled><i class="fas fa-times-circle mr-1"></i>${item.url}</button>`
            }
            $('#results .card-body').append(button)
        })
        if (dropitems.length > 0) {
            $("#target option").remove()
            dropitems.forEach((item) => {
                $("#target").append(`<option value="${item}">${item}</option>`)
            })
        } else {
            $("#target option").remove()
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
    }, $("#urls").val().split('\n').length * 90000);
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
                    _barrage(item.value, $(`button[data-url="${item.value}"]`).attr('data-proxy'))
                    return false;
                } else if (index == $("#target option").length - 1 ) {
                    barragedTargets = []
                    barragedTargets.push(item.value)
                    _barrage(item.value, $(`button[data-url="${item.value}"]`).attr('data-proxy'))
                    return false;
                }
            })
        }
    }, (parseInt($("#TTR").val())+1)*1000);
}

function removeRecurringBarrage() {
    $("#recurringBarrage").show()
    $("#removeRecurringBarrage").hide()
    clearInterval(barrageInterval);
}

function barrageBt() {
    var url = $("#target").val()
    return _barrage(url, $(`button[data-url='${url}']`).attr('data-proxy'))
}

function barrage(ev){
    return _barrage($(ev.target).attr('data-url'), $(ev.target).attr('data-proxy'))
}

function _barrage(target, proxy){
$.ajax({
      type: "POST",
      url: '/api/barrage',
      contentType:"application/json; charset=utf-8",
      data: JSON.stringify({
        "url": target,
        "vus": $("#vUsers").val(),
        "dur": $("#TTR").val(),
        "host": $("#host").val(),
        "folder": $("#folder").val(),
        "proxy": proxy
      }),
      success: function(result) {
        console.log(result)
      }
    })
}

function loadProxies() {
    $.ajax({
      type: "GET",
      url: '/api/proxies',
      contentType:"application/json; charset=utf-8",
      success: function(result) {
        $("#proxies").val(result.proxies)
      }
    })
}

function scanProxies() {
    $.ajax({
      type: "POST",
      url: '/api/proxies',
      contentType:"application/json; charset=utf-8"
    })
}