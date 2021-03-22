$(document).ready(function () {
    $(".sidenav").sidenav(); /*jquery sidenav*/
    $("#flash").fadeOut(3000); /*flash message fade out*/
    $("#no-result").fadeIn("slow");
    $('.collapsible').collapsible(); /*collasible*/
    $('.modal').modal({preventScrolling: false});  /*confirmation before deleting*/
    $('.tap-target').tapTarget(); /*open by tapping*/
    $('.fixed-action-btn').floatingActionButton();
});
