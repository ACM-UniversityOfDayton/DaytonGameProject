import cocos
from cocos.director import director
from cocos.layer import *
import pyglet
from pyglet.window import key
import random
import cocos.collision_model as cm
import cocos.euclid as eu
from cocos.actions import MoveTo, Repeat
from cocos.text import Label
from cocos import scene



img = pyglet.image.load("popo.png")



       
img_grid = pyglet.image.ImageGrid(img, 1, 3)

anim = pyglet.image.Animation.from_image_sequence(img_grid[0:], 0.1, loop=True)


class Mover(cocos.actions.Move):
    def step(self, dt):
        super().step(dt)
        vel_x = (keyboard[key.RIGHT] - keyboard[key.LEFT]) *150
        vel_y = (keyboard[key.UP] - keyboard[key.DOWN]) *150
        self.target.velocity = (vel_x, vel_y)
        self.target.cshape.center = eu.Vector2(*self.target.position)


class Car(cocos.sprite.Sprite):
    def __init__(self):
        super().__init__("Audi.png", scale = .33)


        self.position = 400, 360

        self.cshape = cm.AARectShape(eu.Vector2(*self.position), self.width/4, self.height/1.9)

        self.do(Repeat(MoveTo((random.randint(50, 1200),  random.randint(50, 670)), 2) + MoveTo((random.randint(50, 1200),  random.randint(50, 670)), 2)))

    def update_(self):
        self.cshape.center = eu.Vector2(*self.position)



class Police(cocos.sprite.Sprite):
    def __init__(self):
        super().__init__(anim, scale = .33)
        
        self.position = 800, 360
        self.velocity = (0,0)

        self.cshape = cm.AARectShape(eu.Vector2(*self.position), self.width/4, self.height/1.9)

        self.do(Mover())


class MainLayer(cocos.layer.Layer):
    car_exists = True
    
    def __init__(self):
        super().__init__()

        self.police = Police()
        self.car = Car()

        self.add(self.police, 1)
        self.add(self.car, 0)

        self.coll_manager = cm.CollisionManagerBruteForce()

    def update(self, dt):
        self.car.update_()

        
        if self.coll_manager.they_collide(self.police, self.car):
            director.replace(scene.Scene(FinalScreen()))

            
    
class FinalScreen(ColorLayer):

    def __init__(self):
        super(FinalScreen, self).__init__(68, 100, 208, 1000)

        winText = Label("You win!", font_name= "Times New Roman", font_size = 32, anchor_x = 'center', anchor_y = 'center')
        winText.position = 600, 360
        self.add(winText)

if __name__ == "__main__":

    director.init(width=1280, height=720, caption="Car Game")

    keyboard = key.KeyStateHandler()
    director.window.push_handlers(keyboard)


    main_scene  = cocos.scene.Scene()

    game_layer = MainLayer()

    main_scene.schedule_interval(game_layer.update, 1 / 60)


    

    main_scene.add(game_layer)
    

    director.run(main_scene)
