document.addEventListener('DOMContentLoaded', function() {
    // Sidebar Initialization
    let sidenav = document.querySelectorAll('.sidenav');
    M.Sidenav.init(sidenav);

    // Datepicker Initialization
    let datepicker = document.querySelectorAll('.datepicker');
    M.Datepicker.init(datepicker, {
      format: "dd mmmm, yyyy",
      i18n: {done: "Select"}
    });

    // Select Initialization
    let selects = document.querySelectorAll('select');
    M.FormSelect.init(selects);
  });