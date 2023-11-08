function showLoader() {
  $("#loader-container").show();
}

function hideLoader() {
  $("#loader-container").hide();
}





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

        // Route to main_page using flask
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
  // Handle button click event with jQuery
  $('#fetch-button').click(fetchData);

  $('#summary-button').click(function() {
    $('#company-summary').toggle();
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
});