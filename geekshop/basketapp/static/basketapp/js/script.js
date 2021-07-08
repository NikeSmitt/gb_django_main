window.onload = function () {
    $('.basket_list').on('clicks', 'input[type=number]', function (event) {
        const t_href = event.target;

        $.ajax({
            url: "/basket/edit/" + t_href.name + "/" + t_href.value + "/",

            function(data) {
                $('.basket_list').html(data.result);
            },
        });
        event.preventDefault();
    });
}