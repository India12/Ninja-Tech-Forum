/* Check if bot */
$(document).ready(function() {
  $(function() {
      $("#submit-button").click(function() {
      });

      var numOne = Math.floor(Math.random() * 10) + 1;
      var numTwo = Math.floor(Math.random() * 10) + 1;
      var sum = numOne + numTwo;

      $(".numOne").text(numOne);
      $(".numTwo").text(numTwo);

      $("#submit-button").click(function (event) {
          var value = parseInt($("#calc").val());
          if (value != sum) {
              alert("Your calculation is not correct!");
              event.preventDefault();
          }
          /*else {
              $(this).hide();
          }*/
      });
  });
});

/* show more/less about */
$(document).ready(function() {
 $(".show-more a").on("click", function() {
    var $this = $(this);
    var $content = $this.parent().prev("div.content");
    var linkText = $this.text().toUpperCase();

    if(linkText === "SHOW MORE"){
        linkText = "Show less";
        $content.switchClass("hideContent", "showContent", 400);
    } else {
        linkText = "Show more";
        $content.switchClass("showContent", "hideContent", 400);
    };
    $this.text(linkText);
  });
});

/* tables */
$(document).ready( function (){
    $('#topicTable, #mytopics-table, #mycomments-table, #user-comments-list-table').DataTable({
      "order": [[ 2, "desc" ]]
    });
});
$(document).ready( function (){
    $('#user-topics-list-table').DataTable({
      "order": [[ 1, "desc" ]]
    });
});
$(document).ready( function (){
    $('#users-table').DataTable();
});
