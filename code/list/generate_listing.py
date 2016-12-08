import os
import argparse
from argparse import ArgumentParser

parser = ArgumentParser(description="Generate report from code")    
parser.add_argument("-d", dest="directory", required=True,
    help="input directory", metavar="DIRECTORY",
    type=str)

args = parser.parse_args()

directory = args.directory

html_escape_table = {
    "&": "&amp;",
    '"': "&quot;",
    "'": "&apos;",
    ">": "&gt;",
    "<": "&lt;",
    }

def html_escape(text):
    """Produce entities within text."""
    return "".join(html_escape_table.get(c,c) for c in text)

def generate_listing(directory):
    accepted_extensions = (".c", ".cpp", ".h")

    report = ""

    for root, dirs, files in os.walk(directory):
        for file_name in files:
            if file_name.endswith(accepted_extensions):
                path = os.path.join(root, file_name)
                with open(path, "r") as f:
                    report += "<h3>{}</h3>".format(file_name)
                    report += "<pre>{}</pre>".format(html_escape(f.read()))

    return report

with open(directory + "/report.html", "w") as f:
    print "Generating " + directory + "/report.html" + " ..."
    f.write(generate_listing(directory))
    f.close()
