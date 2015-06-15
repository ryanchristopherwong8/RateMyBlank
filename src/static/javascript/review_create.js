$( document ).ready(function() {
    $(function() {
        $(".score-slider").on("input", function() {
            var reviewForm = $(this).closest(".review-form");
            reviewForm.find(".review-score-input").val($(this).val());
        });

        $(".review-score-input").on("input", function() {
            var reviewForm = $(this).closest(".review-form");
            reviewForm.find(".score-slider").val($(this).val());
        });
    });
});