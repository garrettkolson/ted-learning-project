from django.test import LiveServerTestCase
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

class NewVisitorTest(LiveServerTestCase):
	
	def setUp(self):
		self.browser = webdriver.Firefox()
		self.browser.implicitly_wait(3)
	
	def tearDown(self):
		self.browser.quit()
		
	def check_for_row_in_list_table(self, row_text):
		table = self.browser.find_element_by_id('id_list_table')
		rows = table.find_elements_by_tag_name('tr')
		self.assertIn(row_text, [row.text for row in rows])

	def test_can_start_a_list_and_retrieve_it_later(self):
		# Garrett has heard about a cool new online to-do app. He goes to check out its homepage
		self.browser.get(self.live_server_url)

		# He notices the page title and header mention to-do lists
		## Fix .title & header_text later
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

		# When he hits enter, he is taken to a new URL, and now the page lists "1: Code like crazy"
		# as an item in a to-do list table
		inputbox.send_keys(Keys.ENTER)
		garrett_list_url = self.browser.current_url
		self.assertRegex(garrett_list_url, '/lists/.+')
		self.check_for_row_in_list_table('1: Code like crazy')
		
		# There is still a text box inviting him to add another item. He enters
		# "Code something awesome" (Garrett is very persistant)
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Code something awesome')
		inputbox.send_keys(Keys.ENTER)

		# The page updates again, and now shows both items on his list
		self.check_for_row_in_list_table('1: Code like crazy')
		self.check_for_row_in_list_table('2: Code something awesome')

		# Now, a new user, Courtney, comes along to the site.
		
		## We use a new browser session to make sure that no information of 
		## Garrett's is coming through from cookies, etc. #
		self.browser.quit()
		self.browser = webdriver.Firefox()
		
		# Courtney visits the home page. There is no sign of Garrett's list.
		self.browser.get(self.live_server_url)
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Code like crazy', page_text)
		self.assertNotIn('Code something awesome', page_text)
		
		# Courtney starts a new list by entering a new item.
		inputbox = self.browser.find_element_by_id('id_new_item')
		inputbox.send_keys('Buy milk')
		inputbox.send_keys(Keys.ENTER)
		
		# Courtney gets her own unique URL.
		courtney_list_url = self.browser.current_url
		self.assertRegex(courtney_list_url, '/lists/.+')
		self.assertNotEqual(courtney_list_url, garrett_list_url)
		
		# Again, there is no trace of Garrett's list.
		page_text = self.browser.find_element_by_tag_name('body').text
		self.assertNotIn('Code like crazy', page_text)
		self.assertIn('Buy milk', page_text)
		
		# Satisfied, they both go back to sleep.
		
	def test_layout_and_styling(self):
		# Garrett goes to the home page.
		self.browser.get(self.live_server_url)
		self.browser.set_window_size(1024, 768)
		
		# He notices the input box is nicely centered
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=5)
		
		# He starts a new list and sees the input is nicely centered there too.
		inputbox.send_keys('testing\n')
		inputbox = self.browser.find_element_by_id('id_new_item')
		self.assertAlmostEqual(inputbox.location['x'] + inputbox.size['width'] / 2, 512, delta=5)