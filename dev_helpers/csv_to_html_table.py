import csv

output = []
output.append("<table id=\"machine_code\">")

HEADER_TEMPLATE = "    <th onclick=\"sortTable({header_index})\"><span>{header}</span></th>"

with open('../../sphinx_docs/_static/language_table.csv') as f:
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

print "\n".join(output)
