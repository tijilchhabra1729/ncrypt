
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
            ext == "png" || ext == "jpeg" || ext == "jpg" || ext == "gif" || ext == "pdf"
        )) {
            var path = $(input).val();
            var filename = path.replace(/^.*\\/, "");
            $('.fileUpload span').html('Uploaded Proof : ' + filename);
            return "Uploaded file : " + filename;
        } else {
            $(input).val("");
            return "Only image/pdf formats are allowed!";
        }
    }

});


console.log('Xino <3 Ncrypt')
