$(document).ready(function() {
    // Dropdown toggle event handler using Bootstrap's built-in functionality
    $('.dropdown-toggle').on('click', function() {
      $(this).siblings('.dropdown-menu').toggle(); 
    });
  
    $(document).on('click', function(event) {
      var target = $(event.target);
      if (!target.closest('.dropdown-toggle').length && !target.closest('.dropdown-menu').length) {
        $('.dropdown-menu').hide();
      }
    });
  });
  

setTimeout(function(){
    $('#message').fadeOut('slow')
}, 8000)
