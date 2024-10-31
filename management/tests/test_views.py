from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from management.models import Laptop, LaptopReview, SellerReview, Cart, CartItem, Order, OrderItem

User = get_user_model()



class AuthTests(TestCase):
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
            price=800.00,
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
        # Assicura che il codice di stato sia 302
        self.assertEqual(response.status_code, 302)
        # Verifica che l'utente sia stato creato
        self.assertTrue(User.objects.filter(username='newuser').exists())

    def test_register_with_too_common_password(self):
        response = self.client.post(reverse('register'), {
            'username': 'newuser',
            'password1': 'password',  # Password troppo comune
            'password2': 'password',
            'user_type': 'buyer'
        })
        # Assicura che il codice di stato sia 200, indicando che la pagina di registrazione è stata restituita
        self.assertEqual(response.status_code, 200)
        # Ottiene il modulo dalla risposta
        form = response.context['form']
        # Verifica che ci sia un errore nel campo 'password2'
        self.assertTrue(form.errors['password2'])  # Assicura che ci sia un errore
        self.assertIn('This password is too common.', form.errors['password2'])  # Assicura che il messaggio di errore sia corretto

    def test_login(self):
        response = self.client.post(reverse('login'), {
            'username': 'buyer',
            'password': 'password'
        })
        self.assertEqual(response.status_code, 302)  # Dopo il login dovrebbe ridirezionare
        self.assertEqual(str(response.wsgi_request.user), 'buyer')

    def test_login_with_incorrect_credentials(self):
        response = self.client.post(reverse('login'), {
            'username': 'wronguser',
            'password': 'wrongpassword'
        })
        # Assicura che il codice di stato sia 200, indicando che la pagina di login è stata restituita
        self.assertEqual(response.status_code, 200)
        # Verifica che il messaggio di errore corretto sia presente nella risposta
        self.assertContains(response, 'Please enter a correct username and password. Note that both fields may be case-sensitive.')



class LaptopCreateViewTests(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(username='buyer', password='password1', user_type='buyer')
        self.seller = User.objects.create_user(username='seller', password='password1', user_type='seller')
        self.laptop = Laptop.objects.create(
            name='Test Laptop',
            processor_brand='Intel',
            processor_model='i5',
            ram=8,
            storage=256,
            display_inches=15,
            price=800.00,
            category='BL',
            seller=self.seller
        )
    def test_add_laptop_as_seller_without_image(self):
        self.client.login(username='seller', password='password1')
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
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Laptop.objects.filter(name='New Laptop').exists())

    def test_add_laptop_as_seller_with_image(self):
        self.client.login(username='seller', password='password1')
        with open(r'C:\Users\damor\PycharmProjects\Laptop_ecommerce\management\tests\files\mba13-m2-midnight-gallery1-202402.jpeg', 'rb') as image:
            response = self.client.post(reverse('add_laptop'), {
                'name': 'New Laptop with image',
                'processor_brand': 'Intel',
                'processor_model': 'i7',
                'ram': 16,
                'storage': 512,
                'display_inches': 15,
                'price': 1200.00,
                'image': image,
                'category': 'GA',
            })
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Laptop.objects.filter(name='New Laptop with image').exists())

    def test_add_laptop_as_buyer_forbidden(self):
        # Effettua il login come buyer
        self.client.login(username='buyer', password='password1')
        # Tenta di creare un laptop
        response = self.client.post(reverse('add_laptop'), {
            'name': 'Forbidden Laptop',
            'processor_brand': 'Intel',
            'processor_model': 'i3',
            'ram': 4,
            'storage': 128,
            'display_inches': 13,
            'price': 800.00,
            'category': 'BL',
        })
        # Verifica che il codice di stato sia 403 Forbidden
        self.assertEqual(response.status_code, 403)
        # Assicura che il laptop non sia stato creato
        self.assertFalse(Laptop.objects.filter(name='Forbidden Laptop').exists())

    def test_add_laptop_with_missing_fields(self):
        self.client.login(username='seller', password='password1')
        response = self.client.post(reverse('add_laptop'), {
            'name': '',  # Nome vuoto
            'processor_brand': 'AMD',
            'processor_model': 'Ryzen 5',
            'ram': 16,
            'storage': 512,
            'display_inches': 15,
            'price': 1200.00,
            'category': 'GA',
        })
        # Assicura che il codice di stato sia 200, indicando che la pagina è stata restituita
        # Dovrebbe ritornare la pagina add laptop
        self.assertEqual(response.status_code, 200)
        # Ottiene il modulo dalla risposta
        form = response.context['form']
        # Verifica che ci sia un errore nel campo 'name'
        self.assertTrue(form.errors['name'])
        # Assicura che ci sia un errore
        # Assicura che il messaggio di errore sia corretto
        self.assertIn('This field is required.', form.errors['name'])



class ReviewsTests(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(username='buyer', password='password2', user_type='buyer')
        self.seller = User.objects.create_user(username='seller', password='password2', user_type='seller')
        self.laptop = Laptop.objects.create(
            name='Test Laptop',
            processor_brand='Intel',
            processor_model='i5',
            ram=8,
            storage=256,
            display_inches=15,
            price=800.00,
            category='BL',
            seller=self.seller
        )

    def test_add_laptop_review(self):
        self.client.login(username='buyer', password='password2')
        response = self.client.post(reverse('laptop_review', args=[self.laptop.id]), {
            'rating': 5,
            'description': 'Great laptop!'
        })
        self.assertEqual(response.status_code, 302)  # Dovrebbe ridirezionare
        self.assertTrue(LaptopReview.objects.filter(laptop=self.laptop, user=self.buyer).exists())



class DashboardTests(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(username='buyer', password='password3', user_type='buyer')
        self.seller = User.objects.create_user(username='seller', password='password3', user_type='seller')
        self.laptop = Laptop.objects.create(
            name='Test Laptop',
            processor_brand='Intel',
            processor_model='i5',
            ram=8,
            storage=256,
            display_inches=15,
            price=800.00,
            category='BL',
            seller=self.seller
        )

    def test_access_seller_dashboard(self):
        self.client.login(username='seller', password='password3')
        response = self.client.get(reverse('seller_dashboard', args=[self.seller.id]))
        self.assertEqual(response.status_code, 200)  # Dovrebbe ritornare la pagina dashboard

    def test_access_seller_dashboard_without_login(self):
        response = self.client.get(reverse('seller_dashboard', args=[self.seller.id]))
        self.assertEqual(response.status_code, 302)  # Dovrebbe ridirezionare al login

    def test_access_seller_dashboard_as_buyer_forbidden(self):
        self.client.login(username='buyer', password='password3')
        response = self.client.get(reverse('seller_dashboard', args=[self.seller.id]))
        self.assertEqual(response.status_code, 403)  # Dovrebbe riornare forbidden


class LaptopDetailViewTests(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(username='buyer', password='password4', user_type='buyer')
        self.seller = User.objects.create_user(username='seller', password='password4', user_type='seller')
        self.laptop = Laptop.objects.create(
            name='Test Laptop',
            processor_brand='Intel',
            processor_model='i5',
            ram=8,
            storage=256,
            display_inches=15,
            price=800.00,
            category='BL',
            seller=self.seller
        )

    def test_laptop_detail_view(self):
        response = self.client.get(reverse('laptop_detail', args=[self.laptop.id]))
        self.assertEqual(response.status_code, 200)  # Dovrebbe ritornare la pagina laptop detail

    def test_laptop_detail_view_without_login(self):
        response = self.client.get(reverse('laptop_detail', args=[self.laptop.id]))
        self.assertEqual(response.status_code, 200)  # Dovrebbe ritornare la pagina laptop detail


class SearchTests(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(username='buyer', password='password5', user_type='buyer')
        self.seller = User.objects.create_user(username='seller', password='password5', user_type='seller')
        self.laptop = Laptop.objects.create(
            name='Test Laptop',
            processor_brand='Intel',
            processor_model='i5',
            ram=8,
            storage=256,
            display_inches=15,
            price=800.00,
            category='BL',
            seller=self.seller
        )

    def test_search_exact_match(self):
        response = self.client.get(reverse('search'), {'name': 'Test Laptop'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Laptop')

    def test_search_partial_match(self):
        response = self.client.get(reverse('search'), {'name': 'Laptop'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Laptop')

    def test_search_case_insensitive(self):
        response = self.client.get(reverse('search'), {'name': 'test laptop'})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Test Laptop')



class SellerReviews(TestCase):
    def setUp(self):
        self.buyer = User.objects.create_user(username='buyer', password='password6', user_type='buyer')
        self.seller = User.objects.create_user(username='seller', password='password6', user_type='seller')
        self.laptop = Laptop.objects.create(
            name='Test Laptop',
            processor_brand='Intel',
            processor_model='i5',
            ram=8,
            storage=256,
            display_inches=15,
            price=800.00,
            category='BL',
            seller=self.seller
        )

    def test_add_seller_review(self):
        self.client.login(username='buyer', password='password6')
        response = self.client.post(reverse('seller_review', args=[self.seller.id, self.laptop.id]), {
            'rating': 4,
            'description': 'Good seller!'
        })
        self.assertEqual(response.status_code, 302)  # Dovrebbe ridirezionare
        self.assertTrue(SellerReview.objects.filter(seller=self.seller, user=self.buyer).exists())

    def test_add_seller_review_as_seller_redirect(self):
        # Effettua il login come seller
        self.client.login(username='seller', password='password6')
        # Tenta di aggiungere una recensione per un altro seller
        response = self.client.post(reverse('seller_review', args=[self.seller.id, self.laptop.id]), {
            'rating': 3,
            'description': 'Trying to review as a seller'
        })
        # Verifica che il seller sia stato reindirizzato alla home
        self.assertRedirects(response, reverse('home'))
        # Assicura che la recensione non sia stata creata
        self.assertFalse(SellerReview.objects.filter(seller=self.seller, user=self.seller).exists())



class CartViewsTests(TestCase):
    def setUp(self):
        # Creazione di utenti buyer e seller
        self.buyer = User.objects.create_user(username='buyer', password='password', user_type='buyer')
        self.seller = User.objects.create_user(username='seller', password='password', user_type='seller')

        # Creazione di un laptop
        self.laptop = Laptop.objects.create(
            name='Test Laptop',
            processor_brand='Intel',
            processor_model='i5',
            ram=8,
            storage=256,
            display_inches=15,
            price=1000,
            category='GA',
            seller=self.seller
        )

        # Creazione di un carrello per il buyer
        self.cart = Cart.objects.create(user=self.buyer)

    def test_add_to_cart_as_buyer(self):
        self.client.login(username='buyer', password='password')
        response = self.client.post(reverse('add_to_cart', args=[self.laptop.id]))

        # Verifica del reindirizzamento e della presenza di CartItem
        self.assertEqual(response.status_code, 302)
        cart_item = CartItem.objects.filter(cart=self.cart, laptop=self.laptop).first()
        self.assertIsNotNone(cart_item)
        self.assertEqual(cart_item.quantity, 1)

    def test_add_to_cart_as_seller_redirects(self):
        self.client.login(username='seller', password='password')
        response = self.client.post(reverse('add_to_cart', args=[self.laptop.id]))

        # Verifica che il seller venga reindirizzato alla home e che non sia stato creato nessun CartItem
        self.assertRedirects(response, reverse('home'))
        self.assertFalse(CartItem.objects.filter(cart__user=self.seller).exists())

    def test_cart_detail_as_buyer(self):
        self.client.login(username='buyer', password='password')
        response = self.client.get(reverse('cart_detail'))

        # Verifica che la risposta contenga la pagina del carrello
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Carrello')

    def test_cart_detail_as_seller_redirects(self):
        self.client.login(username='seller', password='password')
        response = self.client.get(reverse('cart_detail'))

        # Verifica che il seller venga reindirizzato alla home
        self.assertRedirects(response, reverse('home'))

    def test_increase_quantity(self):
        # Aggiunta iniziale di un laptop al carrello
        CartItem.objects.create(cart=self.cart, laptop=self.laptop, quantity=1)

        self.client.login(username='buyer', password='password')
        response = self.client.post(reverse('increase_quantity', args=[self.laptop.id]))

        # Verifica che la quantità sia aumentata
        cart_item = CartItem.objects.get(cart=self.cart, laptop=self.laptop)
        self.assertEqual(cart_item.quantity, 2)

    def test_decrease_quantity(self):
        # Aggiunta iniziale di un laptop al carrello
        CartItem.objects.create(cart=self.cart, laptop=self.laptop, quantity=2)

        self.client.login(username='buyer', password='password')
        response = self.client.post(reverse('decrease_quantity', args=[self.laptop.id]))

        # Verifica che la quantità sia diminuita
        cart_item = CartItem.objects.get(cart=self.cart, laptop=self.laptop)
        self.assertEqual(cart_item.quantity, 1)

        # Decrementa la quantità a zero e verifica l'eliminazione del CartItem
        response = self.client.post(reverse('decrease_quantity', args=[self.laptop.id]))
        self.assertFalse(CartItem.objects.filter(cart=self.cart, laptop=self.laptop).exists())

    def test_remove_from_cart(self):
        CartItem.objects.create(cart=self.cart, laptop=self.laptop, quantity=1)

        self.client.login(username='buyer', password='password')
        response = self.client.post(reverse('remove_from_cart', args=[self.laptop.id]))

        # Verifica che il CartItem sia stato eliminato
        self.assertFalse(CartItem.objects.filter(cart=self.cart, laptop=self.laptop).exists())

    def test_checkout_view(self):
        CartItem.objects.create(cart=self.cart, laptop=self.laptop, quantity=1)

        self.client.login(username='buyer', password='password')
        response = self.client.get(reverse('checkout'))

        # Verifica che la pagina di checkout mostri gli articoli del carrello
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Riepilogo Ordine')

    def test_confirm_order(self):
        CartItem.objects.create(cart=self.cart, laptop=self.laptop, quantity=1)

        self.client.login(username='buyer', password='password')
        response = self.client.post(reverse('confirm_order'))

        # Verifica che l'ordine sia stato creato e che il carrello sia svuotato
        self.assertEqual(Order.objects.filter(user=self.buyer).count(), 1)
        self.assertFalse(CartItem.objects.filter(cart=self.cart).exists())

        # Verifica che OrderItem sia stato creato con il laptop e la quantità corretti
        order = Order.objects.get(user=self.buyer)
        order_item = OrderItem.objects.get(order=order, laptop=self.laptop)
        self.assertEqual(order_item.quantity, 1)
        self.assertEqual(order_item.price, self.laptop.price)
