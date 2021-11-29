import utils as ut
from selenium import webdriver
from bs4 import BeautifulSoup

def msg(driver):
    driver.find_element_by_xpath("//*[@class='pv-s-profile-actions pv-s-profile-actions--send-in-mail button-secondary-large mr2 mt2']").click()
    subject="new subject"
    message="Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim."
    driver.find_element_by_xpath("//*[@class='ember-text-field msg-form__subject pl2 ember-view']").send_keys(subject)
    driver.find_element_by_xpath("//*[@class='msg-form__contenteditable t-14 t-black--light t-normal flex-grow-1']/p").send_keys(message)
    #driver.find_element_by_css_selector('.button-primary-large.ml1').click()
    driver.find_element_by_css_selector('.msg-overlay-bubble-header__control.js-msg-close').click()
   

def connect(driver):
    driver.find_element_by_xpath("//*[@class='pv-s-profile-actions pv-s-profile-actions--connect button-primary-large mr2 mt2']").click()
    driver.find_element_by_xpath("//*[@class='button-secondary-large mr1']").click()
    message="Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim."
    driver.find_element_by_xpath('.send-invite__custom-message').send_keys(message)
    #driver.find_element_by_css_selector('.button-primary-large.ml1').click()

def personal_info(soup):
    """Return dict of personal info about the user"""
    top_card = ut.one_or_default(soup, 'section.pv-top-card-section')

    personal_info = ut.get_info(top_card, {
        'name': 'h1.pv-top-card-section__name',
        'headline': '.pv-top-card-section__headline',
        'company': '.pv-top-card-v2-section__company-name',
        'school': '.pv-top-card-v2-section__school-name',
        'location': '.pv-top-card-section__location',
        'summary': 'p.pv-top-card-section__summary-text'
    })
    followers_text = ut.text_or_default(soup,
                                     '.pv-recent-activity-section__follower-count-text', '')
    personal_info['followers'] = followers_text.replace(
        'followers', '').strip()
    return personal_info

def interests(soup):
    """
    Returns:
        list of person's interests
    """
    container = ut.one_or_default(soup, '.pv-interests-section')
    interests = ut.all_or_default(container, 'ul > li')
    interests = map(lambda i: ut.text_or_default(
        i, '.pv-entity__summary-title'), interests)
    return list(interests)

def accomplishments(soup):
    """
    Returns:
        dict of professional accomplishments including:
            - publications
            - cerfifications
            - patents
            - courses
            - projects
            - honors
            - test scores
            - languages
            - organizations
    """
    accomplishments = dict.fromkeys([
        'publications', 'certifications', 'patents',
        'courses', 'projects', 'honors',
        'test_scores', 'languages', 'organizations'
    ])
    container = ut.one_or_default(soup, '.pv-accomplishments-section')
    for key in accomplishments:
        accs = ut.all_or_default(container, 'section.' + key + ' ul > li')
        accs = map(lambda acc: acc.get_text() if acc else None, accs)
        accomplishments[key] = list(accs)
    return accomplishments
    
    
def skills(soup):
    """
    Returns:
        list of skills {name: str, endorsements: int} in decreasing order of
        endorsement quantity.
    """
    skills = soup.select('.pv-skill-category-entity__skill-wrapper')
    skills = list(map(ut.get_skill_info, skills))

    # Sort skills based on endorsements.  If the person has no endorsements
    def sort_skills(x): return int(
        x['endorsements'].replace('+', '')) if x['endorsements'] else 0
    return sorted(skills, key=sort_skills, reverse=True)

def experiences(soup):
    """
    Returns:
        dict of person's professional experiences.  These include:
            - Jobs
            - Education
            - Volunteer Experiences
    """
    experiences = {}
    container = ut.one_or_default(soup, '.background-section')

    jobs = ut.all_or_default(
        container, '#experience-section ul .pv-position-entity')
    jobs = list(map(ut.get_job_info, jobs))
    jobs = ut.flatten_list(jobs)
    experiences['jobs'] = jobs

    schools = ut.all_or_default(
        container, '#education-section .pv-education-entity')
    schools = list(map(ut.get_school_info, schools))
    experiences['education'] = schools

    volunteering = ut.all_or_default(
        container, '.pv-profile-section.volunteering-section .pv-volunteering-entity')
    volunteering = list(map(ut.get_volunteer_info, volunteering))
    experiences['volunteering'] = volunteering

    return experiences