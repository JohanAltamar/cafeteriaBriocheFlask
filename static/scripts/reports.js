const http = new EasyHTTP();
const url = server_url;

const datePickerContainer = document.getElementsByClassName(
  "date-picker-container"
)[0];
const reportContainer = document.getElementsByClassName(
  "report-viewer-container"
)[0];
window.addEventListener("DOMContentLoaded", () => {
  removeElements(reportContainer);
  removeElements(datePickerContainer);

  const datePickerLabel = document.createElement("label");
  datePickerLabel.classList.add("date-picker-label");
  datePickerLabel.innerText = "Fecha de Reporte";
  datePickerLabel.htmlFor = "date";

  const datePicker = document.createElement("input");
  datePicker.classList.add("date-picker");
  datePicker.name = "date";
  datePicker.type = "date";
  datePicker.id = "datePicker";
  let today = new Date();
  datePicker.value =
    today.getFullYear() + "-" + (today.getMonth() + 1) + "-" + today.getDate();
  const datePickerSearchButton = document.createElement("button");
  datePickerSearchButton.classList.add("date-picker-button");
  datePickerSearchButton.innerText = "Buscar";
  datePickerSearchButton.addEventListener("click", () =>
    handleSearchReportDateClick()
  );

  datePickerContainer.append(
    datePickerLabel,
    datePicker,
    datePickerSearchButton
  );
});

const handleSearchReportDateClick = () => {
  searchedDate = document.getElementById("datePicker").value;
  console.log(searchedDate);
  http
    .post(`${url}/admin/reports/${searchedDate}`, {})
    .then((data) => {
      console.log(data);
      removeElements(reportContainer);
      handleCreateReportTable(data);
    })
    .catch((error) => console.error(error));
};

const handleCreateReportTable = (data) => {
  const tableTitle = document.createElement("h3");
  tableTitle.innerText = "Reporte de Ventas";
  tableTitle.className = "title";

  const reportTable = document.createElement("table");

  var tableHeader = reportTable.createTHead();
  var row = tableHeader.insertRow(0);
  var cell = row.insertCell(0);
  cell.innerHTML = "<h4>Nro. Orden</h4>";
  cell = row.insertCell(1);
  cell.innerHTML = "<h4>Total Orden</h4>";
  cell = row.insertCell(2);
  cell.innerHTML = "<h4>Cajero</h4>";

  var tableBody = reportTable.createTBody();
  let r = 0;
  let total = 0;
  data.forEach((order) => {
    row = tableBody.insertRow(r);
    cell = row.insertCell(0);
    cell.innerHTML = order[0];
    cell = row.insertCell(1);
    cell.innerHTML = `$ ${order[1].toLocaleString("de-DE")}`;
    cell = row.insertCell(2);
    cell.innerHTML = order[2];
    r++;
    total += order[1];
  });

  var tableFooter = reportTable.createTFoot();
  row = tableFooter.insertRow(0);
  cell = row.insertCell(0);
  cell.innerHTML = "<h4>Total</h4>";
  cell = row.insertCell(1);
  cell.innerHTML = `$ ${total.toLocaleString("de-DE")}`;

  reportContainer.append(tableTitle, reportTable);
};

const removeElements = (component) => {
  while (component.hasChildNodes()) {
    component.removeChild(component.firstChild);
  }
};
