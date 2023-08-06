;(function($){
    $(document).ready(function(){

        $(".TextInputFieldFilter .TextInputFieldFilterResetButton").click(function(){
            var form = $(this).parents("form");
            var input = form.find(".TextInputFieldFilterInput")
            input.val("");

            var params = parseParam(window.location.href)
            params[input.attr("name")] = "";

            var new_querystring = $.param(params);
            var new_url = window.location.origin + window.location.pathname + "?" + new_querystring;

            window.location.href = new_url;
        });

        $(".TextInputFieldFilter .TextInputFieldFilterSubmitButton").click(function(){
            var form = $(this).parents("form");
            var input = form.find(".TextInputFieldFilterInput")

            var params = parseParam(window.location.href)
            params[input.attr("name")] = input.val();

            var new_querystring = $.param(params);
            var new_url = window.location.origin + window.location.pathname + "?" + new_querystring;

            window.location.href = new_url;
        });
    });
})(jQuery);