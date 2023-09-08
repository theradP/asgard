import scrapy


class EbaySpider(scrapy.Spider):
    name = "ebay"
    # allowed_domains = ["www.ebay.co.uk"]
    start_urls = ["https://www.ebay.co.uk/b/bn_7023493315"]

    def parse(self, response):
        product_links = response.xpath('//a[@class="s-item__link"]/@href').getall()
        if product_links:
            yield from response.follow_all(product_links, callback=self.parse_page)
        next_page = response.xpath('//a[@aria-label="Go to next search page"]/@href').get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def parse_page(self, response):
        product_title = ''.join(response.xpath('//h1[@class="x-item-title__mainTitle"]/span/text()').getall())
        product_price = ''.join(response.xpath('//div[@class="x-price-primary"]/span/text()').getall())
        images = ' , '.join(response.xpath('//div[@class="ux-image-filmstrip-carousel"]//img/@src').getall())
        spec_container = response.xpath('//div[@class="ux-layout-section-evo ux-layout-section--features"]//div[@class="ux-labels-values__labels"]')
        all_spec = []
        for container in spec_container:
            label = ''.join(container.xpath('.//text()').getall())
            value_ = ''.join(container.xpath('./following-sibling::div[1][@class="ux-labels-values__values"]//text()').getall())
            all_spec.append(label+' '+value_)
        all_spec = ' | '.join(all_spec)

        yield {
            'product_title': product_title ,
            'product_price': product_price,
            'images': images,
            'specifications': all_spec,
        }

