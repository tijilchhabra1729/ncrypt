
$(window, document, undefined).ready(function () {

    $('input').blur(function () {
        var $this = $(this);
        if ($this.val())
            $this.addClass('used');
        else
            $this.removeClass('used');
    });
    $('textarea').blur(function () {
        var $this = $(this);
        if ($this.val())
            $this.addClass('used');
        else
            $this.removeClass('used');
    });
});





$(document).ready(function ($) {

    $(".uploadlogo").change(function () {
        var filename = readURL(this);
        $(this).parent().children('span').html(filename);
    });

    function readURL(input) {
        var url = input.value;
        var ext = url.substring(url.lastIndexOf('.') + 1).toLowerCase();
        if (input.files && input.files[0] && (
            ext == "csv"
        )) {
            var path = $(input).val();
            var filename = path.replace(/^.*\\/, "");
            $('.fileUpload span').html('Uploaded Proof : ' + filename);
            return "Selected file : " + filename;
        } else {
            $(input).val("");
            return "Only csv formats are allowed!";
        }
    }

});

$('#pills-tab a').on('click', function (e) {
    e.preventDefault()
    $(this).tab('show')
})

console.log('Xino <3 Ncrypt')
