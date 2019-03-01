function readURL(input) {

    if (input.files && input.files[0]) {
        var reader = new FileReader();

        reader.onload = function (e) {
            $('.imageuploaded').attr('src', e.target.result);
        }

        reader.readAsDataURL(input.files[0]);
    }
}

$("#image").change(function () {
    readURL(this);
    $(".image-upload").css({
        "padding": " 10px 50px"
    })
    console.log("wowo")
});
