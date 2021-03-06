from django import forms
from .models import Product, Category
from .widgets import CustomClearableFileInput


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        # To include all fields
        fields = ('image', 'product_name', 'category', 'price', 'overall_rating', 'brand_name', 'product_description',
                  'exclusive')
        # fields = '__all__'

    image = forms.ImageField(label='Image',
                             required=False,
                             widget=CustomClearableFileInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        categories = Category.objects.all()
        friendly_names = [(c.id, c.get_friendly_name()) for c in categories]
        # friendly_names.insert(0, (0, 'Category *'))

        self.fields['category'].choices = friendly_names

        for field_name, field in self.fields.items():
            # if field_name == 'category':
            #     field.label = False
            #     field.widget.attrs['class'] = 'grey-text'
            if field.required:
                field.label = f'{field.label} *'
            if field_name == 'product_description':
                field.widget.attrs['data-length'] = '120'
