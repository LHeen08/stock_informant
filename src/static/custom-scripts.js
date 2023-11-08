function showLoader() {
  $("#loader-container").addClass("show");
  $("#loader-spinner").show();
}

function hideLoader() {
  $("#loader-container").removeClass("show");
  $("#loader-spinner").hide();
}

// const popover = new bootstrap.Popover('.popover-dismiss', {
//   trigger: 'focus'
// })




function fetchData(inital_fetch) {
  // Show the loader when fetching data
  showLoader();

  var ticker;

  if (inital_fetch) {
    // Get the ticker value from the input field
    ticker = $('#initial-ticker').val();
  }
  else {
    ticker = $('#ticker').val();
  }

  // Make an AJAX POST request to fetch data and update the page
  $.ajax({
    method: 'POST',
    url: '/fetch_data', // Call the fetch_data function in python
    data: { ticker: ticker },
    dataType: 'json',
    success: function (data) {
      if ('success' in data) {
        console.log("Successful response from /fetch_data");

        // Route to data_page using flask
        window.location.href = '/data_page';
      }
      else {
        alert(data.error);
      }

      hideLoader();

    },
    error: function () {
      hideLoader();
      alert('Invalid data or an error occurred while fetching data. Please make sure you entered a correct ticker');
    }

  });
}


$(document).ready(function () {

  hideLoader();
  
  // Handle button click event with jQuery
  $('#fetch-button').click(fetchData);

  $('#company-summary').click(function () {
    $('#company-summary').popover('show');
  });


  // Handle initial page ticker fetch data button with jQuery
  $('#initial-ticker').on("keydown", function (e) {
    if (e.key == "Enter") {
      console.log("Handling enter event with jQuery: " + e.key);
      fetchData(true);
      e.preventDefault();
      return false;
    }
  });


  // Handle initial page ticker fetch data button with jQuery
  $('#ticker').on("keydown", function (e) {
    if (e.key == "Enter") {
      console.log("Handling enter event with jQuery: " + e.key);
      fetchData(false);
      e.preventDefault();
      return false;
    }
  });


  // Handle dcf eps growth rate input
  $('#dcf-eps-growth-entry').on("keydown", function (event) {
    if (event.key == "Enter") {
      console.log("Handling enter event with jQuery: " + event.key);
      event.preventDefault();

      var new_eps_growth = this.value;
      this.value = new_eps_growth;
    }
  }).on("blur", function () {
    console.log("Handling blur: ");
    var new_eps_growth = this.value;

    this.value = new_eps_growth;
  });


  // Handle eps growth rate input
  $('#lynch-eps-growth-entry').on("keydown", function (event) {
    if (event.key == "Enter") {
      console.log("Handling enter event with jQuery: " + event.key);
      event.preventDefault();

      var new_eps_growth = this.value;
      this.value = new_eps_growth;
    }
  }).on("blur", function () {
    console.log("Handling blur: ");
    var new_eps_growth = this.value;

    this.value = new_eps_growth;
  });

  // Handle eps growth rate input
  $('#bg-eps-growth-entry').on("keydown", function (event) {
    if (event.key == "Enter") {
      console.log("Handling enter event with jQuery: " + event.key);
      event.preventDefault();

      var new_eps_growth = this.value;
      this.value = new_eps_growth;
    }
  }).on("blur", function () {
    console.log("Handling blur: ");
    var new_eps_growth = this.value;

    this.value = new_eps_growth;
  });


});