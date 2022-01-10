$(document).ready(function(){
    const select = document.getElementById('floatingSelect')
    console.log(select.options[select.selectedIndex].value)
    $("select").click(function() {
        var option = $(this).val()
        if (option == 'new') {
            $('#new-refuel').css('display', 'block');
            $('#refuel-names-select').css('display', 'none');
            $('#date').css('display', 'block');
            console.log('revealing new input...');
        }
        else if (option == 'add') {
            $('#new-refuel').css('display', 'none');
            $('#refuel-names-select').css('display', 'block');
            $('#date').css('display', 'none');
        }
    })

    var $select = $("#refuel-names-select")
    $.ajax({
        url:`http://irt-t.ru:1234/`,
        type:"GET",
        success: function(results) {
            console.log(results)
            for (i in results.names) {
                    $select.append(`<option value="${i}">${results.names[i]}</option>`);
            }
        }
    });
})