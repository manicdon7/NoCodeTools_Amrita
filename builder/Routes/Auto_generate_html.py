from .Tool.Html_Datas.Datas import *
from .Tool.Html_Datas.base import *
from random import choice
# from Tool.Tools import get_image_url, listof_get_image_url
import random
from bs4 import BeautifulSoup
import requests
from googlesearch import search


def get_image_url(keyword):
    url = f"https://www.google.com/search?q={keyword}&tbm=isch"

    # Make a GET request to the URL and get the HTML content
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    image_urls = set()
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url:
            image_urls.add(img_url)
    return list(image_urls)[0]


def listof_get_image_url(keyword, len):
    url = f"https://www.google.com/search?q={keyword}&tbm=isch"

    # Make a GET request to the URL and get the HTML content
    response = requests.get(url)
    html_content = response.content

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(html_content, 'html.parser')
    image_urls = set()
    for img in soup.find_all('img'):
        img_url = img.get('src')
        if img_url:
            image_urls.add(img_url)
    return list(image_urls)[0:len]


class Make_web:
    def __init__(self, query, ProjectName, TitleOftheDocument=False) -> None:
        # Set the project setting.....
        self.Query = query

        # Theme of the porject
        self.Theme = ProjectName

        if TitleOftheDocument:
            self.DocTitle = TitleOftheDocument
        else:
            self.DocTitle = ProjectName
        self.ProjectName = ProjectName

        # initialize the requrements
        self.Logo = ""
        self.Menu = choice(Menus)
        self.hero = choice(Hero)
        self.about = choice(About)
        self.footer = choice(Footer)
        self.ContactUs = choice(Contactus)
        self.cards = choice(Cards)

    def create_page(self):

        self.code = ''
        # create code......

        self.code = self.code + \
            self.add_section(self.Tailwin_Operation(self.Menu))
        self.code = self.code + \
            self.add_section(self.Tailwin_Operation(self.hero))
        self.code = self.code + \
            self.add_section(self.Tailwin_Operation(self.about))
        self.code = self.code + \
            self.add_section(self.Tailwin_Operation(self.ContactUs))
        self.code = self.code + \
            self.add_section(self.Tailwin_Operation(self.cards))
        self.code = self.code + \
            self.add_section(self.Tailwin_Operation(self.footer))

        Common_code = self.BaseCode(self.DocTitle, self.code)

        return self.change_Text(Common_code)

    def add_section(self, partOfcode):
        return f"""<section>{partOfcode}</section>"""

    def BaseCode(self, title, body):
        BaseCode = base_code
        Icon = f"{get_image_url(self.Theme)}".join(BaseCode.split('{-_-}'))
        Title = f"{title}".join(Icon.split('~~~'))
        Body = f"{body}".join(Title.split('~!~'))
        return Body

    def Tailwin_Operation(self, html):
        # Change The colors
        Colored_html = self.Tailwin_Random_Color_changer(html)
        # Change the images
        Image_Changed = self.change_images(Colored_html)

        return Image_Changed

    def Tailwin_Random_Color_changer(self, html):
        # Load the HTML code into Beautiful Soup
        soup = BeautifulSoup(html, 'html.parser')

        # Define a function to generate a random color class

        def random_color_class(prefix):
            # Choose a random color from the Tailwind CSS color palette
            colors = ['red', 'orange', 'yellow', 'green',
                      'teal', 'blue', 'indigo', 'purple', 'pink']
            color = random.choice(colors)
            # Choose a random shade from the Tailwind CSS color palette
            shades = ['100', '200', '300', '400',
                      '500', '600', '700', '800', '900']
            shade = random.choice(shades)
            # Combine the prefix, color, and shade into a class name
            return f'{prefix}-{color}-{shade}'

        # Find all elements with a bg- or text- color class and replace it with a random color class
        try:
            for elem in soup.find_all(class_=lambda c: c.startswith('bg-') or c.startswith('text-')):
                prefix = elem['class'][0].split('-')[0]
                elem['class'] = [random_color_class(prefix)]
        except:
            pass

        # Print the modified HTML code
        return soup.prettify()

    def change_images(self, html):
        soup = BeautifulSoup(html, 'html.parser')

        # Find all img elements and replace their src attribute with a random image URL
        try:
            for img in soup.find_all('img'):
                img['src'] = choice(listof_get_image_url(
                    self.Theme, choice([i for i in range(choice([10, 15, 20]))])))
        except:
            pass

        # Print the modified HTML code
        return soup.prettify()

    def Fetch_the_Para_Content(self, query, num_results):
        search_urls = list(search(query, num_results=6))
        extracted_conten = []
        try:
            for url in search_urls:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                paragraphs = soup.find_all('p')
                extracted_content = ""
                for i in range(min(num_results, len(paragraphs))):
                    extracted_conten.append(paragraphs[i].text.strip() + " ")

                print(f"Content from {url}: {extracted_content}\n")
        except:
            print("Error are occer while fetching Content...")

        return extracted_conten

    def Fetch_the_HTag_Content(self, query, num_results, find_element):
        search_urls = list(search(query, num_results=6))
        extracted_conten = []
        try:
            for url in search_urls:
                response = requests.get(url)
                soup = BeautifulSoup(response.content, 'html.parser')
                paragraphs = soup.find_all(find_element)

                for i in range(min(num_results, len(paragraphs))):
                    extracted_conten.append(paragraphs[i].text.strip() + " ")
                    print(extracted_conten)
        except:
            print("Error are occer while fetching Content...")
        return extracted_conten

    def change_Text(self, html_doc):
        H_tags = ['h1', 'h2', 'h3', 'h4', 'h5', 'h6']
        # Parse the HTML document
        soup = BeautifulSoup(html_doc, "html.parser")
        p_tags = soup.find_all("p")
        content = self.Fetch_the_Para_Content(self.Theme, len(p_tags))
        try:
            for i, p_tag in enumerate(p_tags):
                p_tag.string = content[i][0:len(p_tag.text)]
        except:
            print("Error are occerd in Text.....")

        for i in H_tags:
            p_tags = soup.find_all(i)
            content = self.Fetch_the_HTag_Content(self.Theme, len(p_tags), i)
            try:
                for i, p_tag in enumerate(p_tags):
                    p_tag.string = content[i][0:len(p_tag.text)]
            except:
                print("Error are occerd in Text.....")

        return str(soup)
