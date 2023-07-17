


function global() {
  return {
    isMobileMenuOpen: false,
    isDarkMode: false,
    themeInit() {
      if (
        localStorage.theme === "dark" ||
        (!("theme" in localStorage) &&
          window.matchMedia("(prefers-color-scheme: dark)").matches)
      ) {
        localStorage.theme = "dark";
        document.documentElement.classList.add("dark");
        this.isDarkMode = true;
      } else {
        localStorage.theme = "light";
        document.documentElement.classList.remove("dark");
        this.isDarkMode = false;
      }
    },
    themeSwitch() {
      if (localStorage.theme === "dark") {
        localStorage.theme = "light";
        document.documentElement.classList.remove("dark");
        this.isDarkMode = false;
      } else {
        localStorage.theme = "dark";
        document.documentElement.classList.add("dark");
        this.isDarkMode = true;
      }
    },
  };
}



// $('form').submit(function(event) {
//   event.preventDefault();
//   const nameVal = $('#name').val();

//   showName();
//   $.post('/msg',
//     { name: nameVal },
//     function(name){
//       $('#name').val('')
//       $('blog.db').append(createTodoTemplate(nameVal, false));

//     }
  
//   )






// });


$("form").submit(function(event) {
  event.preventDefault();
  $("button").click(function(){
    $.ajax({
      url: '/contact/',
      type: 'POST',
      data: {
        name: $('#name').val(),
        email: $('#email').val(),
        msg: $('#message').val()
      },
      success: function(contact_add) {
        $('#send').html(contact_add);
      },
      error: function(contact_add) {
        $('#not_send').html(contact_add);
      }
    });
  });
});
