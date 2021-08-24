import logging
from crawler.items import NewEvents
import scrapy
import re
from datetime import datetime


class NewEventSpider(scrapy.Spider):
    name = 'new_event'
    allowed_domains = ["vsd.vn"]
    domain = "https://vsd.vn"
    page = 5

    def start_requests(self):
        self.current_date = datetime.today().strftime('%d/%m/%Y')
        # self.current_date = '23/08/2021'
        url = f'https://vsd.vn/vi/alo/ISSUER?page={self.page}'
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        logging.info("Start parse response")
        messageEvents = NewEvents()
        events = []
        list_new = response.css('#d_list_news').css('li')
        is_continue = True
        if len(list_new)  == 0:
            return
        for new_event in list_new:
            event = {}
            event['title'] = new_event.css('a::text').get()
            event['link'] = self.domain + new_event.css('a').attrib['href']

            event['date'] = new_event.css('.time-news::text').get()
            date_str = self.extract_date(event['date'])

            if date_str == self.current_date:
                events.append(event)
            else:
                is_continue = False
                break
        messageEvents['events'] = self.format_message_to_mattermost(events)

        yield messageEvents
        if is_continue:
            self.page += 1
            link = f'https://vsd.vn/vi/alo/ISSUER?page={self.page}'
            logging.info("Find in next page" + link)
            # yield scrapy.Request(link, callback=self.parse)

    def extract_date(self, date):
        get_date = re.search("([0-9]{2}\/[0-9]{2}\/[0-9]{4})", date)
        return get_date[0]

    def format_message_to_mattermost(self, events):
        message = f' ##### New events. Time: {self.current_date} \n'
        if len(events) == 0:
            message += "Dont't have new events.\n"
            return message
        message += "| STT  | Title | Date |  Link  | \n"
        message += "| :--: |:--:|:--:| :---: | \n"
        for i, event in enumerate(events, 1):
            title = event['title']
            link = event['link']
            date = event['date']
            message += f'| {i}  | {title} | {date} | {link} | \n'
        return message
