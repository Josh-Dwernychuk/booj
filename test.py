import csv

from booj import get_xml_feed, parse_xml_feed_to_xml_tree, \
    parse_xml_data_by_year, parse_xml_data_by_phrase, \
    order_by_date_listed, create_csv


def test_get_xml_feed():
    ''' Test xml endpoint request '''
    xml_response = get_xml_feed(
        'http://syndication.enterprise.websiteidx.com/feeds/BoojCodeTest.xml'
    )
    assert len(xml_response) >= 1


def test_parse_xml_feed_to_xml_tree():
    ''' Test parsing of xml to xml tree '''
    file = open("test.xml", "r")
    xml_response = file.read()

    xml_tree = parse_xml_feed_to_xml_tree(xml_response)

    assert xml_tree[0].find('Location').find('StreetAddress').text == '123 Test St.'
    assert xml_tree[0].find('ListingDetails').find('DateListed').text == '2016-08-29 00:00:00'
    assert xml_tree[0].find('ListingDetails').find('MlsId').text == '1'
    assert xml_tree[0].find('ListingDetails').find('MlsName').text == '2'
    assert xml_tree[0].find('ListingDetails').find('Price').text == '3'
    assert xml_tree[0].find('BasicDetails').find('Description').text == 'sample description'
    assert xml_tree[0].find('BasicDetails').find('Bedrooms').text == '4'
    assert xml_tree[0].find('BasicDetails').find('FullBathrooms').text == '15'
    assert xml_tree[0].find('BasicDetails').find('HalfBathrooms').text == '16'
    assert xml_tree[0].find('BasicDetails').find('ThreeQuarterBathrooms').text == '17'
    assert xml_tree[0].find('RichDetails').find('Appliances')[0].text == 'Appliance1'
    assert xml_tree[0].find('RichDetails').find('Rooms')[0].text == 'Room1'
    assert xml_tree[0].find('RichDetails').find('Rooms')[1].text == 'Room2'

    assert xml_tree[1].find('Location').find('StreetAddress').text == '456 Other Test St.'
    assert xml_tree[1].find('ListingDetails').find('DateListed').text == '2015-09-18 00:00:00'
    assert xml_tree[1].find('ListingDetails').find('MlsId').text == '8'
    assert xml_tree[1].find('ListingDetails').find('MlsName').text == '9'
    assert xml_tree[1].find('ListingDetails').find('Price').text == '10'
    assert xml_tree[1].find('BasicDetails').find('Description').text == \
        'and another sample description'
    assert xml_tree[1].find('BasicDetails').find('Bedrooms').text == '11'
    assert xml_tree[1].find('BasicDetails').find('FullBathrooms').text == '18'
    assert xml_tree[1].find('BasicDetails').find('HalfBathrooms').text == '19'
    assert xml_tree[1].find('BasicDetails').find('ThreeQuarterBathrooms').text == '20'
    assert xml_tree[1].find('RichDetails').find('Appliances')[0].text == 'Appliance2'
    assert xml_tree[1].find('RichDetails').find('Appliances')[1].text == 'Appliance3'
    assert xml_tree[1].find('RichDetails').find('Rooms')[0].text == 'Room3'


def test_parse_xml_data_by_year():
    ''' Test xml data parsing by year '''
    file = open("test.xml", "r")
    xml_response = file.read()

    xml_tree = parse_xml_feed_to_xml_tree(xml_response)
    xml_tree = parse_xml_data_by_year(xml_tree, 2016)

    assert len(xml_tree) == 1

    assert xml_tree[0].find('Location').find('StreetAddress').text == '123 Test St.'
    assert xml_tree[0].find('ListingDetails').find('DateListed').text == '2016-08-29 00:00:00'
    assert xml_tree[0].find('ListingDetails').find('MlsId').text == '1'
    assert xml_tree[0].find('ListingDetails').find('MlsName').text == '2'
    assert xml_tree[0].find('ListingDetails').find('Price').text == '3'
    assert xml_tree[0].find('BasicDetails').find('Description').text == 'sample description'
    assert xml_tree[0].find('BasicDetails').find('Bedrooms').text == '4'
    assert xml_tree[0].find('BasicDetails').find('FullBathrooms').text == '15'
    assert xml_tree[0].find('BasicDetails').find('HalfBathrooms').text == '16'
    assert xml_tree[0].find('BasicDetails').find('ThreeQuarterBathrooms').text == '17'
    assert xml_tree[0].find('RichDetails').find('Appliances')[0].text == 'Appliance1'
    assert xml_tree[0].find('RichDetails').find('Rooms')[0].text == 'Room1'
    assert xml_tree[0].find('RichDetails').find('Rooms')[1].text == 'Room2'


def test_parse_xml_data_by_phrase():
    ''' Test xml data parsing by phrase '''
    file = open("test.xml", "r")
    xml_response = file.read()

    xml_tree = parse_xml_feed_to_xml_tree(xml_response)
    xml_tree = parse_xml_data_by_phrase(xml_tree, 'and')

    assert len(xml_tree) == 1

    assert xml_tree[0].find('Location').find('StreetAddress').text == '456 Other Test St.'
    assert xml_tree[0].find('ListingDetails').find('DateListed').text == '2015-09-18 00:00:00'
    assert xml_tree[0].find('ListingDetails').find('MlsId').text == '8'
    assert xml_tree[0].find('ListingDetails').find('MlsName').text == '9'
    assert xml_tree[0].find('ListingDetails').find('Price').text == '10'
    assert xml_tree[0].find('BasicDetails').find('Description').text == \
        'and another sample description'
    assert xml_tree[0].find('BasicDetails').find('Bedrooms').text == '11'
    assert xml_tree[0].find('BasicDetails').find('FullBathrooms').text == '18'
    assert xml_tree[0].find('BasicDetails').find('HalfBathrooms').text == '19'
    assert xml_tree[0].find('BasicDetails').find('ThreeQuarterBathrooms').text == '20'
    assert xml_tree[0].find('RichDetails').find('Appliances')[0].text == 'Appliance2'
    assert xml_tree[0].find('RichDetails').find('Appliances')[1].text == 'Appliance3'
    assert xml_tree[0].find('RichDetails').find('Rooms')[0].text == 'Room3'


def test_order_by_date_listed():
    ''' Test ordering by DateListed of xml data'''
    file = open("test.xml", "r")
    xml_response = file.read()

    xml_tree = parse_xml_feed_to_xml_tree(xml_response)
    ordered_xml_data = order_by_date_listed(xml_tree)

    assert len(ordered_xml_data) == 2

    assert ordered_xml_data[0][1].find('Location').find('StreetAddress').text == \
        '456 Other Test St.'
    assert ordered_xml_data[0][1].find('ListingDetails').find('DateListed').text == \
        '2015-09-18 00:00:00'
    assert ordered_xml_data[0][1].find('ListingDetails').find('MlsId').text == '8'
    assert ordered_xml_data[0][1].find('ListingDetails').find('MlsName').text == '9'
    assert ordered_xml_data[0][1].find('ListingDetails').find('Price').text == '10'
    assert ordered_xml_data[0][1].find('BasicDetails').find('Description').text == \
        'and another sample description'
    assert ordered_xml_data[0][1].find('BasicDetails').find('Bedrooms').text == '11'
    assert ordered_xml_data[0][1].find('BasicDetails').find('FullBathrooms').text == '18'
    assert ordered_xml_data[0][1].find('BasicDetails').find('HalfBathrooms').text == '19'
    assert ordered_xml_data[0][1].find('BasicDetails').find('ThreeQuarterBathrooms').text == '20'
    assert ordered_xml_data[0][1].find('RichDetails').find('Appliances')[0].text == 'Appliance2'
    assert ordered_xml_data[0][1].find('RichDetails').find('Appliances')[1].text == 'Appliance3'
    assert ordered_xml_data[0][1].find('RichDetails').find('Rooms')[0].text == 'Room3'

    assert ordered_xml_data[1][1].find('Location').find('StreetAddress').text == '123 Test St.'
    assert ordered_xml_data[1][1].find('ListingDetails').find('DateListed').text == \
        '2016-08-29 00:00:00'
    assert ordered_xml_data[1][1].find('ListingDetails').find('MlsId').text == '1'
    assert ordered_xml_data[1][1].find('ListingDetails').find('MlsName').text == '2'
    assert ordered_xml_data[1][1].find('ListingDetails').find('Price').text == '3'
    assert ordered_xml_data[1][1].find('BasicDetails').find('Description').text == \
        'sample description'
    assert ordered_xml_data[1][1].find('BasicDetails').find('Bedrooms').text == '4'
    assert ordered_xml_data[1][1].find('BasicDetails').find('FullBathrooms').text == '15'
    assert ordered_xml_data[1][1].find('BasicDetails').find('HalfBathrooms').text == '16'
    assert ordered_xml_data[1][1].find('BasicDetails').find('ThreeQuarterBathrooms').text == '17'
    assert xml_tree[0].find('RichDetails').find('Appliances')[0].text == 'Appliance1'
    assert xml_tree[0].find('RichDetails').find('Rooms')[0].text == 'Room1'
    assert xml_tree[0].find('RichDetails').find('Rooms')[1].text == 'Room2'


def test_create_csv():
    ''' Test CSV creation '''
    file = open("test.xml", "r")
    xml_response = file.read()

    xml_tree = parse_xml_feed_to_xml_tree(xml_response)
    ordered_xml_data = order_by_date_listed(xml_tree)
    create_csv(ordered_xml_data, 'test_output_data/test_listings.csv')

    with open('test_output_data/test_listings.csv', 'rb') as csvfile:
        csv_reader = csv.reader(csvfile)

        csv_data = []
        for row in csv_reader:
            csv_data.append(row)

        assert csv_data[0][0] == 'MlsId'
        assert csv_data[0][1] == 'MlsName'
        assert csv_data[0][2] == 'DateListed'
        assert csv_data[0][3] == 'StreetAddress'
        assert csv_data[0][4] == 'Price'
        assert csv_data[0][5] == 'Bedrooms'
        assert csv_data[0][6] == 'Bathrooms'
        assert csv_data[0][7] == 'Appliances'
        assert csv_data[0][8] == 'Rooms'
        assert csv_data[0][9] == 'Description'

        assert csv_data[1][0] == '8'
        assert csv_data[1][1] == '9'
        assert csv_data[1][2] == '2015-09-18 00:00:00'
        assert csv_data[1][3] == '456 Other Test St.'
        assert csv_data[1][4] == '10'
        assert csv_data[1][5] == '11'
        assert csv_data[1][6] == \
            "('Full Bathrooms', '18'), ('Half Bathrooms', '19'), ('Three Quarter Bathrooms', '20')"
        assert csv_data[1][7] == \
            "'Appliance2', 'Appliance3'"
        assert csv_data[1][8] == "'Room3'"
        assert csv_data[1][9] == 'and another sample description'

        assert csv_data[2][0] == '1'
        assert csv_data[2][1] == '2'
        assert csv_data[2][2] == '2016-08-29 00:00:00'
        assert csv_data[2][3] == '123 Test St.'
        assert csv_data[2][4] == '3'
        assert csv_data[2][5] == '4'
        assert csv_data[2][6] == \
            "('Full Bathrooms', '15'), ('Half Bathrooms', '16'), ('Three Quarter Bathrooms', '17')"
        assert csv_data[2][7] == "'Appliance1'"
        assert csv_data[2][8] == "'Room1', 'Room2'"
        assert csv_data[2][9] == 'sample description'
