from pico2d import *

import random
import math
import game_framework
import game_world
from behavior_tree import BehaviorTree, Action, Sequence, Condition, Selector


# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 10.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10.0

animation_names = ['Walk', 'Idle']


class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombie/" + name + " (%d)" % i + ".png") for i in range(1, 11)]
            Zombie.font = load_font('ENCR10B.TTF', 40)
            Zombie.marker_image = load_image('hand_arrow.png')


    def __init__(self, x=None, y=None):
        self.x = x if x else random.randint(100, 1180)
        self.y = y if y else random.randint(100, 924)
        self.load_images()
        self.dir = 0.0      # radian 값으로 방향을 표시
        self.speed = 0.0
        self.frame = random.randint(0, 9)
        self.state = 'Idle'
        self.ball_count = 0


        self.tx, self.ty = 1000, 1000
        # 여기를 채우시오.

        self.build_behavior_tree()


    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50


    def update(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        # fill here


    def draw(self):
        if math.cos(self.dir) < 0:
            Zombie.images[self.state][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
        else:
            Zombie.images[self.state][int(self.frame)].draw(self.x, self.y, 100, 100)
        self.font.draw(self.x - 10, self.y + 60, f'{self.ball_count}', (0, 0, 255))
        Zombie.marker_image.draw(self.tx+25, self.ty-25)



        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass

    def handle_collision(self, group, other):
        if group == 'zombie:ball':
            self.ball_count += 1


    def set_target_location(self, x=None, y=None):
        if x is not None and y is not None:
            raise ValueError('목표 지점 설정하시오 ')
        self.tx,self.ty = x,y
        return BehaviorTree.SUCCESS




    def distance_less_than(self, x1, y1, x2, y2, r):
        # 여기를 채우시오.
        pass



    def move_little_to(self, tx, ty):
        distance = RUN_SPEED_PPS * game_framework.free_time
        self.dir = math.atan2(ty - self.y, tx - self.x)
        self.x += distance * math.cos(self.dir)
        self.y += distance * math.sin(self.dir)


    def move_to(self, r=0.5):
        # frame_time를 이용하여 이동 거리 계산
        self.state='wale'#디버그용 출력
        self.move_little_to(self.tx, self.ty) #목표 지점까지 조금 이동
        pass


    def set_random_location(self):
        # 여기를 채우시오.
        pass


    def is_boy_nearby(self, distance):
        # 여기를 채우시오.
        pass


    def move_to_boy(self, r=0.5):
        # 여기를 채우시오.
        pass


    def get_patrol_location(self):
        # 여기를 채우시오.
        pass


    def build_behavior_tree(self):
        #목표 지점을 설정하는 액션 노드 생성
        a1=Action('Set Target Location',self.set_target_location,1000,1000)
        a2=Action('Move To Target',self.move_to,0.5)
        root= move_to_target_location=Sequence('Move To Target',a1,a2)
        self.bt=BehaviorTree(root)


