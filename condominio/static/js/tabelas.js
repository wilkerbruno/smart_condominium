/*document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("search");
  const filter = document.getElementById("myTable");
  const currentPage = document.getElementById("page-info");
  const prevButton = document.getElementById("prev");
  const nextButton = document.getElementById("next");
  let currentRow = 0;
  let rowsPerPage = 9;

  input.addEventListener("keyup", function (event) {
    let filterValue = event.target.value.toUpperCase();
    let trs = filter.getElementsByTagName("tr");
    for (let i = 1; i < trs.length; i++) {
      let tds = trs[i].getElementsByTagName("td");
      let isVisible = false;
      for (let j = 0; j < tds.length; j++) {
        if (tds[j].textContent.toUpperCase().indexOf(filterValue) > -1) {
          isVisible = true;
          break;
        }
      }
      if (isVisible) {
        trs[i].style.display = "";
      } else {
        trs[i].style.display = "none";
      }
    }
  });

  function updatePageInfo() {
    currentPage.textContent = `. ${Math.ceil(currentRow / rowsPerPage) + 1} de ${Math.ceil(filter.rows.length / rowsPerPage)}`;
  }

  prevButton.addEventListener("click", () => {
    if (currentRow > 0) {
      currentRow -= rowsPerPage;
      if (currentRow < rowsPerPage) {
        prevButton.disabled = true;
      }
      nextButton.disabled = false;
    }
    updateTable();
    updatePageInfo();
  });

  nextButton.addEventListener("click", () => {
    currentRow += rowsPerPage;
    if (currentRow + rowsPerPage >= filter.rows.length) {
      nextButton.disabled = true;
    }
    prevButton.disabled = false;
    updateTable();
    updatePageInfo();
  });

  function updateTable() {
    for (let i = 1; i < filter.rows.length; i++) {
      filter.rows[i].style.display = "none";
      if (i >= currentRow && i < currentRow + rowsPerPage) {
        filter.rows[i].style.display = "";
      }
    }
  }

  // Add click event listener to each list item (table row)
  const tableBody = document.getElementById("myTableBody");
  tableBody.addEventListener("click", (event) => {
    if (event.target.tagName === "TR") {
      const rowIndex = event.target.rowIndex - 1; // Subtract 1 to exclude table header
      currentRow = rowIndex - (rowIndex % rowsPerPage);
      updateTable();
      updatePageInfo();
    }
  });

  updateTable();
  updatePageInfo();
});
*/

document.addEventListener("DOMContentLoaded", function () {
  const rowsPerPage = 5;
  const table = document.getElementById("myTableBody");
  const rows = Array.from(table.getElementsByTagName("tr"));
  const totalPages = Math.ceil(rows.length / rowsPerPage);
  let currentPage = 1;

  const pageNumbers = document.getElementById("page-numbers");
  const pageInfo = document.getElementById("page-info");

  function displayRowsForPage(page) {
    table.innerHTML = "";
    const start = (page - 1) * rowsPerPage;
    const end = start + rowsPerPage;
    const rowsToDisplay = rows.slice(start, end);

    rowsToDisplay.forEach(row => table.appendChild(row));
    updatePageInfo();
    highlightCurrentPage();
  }

  function updatePageInfo() {
    pageInfo.textContent = `Página ${currentPage} de ${totalPages}`;
  }

  function createPageButtons() {
    pageNumbers.innerHTML = "";
    for (let i = 1; i <= totalPages; i++) {
      const button = document.createElement("button");
      button.textContent = i;
      button.className = "page-button";
      button.addEventListener("click", () => {
        currentPage = i;
        displayRowsForPage(currentPage);
      });
      pageNumbers.appendChild(button);
    }
  }

  function highlightCurrentPage() {
    const buttons = document.querySelectorAll(".page-button");
    buttons.forEach((button, index) => {
      if (index === currentPage - 1) {
        button.classList.add("active");
      } else {
        button.classList.remove("active");
      }
    });
  }

  document.getElementById("prev").addEventListener("click", () => {
    if (currentPage > 1) {
      currentPage--;
      displayRowsForPage(currentPage);
    }
  });

  document.getElementById("next").addEventListener("click", () => {
    if (currentPage < totalPages) {
      currentPage++;
      displayRowsForPage(currentPage);
    }
  });

  createPageButtons();
  displayRowsForPage(currentPage);
});
