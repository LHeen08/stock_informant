  // Setup info boxes additional info
  let dcfHelpInfo = `
    Discounted Cash Flow (DCF) analysis assesses a company's value based on 
    projected future free cash flows. This involves predicting cash flows over 
    ten years, incorporating historical data and a growth rate. The analysis discounts 
    future cash flows to present value, factoring in the time value of money and risk.
    <br>
    The equity value is calculated as (Sum of Future Free Cash Flows + Cash and Cash Equivalents - Total Debt) / Outstanding Shares. 
    <br>
    This method, though reliant on assumptions, is widely used to determine a potential investment's value. You should always factor in
    some margin of safety.
  `;

  let lynchHelpInfo = `
    Peter Lynch: You should select from industries and companies from which you are familiar and have an 
    understanding of the factors that will move the stock price. Know the company and their plans for increasing
    growth and any red flags that could hurt that growth. The following metrics below should be used for comparison
    to similar companies to provide meaningful insight.
    <br>
    <br>
    GuruFocus: PEG Ratio x EPS Growth x EPS
    <br>
    Value > 1: Stock may be overvalued relative to its growth prospects. Value < 1: Stock might be undervalued
    relative to its growth prospects.
    <br>
    <br>
    NASDAQ: EPS Growth x EPS
    <br>
    Value ~1: Indicates balance between the current earnings and expected growth
    <br>
    <br>
    Custom: (EPS Growth + Dividend Yield / PE Ratio) x 100
    <br>
    Value > 1: May indicate more favorable combination of growth and income.
    Value < 1: May indicate less favorable combination of growth and income.
    `;

  let benGrahamInfo = `
    The Benjamin Graham Valuation is a formula for valuing growth stocks. It is used to estimate the intrinsic value of the stock. 
  `
  ;
  let grahamNumInfo = `
    The Graham Number measures a stocks fundamental value by taking into account the EPS and Book Value Per Share. It is for a defensive investor to determine an upper bound of the price range that the investor should be willing to pay for a stock. Based off this theory any stock price below the graham number would be considered undervalued.
    <br>
    Formula: Square Root(22.5 x EPS x Book Value Per Share)
  `;

  let multiplesValuationInfo = `
    The multiples valuation is used to compare similar companies multiples to gauge their performance in comparison to the currently researched company. This is used as a reference for a quick broad comparison. 
  `;
  


function showLoader() {
  $("#loader-container").addClass("show");
  $("#loader-spinner").show();
}

function hideLoader() {
  $("#loader-container").removeClass("show");
  $("#loader-spinner").hide();
}

function fetchData(initial_fetch) {
  // Show the loader when fetching data
  showLoader();

  var ticker;

  if (initial_fetch) {
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

// Function to update peter lynch box
function updatePeterLynch() {
  // Variables for eps growth entry
  var epsGrowth = $("#lynch-eps-growth-entry").val();

  // Create a data object to pass to Flask
  var dataToPass = {
    epsGrowth: epsGrowth,
  };

  console.log("Passing to flask: ", dataToPass);

  // Make an ajax call to update with the new values
  $.ajax({
    method: "POST",
    url: "/calculate_peter_lynch",
    data: dataToPass,
    dataType: "json",
    success: function (data) {
      if (data) {
        console.log("Return data: ", data);

        // Return the new lynch values
        $("#lynch-guru-focus").text(data["gurufocus"]); // Guru focus entry
        $("#lynch-nasdaq").text(data["nasdaq"]); // Guru focus entry
        $("#lynch-custom").text(data["my_method"]); // Guru focus entry
      } else {
        alert("Error getting data from /calculate_peter_lynch");
      }
    },
    error: function () {
      alert(
        "Invalid data or an error occurred while calculating peter lynch value."
      );
    },
  });
}


// Function to update peter lynch box
function updateBenGraham() {
  // Variables for eps growth entry
  var epsGrowth = $("#ben-graham-eps-growth-entry").val();

  // Create a data object to pass to Flask
  var dataToPass = {
    epsGrowth: epsGrowth,
  };

  console.log("Passing to flask: ", dataToPass);

  // Make an ajax call to update with the new values
  $.ajax({
    method: "POST",
    url: "/calculate_ben_graham",
    data: dataToPass,
    dataType: "json",
    success: function (data) {
      if (data) {
        console.log("Return data: ", data);

        // Return the new ben graham calc
        $("#ben-graham-formula").text(data["bg_val"]);
      } else {
        alert("Error getting data from /calculate_peter_lynch");
      }
    },
    error: function () {
      alert(
        "Invalid data or an error occurred while calculating peter lynch value."
      );
    },
  });
}

// Function to format numbers
function formatNumberAbbreviation(number) {
  if (Math.abs(number) >= 1.0e12) {
    return (number / 1.0e12).toFixed(2) + "T"; // Trillions
  } else if (Math.abs(number) >= 1.0e9) {
    return (number / 1.0e9).toFixed(2) + "B"; // Billions
  } else if (Math.abs(number) >= 1.0e6) {
    return (number / 1.0e6).toFixed(2) + "M"; // Millions
  } else {
    return number.toFixed(2).toLocaleString(); // Default formatting
  }
}

function elementExists(selector) {
  return $(selector).length > 0;
}

$(document).ready(function () {
  hideLoader();

  // Handle button click event with jQuery
  $("#fetch-button").click(fetchData);

  // Get the company quick info numbers that need to be formatted
  if (elementExists("#quick-data-shares")) {
    var shares_outstanding_str = $("#quick-data-shares").text();
    console.log("Shares:", shares_outstanding_str);
    var formattedShares = formatNumberAbbreviation(shares_outstanding_str);
    $("#quick-data-shares")
      .text("")
      .append($("<strong>").text(formattedShares));
  }

  if (elementExists("#quick-data-market-cap")) {
    var market_cap_str = $("#quick-data-market-cap").text();
    console.log("Market Cap:", market_cap_str);
    var formattedMarketCap = formatNumberAbbreviation(market_cap_str);
    $("#quick-data-market-cap")
      .text("")
      .append($("<strong>").text(formattedMarketCap));
  }



  // Set the text for the popover messages
  $("#dcf-info-popover").attr("data-html", "true");
  $("#dcf-info-popover").attr("title", dcfHelpInfo);
  $("#lynch-info-popover").attr("data-html", "true");
  $("#lynch-info-popover").attr("title", lynchHelpInfo);
  $("#ben-graham-info-popover").attr("data-html", "true");
  $("#ben-graham-info-popover").attr("title", benGrahamInfo);
  $("#graham-number-info-popover").attr("data-html", "true");
  $("#graham-number-info-popover").attr("title", grahamNumInfo);
  $("#multiples-valuation-info-popover").attr("data-html", "true");
  $("#multiples-valuation-info-popover").attr("title", multiplesValuationInfo);


  // Hold onto the old values for the forms, so if we click off and its null its the old value
  var old_dcf_eps_growth_rate_value = $("#dcf-eps-growth-entry").val();
  var old_dcf_discount_rate_value = $("#discount-rate-entry").val();
  var old_dcf_terminal_growth_value = $("#terminal-growth-entry").val();
  var old_dcf_margin_of_safety_value = $("#margin-of-safety-entry").val();

  var old_peter_lynch_eps_growth = $("#lynch-eps-growth-entry").val();

  var old_ben_graham_eps_growth = $("#lynch-eps-growth-entry").val();

  // Handle company summary popover message
  $("#company-summary").popover({ trigger: "hover" });
  $("#dcf-info-popover").popover({ trigger: "hover" });
  $("#lynch-info-popover").popover({ trigger: "hover" });
  $("#ben-graham-info-popover").popover({trigger: "hover"});
  $("#graham-number-info-popover").popover({trigger: "hover"});
  $("#multiples-valuation-info-popover").popover({trigger: "hover"});


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
        if (!isNaN(new_eps_growth) && new_eps_growth.trim() !== "") {
          this.value = new_eps_growth;
          updateDCF();
        } else {
          this.value = old_dcf_eps_growth_rate_value;
        }
      }
    })
    .on("blur", function () {
      console.log("Handling blur: ");
      var new_eps_growth = this.value;
      if (!isNaN(new_eps_growth) && new_eps_growth.trim() !== "") {
        this.value = new_eps_growth;
        updateDCF();
      } else {
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
        if (!isNaN(discountRate) && discountRate.trim() !== "") {
          this.value = discountRate;
          updateDCF();
        } else {
          this.value = old_dcf_discount_rate_value;
        }
      }
    })
    .on("blur", function () {
      console.log("Handling blur: ");
      var discountRate = this.value;
      if (!isNaN(discountRate) && discountRate.trim() !== "") {
        this.value = discountRate;
        updateDCF();
      } else {
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
        // Update if not null
        if (!isNaN(terminal_growth) && terminal_growth.trim() !== "") {
          this.value = terminal_growth;
          updateDCF();
        } else {
          this.value = old_dcf_terminal_growth_value;
        }
      }
    })
    .on("blur", function () {
      console.log("Handling blur: ");
      var terminal_growth = this.value;
      if (!isNaN(terminal_growth) && terminal_growth.trim() !== "") {
        this.value = terminal_growth;
        updateDCF();
      } else {
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
        if (!isNaN(marginOfSafety) && marginOfSafety.trim() !== "") {
          this.value = marginOfSafety;
          updateDCF();
        } else {
          this.value = old_dcf_margin_of_safety_value;
        }
      }
    })
    .on("blur", function () {
      console.log("Handling blur: ");
      var marginOfSafety = this.value;
      if (!isNaN(marginOfSafety) && marginOfSafety.trim() !== "") {
        this.value = marginOfSafety;
        updateDCF();
      } else {
        this.value = old_dcf_margin_of_safety_value;
      }
    });

  // Peter lynch
  // Handle lynch eps growth rate input
  $("#lynch-eps-growth-entry")
    .on("keydown", function (event) {
      if (event.key == "Enter") {
        console.log("Handling enter event with jQuery: " + event.key);
        event.preventDefault();

        var new_eps_growth = this.value;
        if (!isNaN(new_eps_growth) && new_eps_growth.trim() !== "") {
          this.value = new_eps_growth;
          updatePeterLynch();
        } else {
          this.value = old_peter_lynch_eps_growth;
        }
      }
    })
    .on("blur", function () {
      console.log("Handling blur: ");
      var new_eps_growth = this.value;
      if (!isNaN(new_eps_growth) && new_eps_growth.trim() !== "") {
        this.value = new_eps_growth;
        updatePeterLynch();
      } else {
        this.value = old_peter_lynch_eps_growth;
      }
    });

  // Ben graham calc
  // Handle Ben graham calc
  $("#ben-graham-eps-growth-entry")
    .on("keydown", function (event) {
      if (event.key == "Enter") {
        console.log("Handling enter event with jQuery: " + event.key);
        event.preventDefault();

        var new_eps_growth = this.value;
        if (!isNaN(new_eps_growth) && new_eps_growth.trim() !== "") {
          this.value = new_eps_growth;
          updateBenGraham();
        } else {
          this.value = old_ben_graham_eps_growth;
        }
      }
    })
    .on("blur", function () {
      console.log("Handling blur: ");
      var new_eps_growth = this.value;
      if (!isNaN(new_eps_growth) && new_eps_growth.trim() !== "") {
        this.value = new_eps_growth;
        updateBenGraham();
      } else {
        this.value = old_ben_graham_eps_growth;
      }
    });
});
