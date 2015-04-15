$( document ).ready(function() {
  $("#addAttribute").click(function(event){

    formGroupElement = $('<div/>');
    formGroupElement.attr({
      class: "form-group"
    });

    inputContainerElement = $('<div/>');
    inputContainerElement.attr({
      class: "col-md-offset-2 col-md-4"
    });

    inputTypeElement = $('<input type="text"/>');
    inputTypeElement.attr({
      id: 'attribute',
      name: 'attribute',
      class: 'form-control input-md pull-left'
    });

    $(inputContainerElement).append(inputTypeElement);
    $(formGroupElement).append(inputContainerElement);
    $("#forms").append(formGroupElement);
  });
});