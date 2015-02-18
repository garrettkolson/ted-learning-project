from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import unittest

class NewVisitorTest(unittest.TestCase):
	
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)
	
	def tearDown(self):
		self.browser.quit()

	def test_can_start_a_list_and_retrieve_it_later(self):
		# Garrett has heard about a cool new online to-do app. He goes to check out its homepage
		self.browser.get('http://localhost:8000')

		# He notices the page title and header mention to-do lists
		# Fix .title & header_text later
		self.assertIn('To-Do', self.browser.title)
		header_text = self.browser.find_element_by_tag_name('h1').text
		self.assertIn('To-Do', header_text)

		# He is invited to enter a to-do item straight away
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertEqual(
				inputbox.get_attribute('placeholder'),
				'Enter a to-do item'
		)

		# She types "Code like crazy" into a text box (Garrett's hobby is Python coding)
		inputbox.send_keys('Code like crazy')

		# When he hits enter, the page updates, and now the page lists "1: Code like crazy"
		# as an item in a to-do list
		inputbox.send_keys(Keys.ENTER)
		
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertTrue(
			any(row.text == '1: Code like crazy' for row in rows),
			"New to-do item did not appear in table"
		)
		# There is still a text box inviting him to add another item. He enters
		# "Code more and more and more!" (Garrett is very persistant)
		self.fail('Finish the test!')

		# The page updates again, and now shows both items on his list

# Garrett wonders whether the site will remember his list. Then he sees that the site
# has generated a unique URL for him -- there is some explanatory text to that effect.

# He visits that URL - his to-do list is still there.

# Satisfied, he goes back to sleep

if __name__ == '__main__':
	unittest.main(warnings='ignore')