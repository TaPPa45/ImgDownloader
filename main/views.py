from django.conf import settings
import os
from django.shortcuts import render
from django.http import Http404
from django.views.generic import CreateView, ListView, TemplateView
from django.views.generic.edit import FormView
from .forms import ImageForm, ResizeForm
from .models import Images, get_image_path
import requests
from PIL import Image
import re


class ImagesListView(ListView):
    
    http_method_names = ['get']
    context_object_name = 'images'
    model = Images
    template_name = 'main.html'


class ImageView(TemplateView, FormView):
    object = None
    http_method_names = ['get', 'post']
    template_name = 'image.html'
    width = None
    height = None
    form_class = ResizeForm
    def get_object(self, id):
        try:
            return Images.objects.get(id=id)
        except Images.DoesNotExist:
            raise Http404('Изображение с ID %s не найдено' % id)

    def get_context_data(self, **kwargs):
        obj_id = self.kwargs.get('img_id')
        self.object = self.get_object(obj_id)
        img = Image.open(self.object.image)
        self.width, self.height = img.size
        context = super(ImageView, self).get_context_data(**kwargs)
        context.update({
            'image': self.object,
        })
        return context

    def get_initial(self):
        initial = super(ImageView, self).get_initial()
        initial['width'] = self.width
        initial['height'] = self.height
        return initial

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        obj_id = self.kwargs.get('img_id')
        self.object = self.get_object(obj_id)
        if form['width'].data != self.width or form['height'].data != self.height:
            try:
                img = Image.open(self.object.image)
            except IOError:
                return self.form_invalid(form)
            self.width, self.height = img.size
            width = int(form['width'].data)
            height = int(form['height'].data)
            resize_ratio = width / self.width if width != self.width else height / self.height    
            new_width =  int(self.width * resize_ratio)   
            new_height =  int(self.height * resize_ratio)
            if new_height <= 0 or new_width <=0:
                return self.form_invalid(form)
            size = (new_width, new_height)
            new_img = img.resize(size, Image.ANTIALIAS)
            path = self.object.image.path.split('\\')
            new_path = os.path.join(settings.MEDIA_ROOT,'resized_images\\')
            new_filename =  '%sx%s_' % (new_width, new_height) + path[-1] 
            tmpl = r'(\.png)|(\.jpe?g)'
            if not re.match(tmpl, new_path):
                new_filename += '.png'
            if not os.path.exists(new_path):
                os.mkdir(new_path)
            new_img.save(new_path + new_filename)
            self.object.image = new_path + new_filename
            self.object.save()
            self.success_url = '/image/%s' % (self.object.id)
            return self.form_valid(form)
        return self.form_invalid(form)




class AddImage(CreateView):
    object = None
    http_method_names = ['get','post']
    form_class = ImageForm
    model = Images
    success_url = None
    template_name = 'add_image.html'
    file_root = None

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        img = None
        if form.files and not form['url'].data:            
            return self.form_valid(form)
        if form['url'].data and not form.files:
            self.file_root =  os.path.join(settings.MEDIA_ROOT, get_image_path(form['url'].data.split('/')[-1]))
            try:
                img = requests.get(form['url'].data).content
            except:
                return self.form_invalid(form)
            if not os.path.exists('\\'.join(self.file_root.split('\\')[:-1])):
                os.mkdir('\\'.join(self.file_root.split('\\')[:-1]))
            out = open(self.file_root, "wb")
            out.write(img)
            out.close()
            try:
                img = Image.open(self.file_root)
            except IOError:
                os.remove(self.file_root)
                return self.form_invalid(form)
            return self.form_valid(form)
        return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        self.success_url = '/image/%s' % (self.object.id)
        if self.file_root:
            self.object.image = self.file_root
            self.object.save()
        return super().form_valid(form)
                
        

