document.getElementById("fetch-data").addEventListener("click", () => {
  fetch("http://192.168.5.119/EnergieManagement/DigitaleMeter/")
    .then((response) => {
      if (!response.ok) {
        throw new Error("Network response was not ok " + response.statusText);
      }
      return response.json();
    })
    .then((data) => displayData(data))
    .catch((error) => console.error("Error fetching data:", error));
});

function displayData(data) {
  const display = document.getElementById("data-display");
  display.innerHTML = ""; // Clear previous data

  for (const key in data) {
    const value = data[key].value;
    const unit = data[key].unit ? ` ${data[key].unit}` : "";
    const item = document.createElement("div");
    item.className = "data-item";
    item.textContent = `${key}: ${value}${unit}`;
    display.appendChild(item);
  }
}
