from django.test import TestCase
from lists.models import Item, List

from lists.views import home_page  

class HomePageTest(TestCase):

	def test_home_page_retrns_correct_html(self):
		response = self.client.get('/')
		self.assertTemplateUsed(response, 'home.html')
		
class ListItemModelsTest(TestCase):
	def test_saving_and_retreiving_ites(self):
		list_=List()
		list_.save()
		
		first_item = Item()
		first_item.text='the first(ever)item'
		first_item.list = list_
		first_item.save()
		
		second_item = Item()
		second_item.text='item the second'
		second_item.list = list_
		second_item.save()
		
		saved_list = List.objects.first()
		self.assertEqual(saved_list, list_)
		
		saved_items = Item.objects.all()
		self.assertEqual(saved_items.count(),2)
		
		first_saved_item = saved_items[0]
		second_saved_item = saved_items[1]
		self.assertEqual(first_saved_item.text, 'the first(ever)item')
		self.assertEqual(first_saved_item.list, list_)
		self.assertEqual(second_saved_item.text, 'item the second')
		self.assertEqual(second_saved_item.list, list_)
		
class ListViewTest(TestCase):
	
	def test_uses_list_template(self):
		list_=List.objects.create()
		response = self.client.get(f'/lists/{list_.id}/')
		self.assertTemplateUsed(response, 'list.html')
		
	def test_displays_all_items(self):
		correct_list=List.objects.create()
		Item.objects.create(text='fuck1', list=correct_list)
		Item.objects.create(text='fuck2', list=correct_list)
		other_list = List.objects.create()
		Item.objects.create(text='other1', list=other_list)
		Item.objects.create(text='other2', list=other_list)
		response = self.client.get(f'/lists/{correct_list.id}/')
		
		self.assertContains(response, 'fuck1')
		self.assertContains(response, 'fuck2')
		self.assertNotContains(response, 'other1')
		self.assertNotContains(response, 'other2')
	
	def test_passes_correct_list_to_template(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		response = self.client.get(f'/lists/{correct_list.id}/')
		self.assertEqual(response.context['list'], correct_list)  
	
class NewListTest(TestCase):
	def test_can_save_a_POST_request(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		
		self.client.post(
            f'/lists/{correct_list.id}/add_item',
            data={'item_text': 'A new item for an existing list'}
        )
		
		self.assertEqual(Item.objects.count(),1)
		new_item=Item.objects.first()
		self.assertEqual(new_item.text, 'A new item for an existing list')
		self.assertEqual(new_item.list, correct_list)
		
	def test_redirects_after_list_view(self):
		other_list = List.objects.create()
		correct_list = List.objects.create()
		
		response =  self.client.post(
			f'/lists/{correct_list.id}/add_item',
			data={'item_text': 'A new list item for existing list'}
		)
		
		self.assertRedirects(response, f'/lists/{correct_list.id}/')