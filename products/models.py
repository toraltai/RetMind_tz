from django.db import models

class Category(models.Model):
    name = models.CharField(verbose_name='Category name', max_length=100)

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    def __str__(self):
        return f'{self.name}'

class Tag(models.Model):
    name = models.CharField(verbose_name='Tag name', max_length=100)
    
    def __str__(self):
        return f'{self.name}'

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                verbose_name='Category')
    tags = models.ManyToManyField(Tag, verbose_name='Tag')
    description = models.TextField('Description')
    price = models.DecimalField('Price', max_digits=10, decimal_places=2)
    created_at = models.DateTimeField('Created Date',auto_now_add=True)