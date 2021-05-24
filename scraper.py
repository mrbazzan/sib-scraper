
import requests
from bs4 import BeautifulSoup
import re
import os


def _remove(text):
    for each_symbol in ['&', ':', '?', "'", '.', '(', ')', ',', '-']:
        text = text.replace(each_symbol, '')
    return text


def sib_knowledge_base(URL):
    try:
        URL
    except HTTPError as e:
        print(e)
    except URLError:
        print('The server could not be found')
    else:
        driver = requests.get(URL)
        html = driver.text
        soup = BeautifulSoup(html, 'html.parser')
        results = soup.findAll('div', {'class': "uagb-column__inner-wrap"})
        for result in results:
            title = result.find('h4', {'class': 'uagb-ifb-title'}).text
            try:
                os.makedirs(f'settle-in-berlin/{title}')
            except OSError:
                pass
            anecdote = result.find('p', {'class': 'uagb-ifb-desc'}).text
            the_section_li_tag = result.findAll('li')
            for link in the_section_li_tag:
                a_tag = link.find_next('a')
                each_text_file = _remove(a_tag.text)
                with open(f'settle-in-berlin/{title}/{each_text_file}.txt', 'a+', encoding='UTF-8') as f:
                    f.write(f"{title}: {anecdote}")
                    f.write(f"\n{a_tag.text}: {a_tag.attrs['href']}")
                    sib_each_catalogue(f, a_tag.attrs['href'])


def sib_each_catalogue(writer, URL):
    try:
        URL
    except HTTPError as e:
        print(e)
    except URLError:
        print('The server could not be found')
    else:
        driver = requests.get(URL)
        html = driver.text
        soup = BeautifulSoup(html, 'html.parser')
        section_soup = soup.find('section', {"class": "post-content"})

        # print(section_soup.find('h1').text)
        _page = section_soup.find('div', {"class": "text"})
        p_page = _page.find('p')
        writer.write(f'\n  {p_page.text}')
        # writer.write(f"\n  {p_page.find_next('p').text}")
        for h2 in soup.findAll('h2', {"class": ""}):
            writer.write(f"\n{h2.text}")
            # if h2.find('span').text.startswith('FAQ about'):
            #     break
            h2.clear()
            next_tag = h2.next
            while next_tag:
                tag = str(next_tag)
                if tag.startswith('<p>') or tag.startswith('<h3>') or tag.startswith('<h4>') or tag.startswith('<ul>'):
                    if tag.startswith('<p>'):
                        # try ..
                        writer.write(f"\n\t{next_tag.text}")
                    elif tag.startswith('<h3>'):
                        writer.write(f"\n\t{next_tag.text}")
                    elif tag.startswith('<h4'):
                        writer.write(f"\n\n{next_tag.text}")
                    elif tag.startswith('<ul>'):
                        writer.write(f"\n\n{next_tag.text}")
                        # li_tag = next_tag.findAll('li')
                        # for li in li_tag:

                    next_tag.clear()

                elif tag.startswith('<hr') or tag.startswith('<div>') or tag.startswith('<blockquote'):
                    next_tag.clear()

                next_tag = next_tag.next

                if tag.startswith('<h2>'):
                    writer.write('\n')
                    next_tag = None

                if '<div class="clear">' in tag:
                    return
            # if next element is <p>, print it's element
            # if next element is not <p>, but it is <h2> go to the next iter

            # print('next element: ', list(h2.next_siblings))  # very important.
            # print(h2.find_all_next('p', limit=3))


site = "https://www.settle-in-berlin.com/knowledge-base-wiki-moving-to-germany/"
sib_knowledge_base(site)

# sib_each_catalogue("https://www.settle-in-berlin.com/anmeldung/")
# sib_each_catalogue("https://www.settle-in-berlin.com/tax-id-germany/")

# TODO: Try to change for h2 in findx()... `sib_each_catalogue()` to <p>
