$(document).ready(function () {
    $(".sidenav").sidenav(); /*jquery sidenav*/
    $("#flash").fadeOut(3000); /*flash message fade out*/
    $('.collapsible').collapsible(); /*collasible*/
    $('.modal').modal({preventScrolling: false}); /*confirmation before deleting*/
});
