from django.db import models
import uuid
def get_image_path(obj=None, filename='.png'):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    path = ''.join(['images\\', filename])
    return path

class Images(models.Model):

    title = models.CharField(max_length=100, blank=True)
    image = models.ImageField(upload_to=get_image_path)
    url = models.URLField(blank=True)

    def __str__(self):
        return self.title

    
# Create your models here.
