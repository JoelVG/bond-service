from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from bonds.utils import currency_exchange
from bonds.models import Bond


class TestBonds(APITestCase):    
    def setUp(self):
        user = User.objects.create(username='bond')
        user.set_password('bondjamesbond')
        user.save()
        buyer = User.objects.create(username='bond-buyer')
        buyer.set_password('bondjamesbondbuyer')
        buyer.save()
        
        
    def _bondCreate(self, data):
        url = reverse('bonds-list') 
        return self.client.post(url, data=data)
    
    
    def test_create_bond(self):
        self.client.login(username='bond', password='bondjamesbond')
        data = {
            'seller':1, 'name':'bond test', 
            'quantity':100, 'price':300,
        } 
        response = self._bondCreate(data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['seller'], 1)
    
    
    def test_detail_bond(self):
        self.client.login(username='bond', password='bondjamesbond')
        seller = User.objects.get(username='bond')
        instance = Bond.objects.create(seller=seller, name='bond-n', quantity=200, price=1000)
        self.assertIsNotNone(instance.id)
        
        url = reverse('bonds-detail', args=[instance.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'],'bond-n')
        
    
    def test_create_without_auth(self):
        data = {
            'seller':1, 'name':'bond test', 
            'quantity':100, 'price':300,
        }  
        response = self._bondCreate(data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        
    def test_detail_bond_without_auth(self):
        seller = User.objects.get(username='bond')
        instance = Bond.objects.create(seller=seller, name='bond-n', quantity=200, price=1000)
        self.assertIsNotNone(instance.id)
        
        url = reverse('bonds-detail', args=[instance.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    
    def test_create_bond_without_name(self):
        self.client.login(username='bond', password='bondjamesbond')
        data = {
            'seller':1, 'name':'', 
            'quantity':100, 'price':300,
        }  
        response = self._bondCreate(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
    
    def test_create_bond_with_quantity_out_of_range_min(self):
        self.client.login(username='bond', password='bondjamesbond')
        data = {
            'seller':1, 'name':'good_bond', 
            'quantity':-1, 'price':300,
        }  
        response = self._bondCreate(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_create_bond_with_quantity_out_of_range_max(self):
        self.client.login(username='bond', password='bondjamesbond')
        data = {
            'seller':1, 'name':'good_bond', 
            'quantity':10001, 'price':300,
        }  
        response = self._bondCreate(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    def test_create_bond_with_price_out_of_range_min(self):
        self.client.login(username='bond', password='bondjamesbond')
        url = reverse('bonds-list')
        data = {
            'seller':1, 'name':'good_bond', 
            'quantity':-1, 'price':300,
        }  
        response = self.client.post(url, data=data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_create_bond_with_price_out_of_range_max(self):
        self.client.login(username='bond', password='bondjamesbond')
        data = {
            'seller':1, 'name':'good_bond', 
            'quantity':10001, 'price':100000001,
        }  
        response = self._bondCreate(data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        
    def test_buy_bond(self):
        self.client.login(username='bond-buyer', password='bondjamesbondbuyer')
        create = reverse('bonds-list')
        data = {
            'seller':1, 'name':'good_bond', 
            'quantity':1000, 'price':100000,
        }
        self.client.post(create, data=data)
        buyer_id = int(self.client.session['_auth_user_id'])
        data['buyer'] = buyer_id
        buy = reverse('bonds-buy', args={1})
        response = self.client.put(buy)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['buyer'], buyer_id)
        
    
    def test_list_bonds_in_usd(self):
        self.client.login(username='bond-buyer', password='bondjamesbondbuyer')
        data_1 = {
            'seller':1, 'name':'good_bond', 
            'quantity':1000, 'price':100000,
        }
        data_2 = {
            'seller':2, 'name':'really good bond', 
            'quantity':100, 'price':10000,
        }
        prices = (data_1['price'], data_2['price'])
        self._bondCreate(data_1)
        self._bondCreate(data_2)
        current_exchange = currency_exchange()
        list_usd = reverse('bonds-list')+'?currency=USD'
        response = self.client.get(list_usd)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        for i, r in enumerate(response.data):
            self.assertAlmostEqual(float(r['price']), float(prices[i]/current_exchange))