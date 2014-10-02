import xml.etree.ElementTree as ET
import csv
import glob
import io

def convert_to_unicode(x):
    if (x is not None):
        return x.encode('utf-8')
    return None

def convert_to_csv(id, status, title, desc, body, guide_links, see_also_links, writer):
    guide_links += ['']*5
    guide_links = guide_links[0:5]
    see_also_links += ['']*5
    see_also_links = see_also_links[0:5]

    writer.writerow(map(convert_to_unicode, [id, status, title, desc, body] + guide_links + see_also_links))


def parse_file(file_name, writer):
    tree = ET.parse(file_name)
    root = tree.getroot()

    NAMESPACE_PREFIX = '{http://projectmallard.org/1.0/}'

    # Extracting everything in the info element
    id = root.get('id')
    info = root.find(NAMESPACE_PREFIX + 'info')
    revision = info.find(NAMESPACE_PREFIX + 'revision')
    if (revision is not None):
        status = revision.get('status')
    else:
        status = ''

    desc = info.findtext(NAMESPACE_PREFIX + 'desc')
    guide_links = []
    see_also_links = []

    for link in info.findall(NAMESPACE_PREFIX + 'link'):
        if (link.get('type') == 'guide'):
            guide_links.append(link.get('xref'))
        elif (link.get('type') == 'seealso'):
            see_also_links.append(link.get('xref'))

    title = root.find(NAMESPACE_PREFIX + 'title').text

    # Iterate through body and concatenate all elements into a single string
    for element in list(root):
        if (element.tag == NAMESPACE_PREFIX + 'info' or element.tag == NAMESPACE_PREFIX + 'title' or element.tag == NAMESPACE_PREFIX + 'comment'):
            root.remove(element)

    body = ET.tostring(root)
    body_strings = body.split('\n')
    body_strings = body_strings[1:-1]
    body = ('\n').join(body_strings)

    convert_to_csv(id, status, title, desc, body, guide_links, see_also_links, writer)

ET.register_namespace('', 'http://projectmallard.org/1.0/')
ET.register_namespace('if', 'http://projectmallard.org/if/1.0/')
ET.register_namespace('ui', 'http://projectmallard.org/experimental/ui/')
ET.register_namespace('its', 'http://www.w3.org/2005/11/its')
ET.register_namespace('tt', 'http://www.w3.org/ns/ttml')

with open('test.csv', 'w') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['ID', 'Status', 'Title', 'Description', 'Body', 'Guide 1', 'Guide 2', 'Guide 3', 'Guide 4', 'Guide 5', 'Seealso 1', 'Seealso 2', 'Seealso 3', 'Seealso 4', 'Seealso 5'])

    files = glob.glob('./gnome-help/C/*.page')
    gs_files = glob.glob('../gnome-getting-started-docs/gnome-help/C/*.page')
    files += gs_files
    for file_name in files:
        parse_file(file_name, writer)

