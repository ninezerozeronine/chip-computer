import csv

output = []

beginning = """<!DOCTYPE html>
<html>
<head>
<title>Eight Bit Computer Language Table</title>
<style>
  table {
    border-collapse: collapse;
    font-family: Courier New;
  }

  table, th, td {
    border: 1px solid #ddd;
  }

  th {
    cursor: pointer;
    vertical-align: bottom;
    text-align: center;
  }
  
  th span 
  {
    -ms-writing-mode: tb-rl;
    -webkit-writing-mode: vertical-rl;
    writing-mode: vertical-rl;
    transform: rotate(180deg);
    white-space: nowrap;
  }
  
  th, td {
    text-align: left;
    padding: 2px;
    white-space: nowrap;
  }
  
  tr:nth-child(even) {
    background-color: #f2f2f2
  }
</style>
"""

end = """
<!-- Taken from https://www.w3schools.com/howto/howto_js_sort_table.asp -->

<script>
function sortTable(n) {
  var table, rows, switching, i, x, y, shouldSwitch, dir, switchcount = 0;
  table = document.getElementById("language_table");
  switching = true;
  //Set the sorting direction to ascending:
  dir = "asc"; 
  /*Make a loop that will continue until
  no switching has been done:*/
  while (switching) {
    //start by saying: no switching is done:
    switching = false;
    rows = table.rows;
    /*Loop through all table rows (except the
    first, which contains table headers):*/
    for (i = 1; i < (rows.length - 1); i++) {
      //start by saying there should be no switching:
      shouldSwitch = false;
      /*Get the two elements you want to compare,
      one from current row and one from the next:*/
      x = rows[i].getElementsByTagName("TD")[n];
      y = rows[i + 1].getElementsByTagName("TD")[n];
      /*check if the two rows should switch place,
      based on the direction, asc or desc:*/
      if (dir == "asc") {
        if (x.innerHTML.toLowerCase() > y.innerHTML.toLowerCase()) {
          //if so, mark as a switch and break the loop:
          shouldSwitch= true;
          break;
        }
      } else if (dir == "desc") {
        if (x.innerHTML.toLowerCase() < y.innerHTML.toLowerCase()) {
          //if so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
    }
    if (shouldSwitch) {
      /*If a switch has been marked, make the switch
      and mark that a switch has been done:*/
      rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
      switching = true;
      //Each time a switch is done, increase this count by 1:
      switchcount ++;      
    } else {
      /*If no switching has been done AND the direction is "asc",
      set the direction to "desc" and run the while loop again.*/
      if (switchcount == 0 && dir == "asc") {
        dir = "desc";
        switching = true;
      }
    }
  }
}
</script>
</body>
</html>"""


output.append(beginning)
output.append("<table id=\"language_table\">")

HEADER_TEMPLATE = "    <th onclick=\"sortTable({header_index})\"><span>{header}</span></th>"

with open('../docs/_static/language_table.csv') as csv_file:
    reader = csv.reader(csv_file)
    for row_index, row in enumerate(reader):
        if row_index == 0:
            output.append("  <tr>")
            for header_index, header in enumerate(row):
                output.append(HEADER_TEMPLATE.format(
                    header_index=header_index,
                    header=header
                    )
                )
            output.append("  </tr>")
        else:
            output.append("  <tr>")
            row_content = []
            for column in row:
                row_content.append("<td>{column}</td>".format(
                    column=column
                    )
                )
            final_row = "    {tds}".format(tds="".join(row_content))
            output.append(final_row)
            output.append("  </tr>")

output.append("</table>")
output.append(end)

with open("../docs/_static/language_table.html", "w") as html_file:
    html_file.write("\n".join(output))

# print "\n".join(output)
