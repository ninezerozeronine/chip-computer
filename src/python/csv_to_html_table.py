import csv

output = []
output.append("<table id=\"machine_code\">")

HEADER_TEMPLATE = "    <th onclick=\"sortTable({header_index})\"><span>{header}</span></th>"

with open('../../machine-code.csv') as f:
    reader = csv.reader(f)
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
            for column in row:
                output.append("    <td>{column}</td>".format(
                    column=column
                    )
                )
            output.append("  </tr>")

output.append("</table>")

print "\n".join(output)
