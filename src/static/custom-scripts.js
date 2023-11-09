function showLoader() {
  $("#loader-container").addClass("show");
  $("#loader-spinner").show();
}

function hideLoader() {
  $("#loader-container").removeClass("show");
  $("#loader-spinner").hide();
}

function fetchData(inital_fetch) {
  // Show the loader when fetching data
  showLoader();

  var ticker;

  if (inital_fetch) {
    // Get the ticker value from the input field
    ticker = $("#initial-ticker").val();
  } else {
    ticker = $("#ticker").val();
  }

  // Make an AJAX POST request to fetch data and update the page
  $.ajax({
    method: "POST",
    url: "/fetch_data", // Call the fetch_data function in python
    data: { ticker: ticker },
    dataType: "json",
    success: function (data) {
      if ("success" in data) {
        console.log("Successful response from /fetch_data");

        // Route to data_page using flask
        window.location.href = "/data_page";
      } else {
        alert(data.error);
      }

      hideLoader();
    },
    error: function () {
      hideLoader();
      alert(
        "Invalid data or an error occurred while fetching data. Please make sure you entered a correct ticker"
      );
    },
  });
}

function updateDCF() {
  // Variables for dcf
  var epsGrowth = $("#dcf-eps-growth-entry").val();
  var discountRate = $("#discount-rate-entry").val();
  var terminalGrowthRate = $("#terminal-growth-entry").val();
  var marginOfSafety = $("#margin-of-safety-entry").val();

  // Create a data object to pass to Flask
  var dataToPass = {
    epsGrowth: epsGrowth,
    discountRate: discountRate,
    terminalGrowthRate: terminalGrowthRate,
    marginOfSafety: marginOfSafety,
  };

  console.log("Passing to flask: ", dataToPass);

  // Make an ajax call to update with the new values
  $.ajax({
    method: "POST",
    url: "/calculate_dcf",
    data: dataToPass,
    dataType: "json",
    success: function (data) {
      if (data) {
        console.log("Return data: ", data);

        console.log("dcf value: ", data["dcfVal"]);

        // Return the new dcf value
        $("#dcf-val").text(data["dcfVal"]);
      } else {
        alert("Error getting data from /calculate_dcf");
      }
    },
    error: function () {
      alert("Invalid data or an error occurred while calculating dcf value.");
    },
  });
}

$(document).ready(function () {
  hideLoader();

  // Handle button click event with jQuery
  $("#fetch-button").click(fetchData);

  // Handle company summary popover messgage
  $("#company-summary").click(function () {
    $("#company-summary").popover("show");
  });


  // Hold onto the old values for the forms, so if we click off and its null its the old value
  var old_dcf_eps_growth_rate_value = $("#dcf-eps-growth-entry").val();
  var old_dcf_discount_rate_value = $("#discount-rate-entry").val();
  var old_dcf_terminal_growth_value = $("#terminal-growth-entry").val();
  var old_dcf_margin_of_safety_value = $("#magin-of-safety-entry").val();




  // Handle initial page ticker fetch data button with jQuery
  $("#initial-ticker").on("keydown", function (e) {
    if (e.key == "Enter") {
      console.log("Handling enter event with jQuery: " + e.key);
      fetchData(true);
      e.preventDefault();
      return false;
    }
  });

  // Handle initial page ticker fetch data button with jQuery
  $("#ticker").on("keydown", function (e) {
    if (e.key == "Enter") {
      console.log("Handling enter event with jQuery: " + e.key);
      fetchData(false);
      e.preventDefault();
      return false;
    }
  });

  // Handle dcf form
  // Handle dcf eps growth rate input
  $("#dcf-eps-growth-entry")
    .on("keydown", function (event) {
      if (event.key == "Enter") {
        console.log("Handling enter event with jQuery: " + event.key);
        event.preventDefault();

        var new_eps_growth = this.value;
        if (new_eps_growth !== null && new_eps_growth.trim() !== '') {
          this.value = new_eps_growth;
          updateDCF();
        }
        else
        {
          this.value = old_dcf_eps_growth_rate_value;
        }
      }
    })
    .on("blur", function () {
      console.log("Handling blur: ");
      var new_eps_growth = this.value;
      if (new_eps_growth !== null && new_eps_growth.trim() !== '') {
        this.value = new_eps_growth;
        updateDCF();
      }
      else
      {
        this.value = old_dcf_eps_growth_rate_value;
      }
    });

  // Handle discount rate
  $("#discount-rate-entry")
    .on("keydown", function (event) {
      if (event.key == "Enter") {
        console.log("Handling enter event with jQuery: " + event.key);
        event.preventDefault();

        var discountRate = this.value;
        if (discountRate !== null && discountRate.trim() !== '') {
          this.value = discountRate;
          updateDCF();
        }
        {
          this.value = old_dcf_discount_rate_value;
        }
      }
    })
    .on("blur", function () {
      console.log("Handling blur: ");
      var discountRate = this.value;
      if (discountRate !== null && discountRate.trim() !== '') {
        this.value = discountRate;
        updateDCF();
      }
      {
        this.value = old_dcf_discount_rate_value;
      }
    });

  // Handle terminal growth rate
  $("#terminal-growth-entry")
    .on("keydown", function (event) {
      if (event.key == "Enter") {
        console.log("Handling enter event with jQuery: " + event.key);
        event.preventDefault();

        var terminal_growth = this.value;
        // Udpate if not null
        if (terminal_growth !== null && terminal_growth.trim() !== '') {
          this.value = terminal_growth;
          updateDCF();
        }
        {
          this.value = old_dcf_terminal_growth_value;
        }
      }
    })
    .on("blur", function () {
      console.log("Handling blur: ");
      var terminal_growth = this.value;
      if (terminal_growth !== null && terminal_growth.trim() !== '') {
        this.value = terminal_growth;
        updateDCF();
      }
      {
        this.value = old_dcf_terminal_growth_value;
      }
    });

  // Handle margin of safety
  $("#margin-of-safety-entry")
    .on("keydown", function (event) {
      if (event.key == "Enter") {
        console.log("Handling enter event with jQuery: " + event.key);
        event.preventDefault();

        var marginOfSafety = this.value;
        if (marginOfSafety !== null && marginOfSafety.trim() !== '') {
          this.value = marginOfSafety;
          updateDCF();
        }
        {
          this.value = old_dcf_margin_of_safety_value;
        }
      }
    })
    .on("blur", function () {
      console.log("Handling blur: ");
      var marginOfSafety = this.value;
      if (marginOfSafety !== null && marginOfSafety.trim() !== '') {
        this.value = marginOfSafety;
        updateDCF();
      }
      {
        this.value = old_dcf_margin_of_safety_value;
      }
    });

  // Handle eps growth rate input
  $("#lynch-eps-growth-entry")
    .on("keydown", function (event) {
      if (event.key == "Enter") {
        console.log("Handling enter event with jQuery: " + event.key);
        event.preventDefault();

        // This should call update dcf

        var new_eps_growth = this.value;
        this.value = new_eps_growth;
      }
    })
    .on("blur", function () {
      console.log("Handling blur: ");
      var new_eps_growth = this.value;

      this.value = new_eps_growth;
    });

  // Handle eps growth rate input ben graham
  $("#bg-eps-growth-entry")
    .on("keydown", function (event) {
      if (event.key == "Enter") {
        console.log("Handling enter event with jQuery: " + event.key);
        event.preventDefault();

        var new_eps_growth = this.value;
        this.value = new_eps_growth;
      }
    })
    .on("blur", function () {
      console.log("Handling blur: ");
      var new_eps_growth = this.value;

      this.value = new_eps_growth;
    });
});
