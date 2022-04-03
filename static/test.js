var time = 300

$("input:checkbox").on('click', function () {
  var $box = $(this);
  if ($box.is(":checked")) {
    var group = "input:checkbox[name='" + $box.attr("name") + "']";
    $(group).prop("checked", false);
    $box.prop("checked", true);
  } else {
    $box.prop("checked", false);
  }
});

$(".show_answer").on('click', function () {
  $(this).prev().slideToggle();
  if ($(this).html() === "Pokaż odpowiedź") {
    $(this).html("Ukryj odpowieź")
  } else {
    $(this).html("Pokaż odpowiedź")
  }
})

setInterval(function () {
  if (time > 0) {
    time -= 1;
    minutes = parseInt(time / 60)
    seconds = parseInt(time % 60)

    if (seconds < 10) {
      seconds = "0" + seconds
    }

    $("#timer").html("Do końca testu pozostało " + minutes + ":" + seconds + ".")
    if (time == 0) {
      var button = document.getElementById("submit_button");
      button.click();
      alert("Czas minął!")
    }
  }
  
}, 1000);