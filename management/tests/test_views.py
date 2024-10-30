from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from management.models import Laptop, LaptopReview, SellerReview

User = get_user_model()


# TEST PER LE VIEWS
class UserTests(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(username='buyer', password='password', user_type='buyer')
        self.seller = User.objects.create_user(username='seller', password='password', user_type='seller')
        self.laptop = Laptop.objects.create(
            name='Test Laptop',
            processor_brand='Intel',
            processor_model='i5',
            ram=8,
            storage=256,
            display_inches=15,
            price=1000.00,
            category='BL',
            seller=self.seller
        )

    def test_register(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'ciaoBro1',
            'password2': 'ciaoBro1',
            'user_type': 'buyer'
        })
        # Stampa la risposta per il debug
        #print(response.content)
        # Assicurati che il codice di stato sia 302
        self.assertEqual(response.status_code, 302)
        # Verifica che l'utente sia stato creato
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'buyer',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect after login
        self.assertEqual(str(response.wsgi_request.user), 'buyer')

    def test_add_laptop_as_seller(self):
        self.client.login(username='seller', password='password')
        response = self.client.post(reverse('add_laptop'), {
            'name': 'New Laptop',
            'processor_brand': 'AMD',
            'processor_model': 'Ryzen 5',
            'ram': 16,
            'storage': 512,
            'display_inches': 15,
            'price': 1200.00,
            'category': 'GA',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertTrue(Laptop.objects.filter(name='New Laptop').exists())

    def test_add_laptop_review(self):
        self.client.login(username='buyer', password='password')
        response = self.client.post(reverse('laptop_review', args=[self.laptop.id]), {
            'rating': 5,
            'description': 'Great laptop!'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertTrue(LaptopReview.objects.filter(laptop=self.laptop, user=self.buyer).exists())

    def test_access_seller_dashboard(self):
        self.client.login(username='seller', password='password')
        response = self.client.get(reverse('seller_dashboard', args=[self.seller.id]))
        self.assertEqual(response.status_code, 200)  # Should return the dashboard page

    def test_access_seller_dashboard_without_login(self):
        response = self.client.get(reverse('seller_dashboard', args=[self.seller.id]))
        self.assertEqual(response.status_code, 302)  # Should redirect to login

    def test_laptop_detail_view(self):
        response = self.client.get(reverse('laptop_detail', args=[self.laptop.id]))
        self.assertEqual(response.status_code, 200)  # Should return the laptop detail page

    def test_search_laptops(self):
        response = self.client.get(reverse('search'), {'name': 'Test Laptop'})
        self.assertEqual(response.status_code, 200)  # Should return search results
        self.assertContains(response, 'Test Laptop')

    def test_add_seller_review(self):
        self.client.login(username='buyer', password='password')
        response = self.client.post(reverse('seller_review', args=[self.seller.id, self.laptop.id]), {
            'rating': 4,
            'description': 'Good seller!'
        })
        self.assertEqual(response.status_code, 302)  # Should redirect
        self.assertTrue(SellerReview.objects.filter(seller=self.seller, user=self.buyer).exists())
