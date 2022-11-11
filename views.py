from framework.templator import render
from patterns.сreational_patterns import Engine, MapperRegistry
from patterns.structural_patterns import AppRoute
from patterns.behavioral_patterns import SmsNotifier, ListView, CreateView, BaseSerializer, ConsoleWriter
from patterns.architectural_patterns import UnitOfWork

site = Engine()
sms_notifier = SmsNotifier()
UnitOfWork.new_current()
UnitOfWork.get_current().set_mapper_registry(MapperRegistry)

routes = {}


@AppRoute(routes=routes, url='/')
class Index:
    def __call__(self, request):
        return '200 OK', render('index.html', objects_list=site.categories)


@AppRoute(routes=routes, url='/products/')
class Products:
    def __call__(self, request):
        return '200 OK', render('products.html')


@AppRoute(routes=routes, url='/bio/')
class Bio:
    def __call__(self, request):
        return '200 OK', render('bio.html')


@AppRoute(routes=routes, url='/career/')
class Career:
    def __call__(self, request):
        return '200 OK', render('career.html')


@AppRoute(routes=routes, url='/contact/')
class Contact:
    def __call__(self, request):
        return '200 OK', render('contact.html')


class NotFound404:
    def __call__(self, request):
        return '404 WHAT', '404 PAGE Not Found'


@AppRoute(routes=routes, url='/products-list/')
class ProductsList:
    def __call__(self, request):
        try:
            category = site.find_category_by_id(
                int(request['request_params']['id']))
            return '200 OK', render('product_list.html',
                                    objects_list=category.products,
                                    name=category.name, id=category.id)
        except KeyError:
            return '200 OK', 'No products have been added yet'


@AppRoute(routes=routes, url='/create-product/')
class CreateProduct:
    category_id = -1

    def __call__(self, request):
        if request['method'] == 'POST':

            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category = None
            if self.category_id != -1:
                category = site.find_category_by_id(int(self.category_id))
                product = site.create_product('service', name, category)

                product.observers.append(sms_notifier)  ### as soon as product is created we tie up subscribers to it
                site.products.append(product)

            return '200 OK', render('product_list.html',
                                    objects_list=category.products,
                                    name=category.name,
                                    id=category.id)

        else:
            try:
                self.category_id = int(request['request_params']['id'])
                category = site.find_category_by_id(int(self.category_id))

                return '200 OK', render('create_product.html',
                                        name=category.name,
                                        id=category.id)
            except KeyError:
                return '200 OK', 'No categories have been added yet'


@AppRoute(routes=routes, url='/create-category/')
class CreateCategory:
    def __call__(self, request):

        if request['method'] == 'POST':

            data = request['data']

            name = data['name']
            name = site.decode_value(name)

            category_id = data.get('category_id')

            category = None
            if category_id:
                category = site.find_category_by_id(int(category_id))

            new_category = site.create_category(name, category)

            site.categories.append(new_category)

            return '200 OK', render('index.html', objects_list=site.categories)
        else:
            categories = site.categories
            return '200 OK', render('create_category.html',
                                    categories=categories)


@AppRoute(routes=routes, url='/category-list/')
class CategoryList:
    def __call__(self, request):
        return '200 OK', render('category_list.html',
                                objects_list=site.categories)


@AppRoute(routes=routes, url='/copy-product/')
class CopyProduct:
    def __call__(self, request):
        request_params = request['request_params']

        try:
            name = request_params['name']

            old_product = site.get_product(name)
            if old_product:
                new_name = f'copy_{name}'
                new_product = old_product.clone()
                new_product.name = new_name
                site.products.append(new_product)

            return '200 OK', render('product_list.html',
                                    objects_list=site.products,
                                    name=new_product.category.name)
        except KeyError:
            return '200 OK', 'No products have been added yet'


@AppRoute(routes=routes, url='/seller-list/')
class SellerListView(ListView):
    template_name = 'seller_list.html'

    def get_queryset(self):
        mapper = MapperRegistry.get_current_mapper('seller')
        return mapper.all()



@AppRoute(routes=routes, url='/create-seller/')
class SellerCreateView(CreateView):
    template_name = 'create_seller.html'

    def create_obj(self, data: dict):
        name = data['name']
        name = site.decode_value(name)
        new_obj = site.create_user('seller', name)
        site.sellers.append(new_obj)
        new_obj.mark_new()
        UnitOfWork.get_current().commit()


@AppRoute(routes=routes, url='/add-seller/')
class AddSellerByProductCreateView(CreateView):
    template_name = 'add_seller.html'

    def get_context_data(self):
        context = super().get_context_data()
        context['products'] = site.products
        context['sellers'] = site.sellers
        return context

    def create_obj(self, data: dict):
        product_name = data['product_name']
        product_name = site.decode_value(product_name)
        product = site.get_product(product_name)
        seller_name = data['seller_name']
        seller_name = site.decode_value(seller_name)
        seller = site.get_seller(seller_name)
        product.add_seller(seller)


# @AppRoute(routes=routes, url='/api/')
# class ProductApi:
#     @Debug(name='CourseApi')
#     def __call__(self, request):
#         return '200 OK', BaseSerializer(site.products).save()
