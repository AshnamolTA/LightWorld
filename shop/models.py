from django.db import models

# Create your models here.
from django.contrib.auth.models import User

from django.db.models.signals import post_save

from django.db import models



from embed_video.fields import EmbedVideoField



# Create your models here.


class BaseModel(models.Model):

    created_date=models.DateTimeField(auto_now_add=True)
    
    updated_date=models.DateTimeField(auto_now=True)

    is_active=models.BooleanField(default=True)


class UserProfile(BaseModel):

    bio=models.CharField(max_length=200,null=True)

    profile_picture=models.ImageField(upload_to="profile_picture",null=True,blank=True,default="profile_picture/default.png")

    phone=models.CharField(max_length=200,null=True)

    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="profile")


    def __str__(self):

        return self.owner.username





class Tag(BaseModel):

    title=models.CharField(max_length=200)

    def __str__(self):
        return self.title





class Brand(BaseModel):

    B_name=models.CharField(max_length=200)

    def __str__(self):
        return self.B_name




class Light(BaseModel):

    light_name=models.CharField(max_length=200)

    description=models.TextField()

    preview_image=models.ImageField(upload_to="previewimage",null=True,blank=True)

    thumbnail=EmbedVideoField()
    
    distributer=models.ForeignKey(User,on_delete=models.CASCADE)

    tag_objects=models.ManyToManyField(Tag)

    brand_object=models.ForeignKey(Brand,on_delete=models.CASCADE)




class Shape(BaseModel):

    Shape=models.CharField(max_length=200)

    def __str__(self):
        return self.shape



class Material(BaseModel):

    material=models.CharField(max_length=200)

    def __str__(self):
        return self.material


class LightBodyColour(BaseModel):

    bodycolour=models.CharField(max_length=200)

    def __str__(self):
        return self.bodycolour



class LightColour(BaseModel):

    colour=models.CharField(max_length=200)

    def __str__(self):
        return self.colour


class Wates(BaseModel):

    wates=models.CharField(max_length=200)

    def __str__(self):
        return self.wates



class LightVariant(BaseModel):

    price=models.PositiveIntegerField()

    body_object=models.ForeignKey(LightBodyColour,on_delete=models.CASCADE)

    colour_object=models.ForeignKey(LightColour,on_delete=models.CASCADE)

    material_object=models.ForeignKey(Material,on_delete=models.CASCADE)

    shape_object=models.ForeignKey(Shape,on_delete=models.CASCADE)

    wates_object=models.ForeignKey(Wates,on_delete=models.CASCADE)

    




#whishlist.objects.filter(owner=request.user)

#request.user.basket
class WishList(BaseModel):

    owner=models.OneToOneField(User,on_delete=models.CASCADE,related_name="basket")


class WishListItem(BaseModel):

    wishlist_object=models.ForeignKey(WishList,on_delete=models.CASCADE,related_name="basket_item")

    project_object=models.ForeignKey(Light,on_delete=models.CASCADE)

    is_order_placed=models.BooleanField(default=False)

    # class Meta:

    #     unique_together=("wishlist_object","project_object","is_order_placed")


class Order(BaseModel):

    wishlistitem_objects=models.ManyToManyField(WishListItem)

    is_paid=models.BooleanField(default=False)

    order_id=models.CharField(max_length=200,null=True)

    cusomer=models.ForeignKey(User,on_delete=models.CASCADE,null=True)



#django.db.models.signals---post_save,pre_save,post_init


def create_user_profile(sender,instance,created,**kwargs):

    if created:

        UserProfile.objects.create(owner=instance)

post_save.connect(create_user_profile,User)


def create_wishlist(sender,instance,created,**kwargs):

    if created:

        WishList.objects.create(owner=instance)

post_save.connect(create_wishlist,sender=User)