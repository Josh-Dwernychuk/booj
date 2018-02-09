import csv
from datetime import datetime
import requests
from xml.etree import ElementTree


def get_xml_feed(url):
    ''' Method to request XML data from given url
        Args:
            url <str>: URL endpoint to be requested
        Returns:
            xml_response <str>: serialized xml response returned from endpoint
    '''
    response = requests.get(url)
    xml_response = response.text
    return xml_response


def parse_xml_feed_to_xml_tree(xml_response):
    ''' Method to parse XML data into an xml tree
        Args:
            xml_response <str>: serialized xml response returned from endpoint
        Returns:
            xml_tree <xml object>: parsed xml tree
    '''
    encoded_xml_string = xml_response.encode('utf-8').strip()
    xml_tree = ElementTree.fromstring(encoded_xml_string)
    return xml_tree


def parse_xml_data_by_year(xml_tree, year):
    ''' Method to remove xml data not posted within a given year
        Args:
            xml_tree <xml object>: parsed xml tree
            year <int>: specific DateListed year to be parsed
        Returns:
            xml_tree <xml object>: parsed xml tree with
                only data listed during the specified year
    '''
    for listing in xml_tree.findall('Listing'):
        listing_details = listing.find('ListingDetails')
        date_listed = listing_details.find('DateListed')
        date_listed_string = date_listed.text
        date_listed_datetime = datetime.strptime(
            date_listed_string,
            '%Y-%m-%d' + ' ' + '%H:%M:%S'
        )

        if date_listed_datetime.year != year:
            xml_tree.remove(listing)
    return xml_tree


def parse_xml_data_by_phrase(xml_tree, phrase):
    ''' Method to remove xml data that does not contain
        a specific phrase in the description
        Args:
            xml_tree <xml object>: parsed xml tree
            phrase <str>: specific phrase criteria for parsing
        Returns:
            xml_tree <xml object>: parsed xml tree with
                only descriptions containing the specified phrase
    '''
    for listing in xml_tree.findall('Listing'):
        basic_details = listing.find('BasicDetails')
        description = basic_details.find('Description')

        if phrase not in description.text:
            xml_tree.remove(listing)

    return xml_tree


def order_by_date_listed(xml_tree):
    ''' Method to order xml data by DateListed and place listings in a list
        Args:
            xml_tree <xml object>: parsed xml tree
        Returns:
            ordered_xml_data <li>: list of xml data objects ordered by DateListed
    '''
    date_listed_xml_data = []
    for node in xml_tree:
        date_listed = node.find('ListingDetails').find('DateListed').text
        date_listed_xml_data.append((date_listed, node))

    ordered_xml_data = sorted(date_listed_xml_data)
    return ordered_xml_data


def collect_appliance_sub_nodes_fom_listing(listing):
    ''' Method to extract appliance sub-nodes from xml listing object
        Args:
            listing <xml object>: Single listing object
        Returns:
            appliances_list <li>: List of appliances contained
                within listings object
    '''
    appliances_list = []
    if listing.find('RichDetails').find('Appliances') is not None:
        for appliance in listing.find('RichDetails').find('Appliances'):
            appliances_list.append(appliance.text)
    return appliances_list


def collect_room_sub_nodes_from_listing(listing):
    ''' Method to extract room sub-nodes from xml listing object
        Args:
            listing <xml object>: Single listing object
        Returns:
            rooms_list <li>: List of rooms contained
                within listings object
    '''
    rooms_list = []
    if listing.find('RichDetails').find('Rooms') is not None:
        for room in listing.find('RichDetails').find('Rooms'):
            rooms_list.append(room.text)
    return rooms_list


def collect_bathroom_sub_nodes_from_listing(listing):
    ''' Method to extract bathroom sub-nodes from xml listing object
        Args:
            listing <xml object>: Single listing object
        Returns:
            bathrooms_list <li>: List of tuples specifying the bathrooms contained
                within the listings object
    '''
    bathrooms_list = []

    full_bathrooms = listing.find('BasicDetails').find('FullBathrooms')
    if full_bathrooms is not None:
        bathrooms_list.append(('Full Bathrooms', full_bathrooms.text))

    half_bathrooms = listing.find('BasicDetails').find('HalfBathrooms')
    if half_bathrooms is not None:
        bathrooms_list.append(('Half Bathrooms', half_bathrooms.text))

    three_quarter_bathrooms = \
        listing.find('BasicDetails').find('ThreeQuarterBathrooms')
    if three_quarter_bathrooms is not None:
        bathrooms_list.append(('Three Quarter Bathrooms', three_quarter_bathrooms.text))

    return bathrooms_list


def create_csv(ordered_xml_data, filewrite_location):
    ''' Method to create a csv file from parsed xml data from endpoint
        Args:
            ordered_xml_data <li>: list of xml data objects ordered by DateListed
            filewrite_location <str>: path to write the completed csv file
    '''
    with open(filewrite_location, 'wb') as csvfile:
        filewriter = csv.writer(csvfile)

        filewriter.writerow([
            'MlsId',
            'MlsName',
            'DateListed',
            'StreetAddress',
            'Price',
            'Bedrooms',
            'Bathrooms',
            'Appliances',
            'Rooms',
            'Description',
        ])

        for date_listed, listing in ordered_xml_data:

            appliances_list = collect_appliance_sub_nodes_fom_listing(listing)
            rooms_list = collect_room_sub_nodes_from_listing(listing)
            bathrooms_list = collect_bathroom_sub_nodes_from_listing(listing)

            filewriter.writerow([
                listing.find('ListingDetails').find('MlsId').text,
                listing.find('ListingDetails').find('MlsName').text,
                date_listed,
                listing.find('Location').find('StreetAddress').text,
                listing.find('ListingDetails').find('Price').text,
                listing.find('BasicDetails').find('Bedrooms').text,
                str(bathrooms_list)[1:-1],
                str(appliances_list)[1:-1],
                str(rooms_list)[1:-1],
                listing.find('BasicDetails').find('Description').text[:199],
            ])


if __name__ == "__main__":
    '''Main method to:
            - collect xml data from endpoint
            - parse xml data to an xml tree
            - remove all nodes that were not listed within 2016
            - remove all nodes that do not contain the phrase 'and'
                within the description
            - order xml data by DateListed
            - write all data to a csv file stored at 'output_data/listings.csv'
    '''
    xml_response = get_xml_feed(
        'http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml'
    )
    xml_tree = parse_xml_feed_to_xml_tree(xml_response)
    xml_tree = parse_xml_data_by_year(xml_tree, 2016)
    xml_tree = parse_xml_data_by_phrase(xml_tree, 'and')
    ordered_xml_data = order_by_date_listed(xml_tree)
    create_csv(ordered_xml_data, 'output_data/listings.csv')
