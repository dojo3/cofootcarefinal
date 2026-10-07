"""Preserve the article supplied as IMG_7647.jpeg, transcribed column by column."""
import html
import json
import math
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
paragraphs = [
    'In the early 1990’s, quirky little health food stores could be found sprinkled around the country like natural cane sugar atop a bran muffin. I had the opportunity to work in this industry while attending nursing school. These stores were full of vitamins, herbal medicine, organic foods and interesting people. Experiences at this time cultivated my love of “holistic” medicine. Alongside of my education in natural healing, I learned allopathic medicine in nursing school. I witnessed the need for both schools of thought and this has since inspired me in my career as well as my healthy living lifestyle.',
    'At that time in history, buying vitamins, herbs and organic foods was considered “alternative”. Fast forward almost 30 years and all those products are considered mainstream and can easily be purchased at the local grocery store. There was a demand for natural products and the marketplace responded. The natural foods industry is only a sliver of what may be considered holistic or alternative medicine. Acupuncture, homeopathy, Qi Gong, and yoga are a few practices that were also considered alternative but are rapidly becoming more mainstream. I find this to be an exciting time when we have advances in medical technologies and breakthroughs as well as an embracing of ancient healing techniques.',
    'There are many practices and terminologies used that may cause some misconceptions about holistic medicine. First of all, holistic healing / medicine by definition looks at the whole person-body, mind, spirit and emotions and looks for root causes for disease as well as methods for wellness. Other terminology that may be substituted for the word holistic may be: alternative, complimentary, integrative, Eastern, or functional. The practices may be numerous, as I have listed a few above, and many have been practiced for thousands of years.',
    'In defining holistic medicine, we also need to look at the counterpart-modern medicine, and how it may differ. Modern medicine, also known as allopathic, Western, or conventional medicine has been practiced for the last 200 years. The importance of sanitation, understanding of infectious diseases, the discovery of antibiotics and other medications as well as surgery have saved lives worldwide.',
    'Modern medicine makes a huge impact of saving lives, especially in an acute health care crisis. However, at present, we have an assault of chronic diseases on the rise in the United States. Auto-immune disorders, diabetes and chronic pain are examples of health issues plaguing many Americans. Many people are turning to holistic medicine and addressing issues with diet and alleviating stress by use of alternative practices.',
    'By examining these explanations of conventional and complementary medicine, there may appear to be a polarity between the two. An interesting symbol of what I would view to be an integration of both is the symbol of modern medicine- the caduceus. The caduceus is a symbol with two serpents intertwined on a staff with two wings on the top. It is also the same symbol for kundalini yoga. In kundalini yoga, it is a representation of life force energy, balance, and consciousness. This could be a coincidence or it could be an illustration of holistic healing hidden in plain sight. I think it is a beautiful representation of what could become of modern medicine by incorporating more ancient healing techniques.',
    'For those interested in learning more about the world of holistic healing, a good place to start would be by visiting www.nccih.nih.gov. This is the website for the National Institute of Health/The National Center for Complementary and Integrative Health. This is a federal agency that is funded to research health practices that are not under the umbrella of conventional medicine. Information and studies can be found there and range from topics such as Aloe Vera to Transcendental Meditation.',
    'There are many medical doctors that practice integrative medicine as well as other practitioners in the health care field. You may find a Physician that also practices acupuncture. You may also find a Registered Nurse or Psychologist that practices Healing Touch. You may find a musician that teaches sound healing. The variety of healing modalities are as varied as are the education and background of the practitioner. Some healing techniques are not limited to those that have a medical background nor should they be. Healing is and should be available to anyone who seeks it.',
    'We are all health care consumers. As such, we all influence the health care market. Just as my story of the small health foods industry paving the way for health products on a larger scale, we all can impact the direction of health care. Recognizing that we are more than a physical / mechanical being and that health is something we can educate ourselves in and practice techniques of wellness is the giant step forward in the evolution of health care. It is also important to know what is happening in health care policy, get to know the issues and vote toward a better future in health care.',
    'Kirsten Antony is a Registered Nurse and holistic health care practitioner. Kirsten is certified in many healing modalities and offers her services in the Metro Denver area at a variety of facilities as well as making house calls. For more information please visit www.kirstenantony.com or call 303-668-8992.',
]
body = '\n'.join('<p>' + html.escape(p) + '</p>' for p in paragraphs)
words = len(re.findall(r'\S+', ' '.join(paragraphs)))
article = {
    'title': 'Integrating Holistic Medicine',
    'slug': 'integrating-holistic-medicine',
    'date': '2018',
    'date_label': 'Circa 2018 · Exact publication date unconfirmed',
    'date_note': 'The issue date is outside the photographed area. The approximate year is inferred from an adjacent advertisement for November 10, 2018; it is not a confirmed publication date.',
    'category': 'Healing arts',
    'publication': 'Prime Time News',
    'body_html': body,
    'words': words,
    'minutes': math.ceil(words / 200),
    'excerpt': 'Kirsten reflects on her nursing education, the changing place of holistic healing, and the relationship between conventional and complementary medicine.',
    'clipping': 'images/article-clippings/integrating-holistic-medicine.jpeg',
    'source_file': 'IMG_7647.jpeg',
    'preserved_on': '2026-10-07',
}
path = ROOT / 'data/articles.json'
articles = json.loads(path.read_text())
if not any(a['slug'] == article['slug'] for a in articles):
    articles.append(article)
    articles.sort(key=lambda a: a['date'], reverse=True)
    path.write_text(json.dumps(articles, ensure_ascii=False, indent=2) + '\n')
print('Preserved print article:', article['title'], words, 'words')
