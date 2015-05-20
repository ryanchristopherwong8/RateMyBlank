$(document).ready(function() {
    var constants = {
       "scoreToHexFactor" : 102 // 2.5 * 102 is 255 (max)
    };

    function renderReviewAverageColors() {
        var reviewAverages = $(".review-average");
        reviewAverages.each(function(index, element) {
            var score = $(element).text();
            var redHex = 255;
            var greenHex = 255;
            if (score >= 0 && score <= 5) {
                if (score <= 2.5) {
                    greenHex = Math.round(constants.scoreToHexFactor * score);
                } else if (score >= 2.5) {
                    redHex = Math.round(255 - (constants.scoreToHexFactor * (score - 2.5)));
                }
                var reviewColor = "rgb(" + redHex + "," + greenHex + ",0)";
                $(element).css("background-color", reviewColor);
            } else {
                $(element).css("background-color", "rgb(100,100,100)");
            }
        });
    }
    renderReviewAverageColors();
});