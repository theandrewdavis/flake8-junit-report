import os
import xml.etree.cElementTree as ET


def _parse(file_name):
    lines = tuple(open(file_name, 'r'))
    parsed = []

    for line in lines:
        splitted = line.split(":")
        parsed.append({
            'file': splitted[0].strip(),
            'line': splitted[1].strip(),
            'col': splitted[2].strip(),
            'detail': splitted[3].strip(),
            'code': splitted[3].strip()[:4]
        })

    return parsed


def _convert(origin, destination):
    parsed = _parse(origin)

    if len(parsed) < 1:
        return

    testsuite = ET.Element("testsuite")
    testsuite.attrib["errors"] = str(len(parsed))
    testsuite.attrib["failures"] = "0"
    testsuite.attrib["name"] = "flake8 failures"
    testsuite.attrib["tests"] = str(len(parsed))
    testsuite.attrib["time"] = "1"

    for line in parsed:
        # todo
        # Mover file, line, col, etc a testcase y quitar de testsuite
        testcase = ET.SubElement(testsuite, "testcase", file=line['file'],
                                 line=line['line'], col=line['col'])

        ET.SubElement(testcase, "error", message=line['detail'],
                      type="flake8 %s" % line['code']).text = line['detail']

    tree = ET.ElementTree(testsuite)
    tree.write(destination, encoding='utf-8', xml_declaration=True)
