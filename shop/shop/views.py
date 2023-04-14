from django.contrib import messages
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse, reverse_lazy

from orders.models import Cart, Order, OrderItem

from .forms import CartAddForm, ClientRegisterForm, OrderCreateForm, UserChangeForm, UserProfileForm
from .models import Author, Book
from .task import order_send


def register(request):
    if request.method == 'POST':
        form = ClientRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = ClientRegisterForm()
    return render(request, 'shop/register.html', {'form': form})


class CustomLoginView(LoginView):
    template_name = 'shop/login.html'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse('home')


def logout_view(request):
    logout(request)
    return redirect('home')


@login_required
def user_profile(request):
    user = request.user
    orders = Order.objects.filter(client=user).order_by('-created')
    context = {'user': user, 'orders': orders}
    return render(request, 'shop/user_profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        user_form = UserChangeForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save(commit=False)
            if not request.user.is_superuser and user.is_superuser:
                messages.error(request, 'Good try)!')
                return redirect('edit_profile')
            user.save()
            profile_form.save()
            messages.success(request, 'Your profile was updated successfully!')
            return redirect('edit_profile')
        else:
            messages.error(request, 'Please correct the error')
    else:
        user_form = UserChangeForm(instance=request.user)
        profile_form = UserProfileForm(instance=request.user)

    return render(request, 'shop/edit_profile.html', {'user_form': user_form, 'profile_form': profile_form})


class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'shop/password.html'
    success_url = reverse_lazy('edit_profile')


def book_list(request):
    genre = request.GET.get('genre')
    if genre:
        books = Book.objects.filter(genre=genre, available=True).order_by('-id')
    else:
        books = Book.objects.filter(available=True).order_by('-id')
    paginator = Paginator(books, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    cart_form = CartAddForm()
    return render(request, 'shop/home.html', {'page_obj': page_obj, 'cart_form': cart_form, 'genre': genre})


def book_detail(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_form = CartAddForm()
    if request.method == 'POST':
        cart_form = CartAddForm(request.POST)
        if cart_form.is_valid():
            cd = cart_form.cleaned_data
            cart = request.session.get('cart', {})
            if str(book_id) in cart:
                cart[str(book_id)]['quantity'] += cd['quantity']
            else:
                cart[str(book_id)] = {'quantity': cd['quantity'], 'price': str(book.price)}
            request.session['cart'] = cart
            messages.success(request, f"{cd['quantity']}x {book.title} was added to the cart")
            return redirect('cart_detail')
    return render(request, 'shop/book_detail.html', {'book': book, 'cart_form': cart_form})


def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, 'shop/author_detail.html', {'author': author})


@login_required
def cart_add(request, book_id):
    book = get_object_or_404(Book, id=book_id)
    cart_item, created = Cart.objects.get_or_create(user=request.user, book=book)
    max_quantity = book.quantity
    form = None
    if request.method == 'POST':
        form = CartAddForm(request.POST, book_id=book_id, max_quantity=max_quantity)
        if form.is_valid():
            cd = form.cleaned_data
            cart_item.quantity = cd['quantity']
            cart_item.save()
            messages.success(request, f"{cd['quantity']}x {book.title} was added to the cart")
            return redirect('cart_detail')
    else:
        form = CartAddForm(initial={'quantity': cart_item.quantity}, book_id=book_id, max_quantity=max_quantity)

    return render(request, 'shop/cart_add.html', {'form': form, 'book': book})


@login_required
def cart_detail(request):
    cart_items = Cart.objects.filter(user=request.user)
    total_cost = 0
    for cart_item in cart_items:
        total_cost += cart_item.book.price * cart_item.quantity

    if request.method == 'POST':
        if 'delete' in request.POST:
            item_id = request.POST.get('delete')
            cart_item = Cart.objects.get(id=item_id)
            cart_item.delete()
        else:
            for cart_item in cart_items:
                new_quantity = request.POST.get(str(cart_item.id))
                if new_quantity:
                    cart_item.quantity = new_quantity
                    cart_item.save()
            return redirect('cart_detail')

    return render(request, 'shop/cart_detail.html', {'cart_items': cart_items, 'total_cost': total_cost})


@login_required
def cart_delete(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    cart_item.delete()
    messages.success(request, "Book was removed from the cart")
    return redirect('cart_detail')


@login_required
def cart_update(request, cart_item_id):
    cart_item = get_object_or_404(Cart, id=cart_item_id, user=request.user)
    form = CartAddForm(request.POST, book_id=cart_item.book.id, max_quantity=None)
    if form.is_valid():
        cd = form.cleaned_data
        cart_item.quantity = cd['quantity']
        cart_item.save()
        messages.success(request, "Cart was updated")
    return redirect('cart_detail')


@login_required
def order_create(request):
    cart_items = Cart.objects.filter(user=request.user)
    if not cart_items:
        messages.error(request, "Your cart is empty")
        return redirect('cart_detail')

    if request.method == 'POST':
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data

            user_id = cart_items.first().user.id

            order = Order.objects.create(
                client_id=user_id,
                first_name=cd['first_name'],
                last_name=cd['last_name'],
                address=cd['address']
            )

            for cart_item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    book=cart_item.book,
                    quantity=cart_item.quantity
                )

            cart_items.delete()
            order_send.delay(order.pk)  # SEND ORDER ///////////////////////////////////////////////////
            messages.success(request, "Your order has been submitted")
            return redirect('order_detail', order_id=order.id)
    else:
        form = OrderCreateForm()

    return render(request, 'shop/create_order.html', {'form': form})


@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'shop/order_detail.html', {'order': order})


@login_required
def orderlist(request):
    orders = Order.objects.filter(client=request.user).order_by('-created')
    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'shop/order_list.html', {'page_obj': page_obj})
