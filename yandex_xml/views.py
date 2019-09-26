from django.shortcuts import render
from django.http import HttpResponse

# Импорт Модулей для генерации XML
import xml.etree.cElementTree as ET
from xml.dom import minidom

from datetime import datetime
# Импорт моделей
from selling.models import Selling


# Отображение
def xml_feed(request):
    def prettify(elem):
        rough_string = ET.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml()

    def create_xml_feed(objects):
        reality_feed = ET.Element('realty-feed', xmlns='http://webmaster.yandex.ru/schemas/feed/realty/2010-06')
        generation_date = ET.SubElement(reality_feed, 'generation-date')
        generation_date.text = 'str(datetime.now())'
        for ob in objects:
            offer = ET.SubElement(reality_feed, 'offer', internal_id=str(ob.id))

            offer__type = ET.SubElement(offer, 'type')
            offer__type.text = str(ob.selling_deal)
            offer__property_type = ET.SubElement(offer, 'property-type')
            offer__property_type.text = str('жилая')
            offer__category = ET.SubElement(offer, 'category')
            offer__category.text = str(ob.selling_apartment)
            offer__creation_date = ET.SubElement(offer, 'creation-date')
            offer__creation_date.text = str(ob.selling_date)

            offer__location = ET.SubElement(offer, 'location')
            offer__location__country = ET.SubElement(offer__location, 'country')
            offer__location__country.text = 'Россия'
            offer__location__locality_name = ET.SubElement(offer__location, 'locality-name')
            offer__location__locality_name.text = 'Нижний Тагил'
            offer__location__sub_locality_name = ET.SubElement(offer__location, 'sub-locality-name')
            offer__location__sub_locality_name.text = str(ob.state_parent)
            offer__location__sub_locality_name__address = ET.SubElement(offer__location__sub_locality_name, 'address')
            offer__location__sub_locality_name__address.text = str(ob.selling_str) + ', ' + str(ob.selling_House_number)

            offer__sales_agent = ET.SubElement(offer__location, 'sales-agent')
            offer__sales_agent__category = ET.SubElement(offer__sales_agent, 'sales_agent')
            offer__sales_agent__category.text = str(ob.selling_user)
            offer__sales_agent__phone = ET.SubElement(offer__sales_agent, 'sales_agent')
            offer__sales_agent__phone.text = str(ob.selling_phone)
            offer__sales_agent__category = ET.SubElement(offer__sales_agent, 'sales_agent')
            offer__sales_agent__category.text = 'агентство'

            offer__price = ET.SubElement(offer, 'price')
            offer__price__value = ET.SubElement(offer__price, 'value')
            offer__price__value.text = str(ob.selling_price)
            offer__price__currency = ET.SubElement(offer__price, 'currency')
            offer__price__currency.text = 'RUB'

            offer__area = ET.SubElement(offer, 'area')
            offer__area__value = ET.SubElement(offer__area, 'value')
            offer__area__value.text = str(ob.selling_flat_area)
            offer__area__unit = ET.SubElement(offer__area, 'unit')
            offer__area__unit.text = 'кв. м'
            offer__area__description = ET.SubElement(offer__area, 'description')
            offer__area__description.text = str(ob.selling_description)

            offer__rooms = ET.SubElement(offer, 'rooms')
            offer__rooms.text = str(ob.selling_apartment)
            offer__floor = ET.SubElement(offer, 'floor')
            offer__floor.text = str(ob.selling_floor)

            xml = prettify(reality_feed)
        return xml

    xml = Selling.objects.all()

    xml = create_xml_feed(xml)
    xml.replace('internal_id', 'internal-id')

    return HttpResponse(xml, content_type='application/xml')
