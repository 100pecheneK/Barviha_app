from django.shortcuts import render
from django.http import HttpResponse

# Импорт Модулей для генерации XML
import xml.etree.cElementTree as ET
from xml.dom import minidom

from datetime import datetime
# Импорт моделей
from selling.models import Selling

import datetime
import re


# Отображение
def xml_feed(request):
    def prettify(elem):
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml()

    def cleanhtml(raw_html):
        cleanr = re.compile('<.*?>')
        cleantext = re.sub(cleanr, '', raw_html)
        return cleantext

    def create_xml_feed(objects):
        time = datetime.datetime.now().isoformat()
        grin = '+05:00'
        time = time.split(".")[0]
        time = time.replace(' ', 'T')
        time = time + grin

        reality_feed = ET.Element('realty-feed', xmlns='http://webmaster.yandex.ru/schemas/feed/realty/2010-06')
        generation_date = ET.SubElement(reality_feed, 'generation-date')
        generation_date.text = str(time)
        for ob in objects:
            selling_date = str(ob.selling_date).split("+")[0]
            selling_date = selling_date.replace(' ', 'T')
            selling_date = selling_date + grin

            selling_description = cleanhtml(ob.selling_description)

            offer = ET.SubElement(reality_feed, 'offer', internal_id=str(ob.id))

            offer__type = ET.SubElement(offer, 'type')
            offer__type.text = str(ob.selling_deal)
            offer__property_type = ET.SubElement(offer, 'property-type')
            offer__property_type.text = str('жилая')
            offer__category = ET.SubElement(offer, 'category')
            offer__category.text = str(ob.selling_apartment)
            offer__creation_date = ET.SubElement(offer, 'creation-date')
            offer__creation_date.text = str(selling_date)

            offer__location = ET.SubElement(offer, 'location')
            offer__location__country = ET.SubElement(offer__location, 'country')
            offer__location__country.text = 'Россия'
            offer__location__locality_name = ET.SubElement(offer__location, 'locality-name')
            offer__location__locality_name.text = 'Нижний Тагил'
            offer__location__sub_locality_name = ET.SubElement(offer__location, 'district')
            offer__location__sub_locality_name.text = str(ob.state_parent)
            offer__location__sub_locality_name__address = ET.SubElement(offer__location, 'address')
            offer__location__sub_locality_name__address.text = str(ob.selling_str) + ', ' + str(ob.selling_House_number)

            offer__sales_agent = ET.SubElement(offer, 'sales-agent')
            offer__sales_agent__category = ET.SubElement(offer__sales_agent, 'name')
            offer__sales_agent__category.text = str(ob.selling_user)
            offer__sales_agent__phone = ET.SubElement(offer__sales_agent, 'phone')
            offer__sales_agent__phone.text = str(ob.selling_phone)
            offer__sales_agent__category = ET.SubElement(offer__sales_agent, 'category')
            offer__sales_agent__category.text = 'агентство'

            offer__price = ET.SubElement(offer, 'price')
            offer__price__value = ET.SubElement(offer__price, 'value')
            selling_price = ob.selling_price
            if (selling_price == None):
                selling_price = 0
            offer__price__value.text = str(selling_price)
            offer__price__currency = ET.SubElement(offer__price, 'currency')
            offer__price__currency.text = 'RUB'

            offer__area = ET.SubElement(offer, 'area')
            offer__area__value = ET.SubElement(offer__area, 'value')
            selling_flat_area = ob.selling_flat_area
            if (selling_flat_area == None):
                selling_flat_area = 0
            offer__area__value.text = str(selling_flat_area)
            offer__area__unit = ET.SubElement(offer__area, 'unit')
            offer__area__unit.text = 'кв. м'
            offer__area__description = ET.SubElement(offer, 'description')
            offer__area__description.text = str(selling_description)

            offer__rooms = ET.SubElement(offer, 'rooms')
            offer__rooms.text = str(1)
            offer__floor = ET.SubElement(offer, 'floor')
            selling_floor = ob.selling_floor
            if (selling_floor == None):
                selling_floor = 1
            offer__floor.text = str(selling_floor)

            xml = prettify(reality_feed)
        return xml

    xml = Selling.objects.all()[:1]

    xml = create_xml_feed(xml)
    xml = xml.replace('internal_id', 'internal-id')

    return HttpResponse(xml, content_type='application/xml')
