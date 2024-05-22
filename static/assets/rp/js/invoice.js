window.onload = function () {
  var today = new Date().toISOString().split("T")[0];
  var dateInput = document.getElementsByName("visitingdate")[0];
  dateInput.setAttribute("min", today);
  dateInput.setAttribute("max", today);
  dateInput.value = today;
};

function populateDoctors() {
  var patientType = document.getElementById("patient-type").value;
  var doctorDropdown = document.getElementById("doctor-select");
  doctorDropdown.innerHTML = "";

  if (patientType === "ODP") {
    var doctors = [
      { name: "Doctor A", fee: 100 },
      { name: "Doctor B", fee: 200 },
      { name: "Doctor C", fee: 300 },
    ];
  } else if (patientType === "PD") {
    var doctors = [
      { name: "Doctor D", fee: 150 },
      { name: "Doctor E", fee: 250 },
      { name: "Doctor F", fee: 350 },
    ];
  } else if (patientType === "SD") {
    var doctors = [
      { name: "Doctor G", fee: 200 },
      { name: "Doctor H", fee: 300 },
      { name: "Doctor I", fee: 400 },
    ];
  }

  for (var i = 0; i < doctors.length; i++) {
    var option = document.createElement("option");
    option.value = doctors[i].fee; // Set fee as the option value
    option.text = doctors[i].name;
    doctorDropdown.add(option);
  }

  // Call calculateInvoice to update the fee display
  calculateInvoice();
}


function calculateInvoice() {
  var doctorFee = document.getElementById("doctor-select").value;
  var gstRate = 18;

  var feeWithoutGST = parseFloat(doctorFee);
  var gstAmount = (feeWithoutGST * gstRate) / 100;
  var totalFee = feeWithoutGST + gstAmount;

  document.getElementById("fee-without-gst").innerHTML = feeWithoutGST.toFixed(2);
  document.getElementById("gst-amount").innerHTML = gstAmount.toFixed(2);
  document.getElementById("total-fee").innerHTML = totalFee.toFixed(2);
}