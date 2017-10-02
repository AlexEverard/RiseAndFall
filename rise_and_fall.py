import sys
import pygame
import scenario_europe as scenario

pygame.init()

BLACK = 0, 0, 0

class ProvinceDisplay(pygame.sprite.Sprite):

    # __init__ = Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, group, location, coordinate, province):  # note default values of params
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self,group)

       color  = BLACK
       width  = 40
       height = 50
       self.location = location
       x,y = coordinate
       self.province = province

       # Create an image of the block, and fill it with a color.
       # This could also be an image loaded from the disk.
       self.image = pygame.Surface([width, height])
       self.image.fill(color)

       # Fetch the rectangle object that has the dimensions of the image
       # Update the position of this object by setting the values of rect.x and rect.y
       self.rect = self.image.get_rect()                  # created by default at 0,0
       self.rect.move_ip(x-int(width/2),y-int(height/2))  # move_ip expects top left point - convert our centre values to top-left

    def draw(self):
        PLAYER_COLOURS = (
            (222,222,222),     # nation 0 - grey
        )
       # print('nation',self.province.nation)
        assert self.province.nation <= len(PLAYER_COLOURS)
        player_colour = PLAYER_COLOURS[self.province.nation]
      #  print('player_colour',player_colour)
        self.image.fill(player_colour)
        font = pygame.font.Font(None, 18)
        label  = font.render(self.province.short_name ,True,BLACK,player_colour)
        armies = font.render(str(self.province.armies),True,BLACK,player_colour)

        label_rect = label.get_rect()
        x = int((self.rect.width  - label_rect.width )/2)
        y = 6
        self.image.blit(label,(x,y))
        self.image.blit(armies,(x,y+20))


class PygameMap:
    def __init__(self,surface):
        self.province_display_group = pygame.sprite.Group()
        self.surface = surface

    def load(self,model):
        for location, coordinate in scenario.PROVINCE_DISPLAYS:
            province = model.province[location]
            ProvinceDisplay(self.province_display_group,location,coordinate,province)

    def draw(self):
        self.province_display_group.draw(self.surface)
        for province_display in self.province_display_group.sprites():
            province_display.draw()

class Model:
    '''
    data only - graphics keep out!
    '''
    def __init__(self):
        self.province = {}  # {} denotes dictionary, built in structure with keys: attributes
        self.links = {}

    def load(self):
        for location in scenario.PROVINCES:
            short_name,long_name = scenario.PROVINCES[location]   # [] denotes index to an array / dictionary etc
            self.province[location] = Province(location,short_name,long_name)

        for fr_location,to_location,link_type in scenario.LINKS:
          #  print('100',fr_location,to_location,link_type)

            if fr_location not in self.links:
                self.links[fr_location] = set()
            self.links[fr_location].add((to_location,link_type))    # () represent either arguments or tuples
                                                                    # in this case 1st( is arg, 2nd ( contains a tuple

            if to_location not in self.links:
                self.links[to_location] = set()
            self.links[to_location].add((fr_location,link_type))

    def __str__(self):
        return repr(self.province) + '\n' + str(self.links)
        # __str_ string of(object)
        # repr  return string representation of object

class Province:
    def __init__(self,location,short_name,long_name):
        '''
        Province is the basic unit of area on the board

        :param location: a 2-tuple identifying where the province is eg as a D12*D6 roll
        :param short_name: 3-letter (uppercase) code for a province eg ROM
        :param long_name: full name (mixed case) of a province, eg Rome
        :return:
        '''
        self.location = location
        self.short_name = short_name
        self.long_name = long_name
        self.nation = 0
        self.armies = 2

    def __repr__(self):
        return 'Province("{}")'.format(self.short_name)
        # format = built in method of str (string)
        # each {} is placeholder for a parameter in format - clever stuff in docs

class RiseAndFall:
    def __init__(self):
        self.running=False
        self.model = None

    def setup_scenario(self):
        self.board = pygame.image.load("board_1200_900.jpg")
        self.boardrect = self.board.get_rect()
        self.size = width, height = 1200, 900
        self.screen = pygame.display.set_mode(self.size)
        self.model = Model()
        self.model.load()
        self.pygame_map = PygameMap(self.screen)
        self.pygame_map.load(self.model)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running=False

    def update(self):
        pass

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.board, self.boardrect)
        self.pygame_map.draw()
        pygame.display.flip()

    def run(self):
        try:
            self.running=True
            self.setup_scenario()
            while self.running:
                self.handle_events()
                self.update()
                self.draw()
                pygame.time.wait(25)
        except:
            raise
        finally:
            pygame.quit()

game=RiseAndFall()
game.run()
print(game.board)
print(game.model)

