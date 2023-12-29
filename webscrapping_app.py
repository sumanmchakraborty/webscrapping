import streamlit as st
import requests
import bs4
import re

def scrape_fairmont_website(url):
    res = requests.get(url)
    soup = bs4.BeautifulSoup(res.text, features='html.parser')
    link1 = soup.select('li.property-link')
    list_of_websites = [''.join(('https://www.fairmont.com', link.get('href'))) for link2 in link1 for link in link2]
    city_names = [re.search(r'/([^/]+)/$', url).group(1) for url in list_of_websites]
    return list_of_websites, city_names

def get_contact_info(website_url):
    res1 = requests.get(website_url)
    soup1 = bs4.BeautifulSoup(res1.text, features='html.parser')
    elements = soup1.select('div.header-description')
    text = ''.join([elements[i].getText() for i in range(0, len(elements))])
    final_text = re.sub(r'\n', '', text)
    tel_number_match = re.search(r'\+[\(?\d+\)?\s?\-?]+[\(?\d+\)?]+', final_text)
    email_ids = re.findall(r'[\w\.-]+@[\w\.-]+', final_text)
    return tel_number_match.group() if tel_number_match else None, email_ids

def main():
    st.title('Fairmont Website Scraper')
    st.write('This app extracts email and telephone number from the Fairmont website.')

    fairmont_url = 'https://www.fairmont.com/'
    list_of_websites, city_names = scrape_fairmont_website(fairmont_url)

    # Dropdown box for selecting a specific place
    selected_city = st.selectbox('Select a Fairmont City:', city_names)

    # Get the corresponding URL for the selected city
    selected_url = list_of_websites[city_names.index(selected_city)]

    st.subheader(f'Contact Information for {selected_city}:')
    st.write(f'Website: {selected_url}')
    tel_number, email_ids = get_contact_info(selected_url)
    st.write(f'Tel Number: {tel_number}' if tel_number else 'Tel Number: Not Found')
    st.write(f'Email IDs: {", ".join(email_ids)}' if email_ids else 'Email IDs: Not Found')

if __name__ == '__main__':
    main()
