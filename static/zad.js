$(".show").on('click', function(){
    if ($(this).html() === "Pokaż rozwiązanie"){
        $(this).html("Ukryj rozwiązanie")
    } else{
        $(this).html("Pokaż rozwiązanie")
    }
    $(this).next().slideToggle();

})