import sys
import pygame
import random
import scenario_europe as scenario
import advantage as advantage

pygame.init()

BLACK = 0, 0, 0

class ProvinceDisplay(pygame.sprite.Sprite):

    # __init__ = Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, group, provId, coordinate, province):  # note default values of params
       # Call the parent class (Sprite) constructor
       pygame.sprite.Sprite.__init__(self,group)
       color  = BLACK
       width  = 40
       height = 50
       self.provId = provId
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
            (222, 222, 222),     # pid 0 - grey
            (255,   0,   0),     # pid 1 - red
            (0  , 255,   0),     # pid 2 - green
            (0  ,   0, 255),     # pid 3 - blue
        )
      # print('nation',self.province.pid)
        assert self.province.pid <= len(PLAYER_COLOURS)
        player_colour = PLAYER_COLOURS[self.province.pid]
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
        for provId, coordinate in scenario.PROVINCE_DISPLAYS:
            province = model.province[provId]
            ProvinceDisplay(self.province_display_group,provId,coordinate,province)

    def draw(self):
        self.province_display_group.draw(self.surface)
        for province_display in self.province_display_group.sprites():
            province_display.draw()

class Province:
    def __init__(self, provId, short_name, long_name, pid, armies):
        '''
        Province is the basic unit of area on the board

        :param provId: integer ID (position in Scenario list)
        :param short_name: 3-letter (uppercase) code for a province eg ROM
        :param long_name: full name (mixed case) of a province, eg Rome
        :param pid: Player id. 0 = Neutral.
        :param armies: no of armies!
        :return:
        '''
        self.provId     = provId
        self.short_name = short_name
        self.long_name  = long_name
        self.pid        = pid
        self.armies     = armies

    def __repr__(self):
        return 'id='+ str(self.provId) + ' ' + self.short_name + ' p='+ str(self.pid)+ ' ar='+ str(self.armies)
        # return 'Province("{}")'.format(self.short_name) + ' ' + str(self.pid)
        # format = built in method of str (string)
        # each {} is placeholder for a parameter in format - clever stuff in docs

class Advantage:
    def __init__(self, advId, short_name, long_name):
        '''
        National Advantages

        :param advId: integer ID (position in list)
        :param short_name: 2-letter (uppercase)  eg AR
        :param long_name: full name (mixed case) eg Archery
        :return:
        '''
        self.advId      = advId
        self.short_name = short_name
        self.long_name  = long_name

    def __repr__(self):
        return 'Id='+str(self.advId) + ' ' + self.short_name + ' ' + self.long_name
        # return 'Province("{}")'.format(self.short_name) + ' ' + str(self.pid)
        # format = built in method of str (string)
        # each {} is placeholder for a parameter in format - clever stuff in docs

class PlayerTurn:
    def __init__(self, pid, nid):
        self.pid     = pid
        self.nid     = nid
        self.turn    = game.model.turn
        self.gold    = 0
        self.qtyProv = 0
        self.qtyArmy = 0
        self.score   = 0

    def __repr__(self):
        return   'p='  + str(self.pid)     + ' n=' + str(self.nid) \
               +' t='  + str(self.turn)    + ' g=' + str(self.gold) \
               +' pv=' + str(self.qtyProv) + ' a=' + str(self.qtyArmy) \
               +' sc='+ str(self.score)

class Player:
    def __init__(self, pid, nid, name):
        self.pid      = pid
        self.nid      = nid
        self.name     = name
        self.turnJoin = game.model.turn
        self.turnQuit = 9999
        self.score    = 0

    def __repr__(self):
        return    'p=' + str(self.pid)      + ' n='  + str(self.nid) \
               +' nm=' + str(self.name)     + ' tj=' + str(self.turnJoin) \
               +' tj=' + str(self.turnJoin) + ' tq=' + str(self.turnQuit) \
               +' sc=' + str(self.score)

class GameTurn:
    def __init__(self):
        self.playerTurn = {}    # pk = pid. contains playerTurn object
        #print('GameTurn init')
        #print(self.playerTurn)

    def phaseMaint(self):
        #self.playerTurn = {}   # here because init not firing for some reason

        # set up playerTurn array ? should be in init?
        for pid in game.model.pidAgeSeq:
            # create / init new playerTurn data
            # TODO archive old player turns to history/log
            nid = game.model.players[pid].nid
            self.playerTurn[pid] = PlayerTurn(pid,nid)

        # calculate playerTurn - loop (provinces); accumulate playerTurn Provinces, Armies
        for provId in game.model.province:
            pid = game.model.province[provId].pid
            if pid > 0:
                self.playerTurn[pid].qtyProv += 1
                #print('qtyprov='+str(#self.playerTurn[provpid].qtyProv))
                self.playerTurn[pid].qtyArmy += game.model.province[provId].armies
                #print('prov='+str(provpid)+' armies='+str(game.model.province[provId].armies))

        print('phaseMaint 10 playerTurn')
        print(self.playerTurn)

        # now calc maint for each player
        for pid in game.model.pidAgeSeq:
            #self.playerTurn[pid].gold += (self.playerTurn[pid].qtyProv * 5)
            taxrate   = 5 # TODO unless Farmer
            tottax    = taxrate   * self.playerTurn[pid].qtyProv * 5
            unitMaint = 2 # TODO lookup
            totMaint  = unitMaint * self.playerTurn[pid].qtyArmy
            self.playerTurn[pid].gold = self.playerTurn[pid].gold + tottax - totMaint
            # TODO cfwd gold from turn to turn

            unitRaise = 5  # TODO lookup

            print('p='+str(pid)+' n='+str(nid) \
                  + ' g='  + str(self.playerTurn[pid].gold) \
                  + ' qp=' + str(self.playerTurn[pid].qtyProv) \
                  + ' qa=' + str(self.playerTurn[pid].qtyArmy) \
                  + ' tx=' + str(tottax) \
                  + ' tm=' + str(totMaint)
                 )

            #TODO B0-B2 uprising reinfs

            incrArmies = 0
            if self.playerTurn[pid].gold < 0:
                #disband units
                incrArmies = (self.playerTurn[pid].gold // unitRaise) -1
            elif self.playerTurn[pid].gold >= unitRaise:
                #raise units
                incrArmies = self.playerTurn[pid].gold // unitRaise

            self.playerTurn[pid].gold -= (incrArmies * unitRaise)
            print('raise ' + str(incrArmies) + 'rem gold=' + str(self.playerTurn[pid].gold))

            #pick province
            #TODO identify avail provs, loop through to add/remove until incrArmies used up
            incrprovId = game.model.nations[pid].homeProvId
            game.model.province[incrprovId].armies += incrArmies
            self.playerTurn[pid].qtyArmy           += incrArmies

            print('p='+str(pid)+' n='+str(nid) \
                  + ' g='  + str(self.playerTurn[pid].gold) \
                  + ' qa=' + str(self.playerTurn[pid].qtyArmy) \
                  + ' pv=' + str(incrprovId) \
                  + ' p.a=' + str(game.model.province[incrprovId].armies)
                  )

        #end loop: for pid in game.model.pidAgeSeq

        print('phaseMaint 90 playerTurn,province')
        print(self.playerTurn)
        print(game.model.province)

    def phaseMove(self):
        pass

    def phaseScore(self):
        pass

    def phaseStatus(self):
        pass

    def __repr__(self):
        return  self.playerTurn

# Will spawn 2 objects of this class, ActiveNations, and FallenNations (ie dead ones)
class Nation:
    def __init__(self):

            '''
        Each player will control several nations, one after the other.

        :param pid:        player id
        :param nid:        nation id
        :param name:       full name (mixed case) of a Nation eg Foosballmen
        :param ageCat:     Age Category, B(arbarian), K(ingdom), E(mprire)
        :param ageLvl:     Age of nation within above category, eg 0,1,2,
        :param advid:      Advantage Id
        :param homeProvId: FK to home Province
        :param gold:       Qty gold in treasury
        :param turnRose:   Turn nation Arose / was born
        :param turnFell:   Turn nation Fell
        :param scoreCum:   Cumulative score
        :return:
        '''

     #   self.pid        = pid
     #   self.nid        = nid
     #   self.name       = name
     #   self.advid      = advid
     #   self.ageCat     = ageCat
     #   self.ageLvl     = ageLvl
     #   self.homeProvId = homeProvId
     #   self.gold       = gold
     #   self.turnRose   = turnRose
     #   self.turnFell   = turnFell
     #   self.scoreCum   = scoreCum

    # Is integer i in intDir (which should be a Directory of Integers)
    # returns Bool
    def isInIntDir(self, i, intDir):
        inInDir = False
        for j in intDir:
            if i == intDir[j]:
                inInDir = True
                #print('inInDir ' + str(i))
        return inInDir

    # get a random (non-duplicate) advantage to choose from
    def genAdvChoice(self, curChoices):
        validAdvId = False
        loopMax    = 10
        while validAdvId == False and loopMax > 0:
            loopMax = loopMax -1
            advId = random.randrange(1,12)
            if self.isInIntDir(i=advId, intDir=curChoices):
                pass               # duplicate - try again
            else:
                validAdvId = True  # unique - exit loop
            # TODO add check on too many nations
        return advId

    def isValidHomeProv(self, provId, homeChoices):
        valid = True  # True unless fail any validation

        if self.isInIntDir(i=provId, intDir=homeChoices):
            #print('Clash with homeChoices provId='+str(provId))
            valid = False         # duplicate - try again

        if self.isInIntDir(i=provId, intDir=game.model.noGoProvince):
            #print('Clash with noGoProvince provId='+str(provId))
            valid = False         # duplicate - try again

        return valid

    def genProvChoice(self, curProvChoices, provTp='STD'):  # STD or EDGE
        validProvId = False
        loopMax = 10
        while validProvId == False and loopMax > 0:
            loopMax = loopMax - 1
            if provTp == 'EDGE':
                edgeId  = random.randrange(1, game.model.maxEdge)
                provId = game.model.edgeProvince[edgeId]
            else:
                provId = random.randrange(1, game.model.maxProv)

            if self.isValidHomeProv(provId=provId, homeChoices=curProvChoices):
                validProvId = True  # valid - exit loop

        return provId

    def birthchoices(self):

        advChoices = {}
        advChoices[1] = self.genAdvChoice(curChoices=advChoices)
        advChoices[2] = self.genAdvChoice(curChoices=advChoices)
        advChoices[3] = self.genAdvChoice(curChoices=advChoices)
        #print('advchoices ')
        #print(advChoices)

        homeChoices = {}
        homeChoices[1] = self.genProvChoice(curProvChoices=homeChoices, provTp='STD')
        homeChoices[2] = self.genProvChoice(curProvChoices=homeChoices, provTp='EDGE')

        #print('homeChoices ')
        #print(homeChoices)

        print('Advantages'
              + '[1: a=' + str(advChoices[1]) + ' ' + game.model.advantage[advChoices[1]].short_name + ']'
              + '[2: a=' + str(advChoices[2]) + ' ' + game.model.advantage[advChoices[2]].short_name + ']'
              + '[3: a=' + str(advChoices[3]) + ' ' + game.model.advantage[advChoices[3]].short_name + ']'
              )
        print('Home Provs'
              + '[1: p=' + str(homeChoices[1]) + ' ' + game.model.province[homeChoices[1]].short_name + ']'
              + '[2: p=' + str(homeChoices[2]) + ' ' + game.model.province[homeChoices[2]].short_name + ']'
              )
        advIdx = input('Choose Advantage 1,2,3 ')
        homIdx = input('Choose HomeProv  1,2 ')

        return ( advChoices[int(advIdx)] , homeChoices[int(homIdx)] )

    def birth(self, pid):
        #print('birth start' + str(pid) + str(nid) + str(homeProvId))

        advId, homeId = self.birthchoices()
        #print('advId='+str(advId))
        #print('homeId='+str(homeId))

        self.pid        = pid
        self.nid        = game.model.nextNid
        game.model.nextNid = game.model.nextNid  + 1
        self.advid      = advId
        self.ageCat     = 'B'
        self.ageLvl     = 0
        self.homeProvId = homeId
        self.gold       = 0
        self.turnRose   = game.model.turn
        self.turnFell   = 9999
        self.scoreCum   = 0
        game.model.province[self.homeProvId].pid    = self.pid
        game.model.province[self.homeProvId].armies = 5

        game.model.addToNoGoProv(self.homeProvId, game.model.noGoProvince)
        game.model.addPidAgeSeq(self.pid)
        #print('birth end'  + str(self.pid) + str(self.nid) + str(self.advid)
        #      + str(self.ageCat) + str(self.ageLvl) + str(self.gold))

    #def __str__(self):
    #    return 's '  + str(self.pid) + str(self.nid) + str(self.advid) + str(self.ageCat) + str(self.ageLvl) + str(self.gold)
    #    # __str_ string of(object)
    #    # repr  return string representation of object

    def __repr__(self):
        return  'p='   + str(self.pid)    +' n=' + str(self.nid) \
               +' a='  + str(self.advid)  + ' ' + game.model.advantage[self.advid].short_name\
               +' age='+ str(self.ageCat) + str(self.ageLvl) \
               +' g='  + str(self.gold)   +' tr='+ str(self.turnRose) +' tf='+ str(self.turnFell) \
               +' sc=' + str(self.scoreCum)
        # __str_ string of(object)
        # repr  return string representation of object

class Model:
    '''
    data only - graphics keep out!
    '''
    def __init__(self):
        self.province = {}       # {} denotes dictionary, built in structure with keys: attributes
        self.edgeProvince = {}
        self.noGoProvince = {}   # provinces ineligible to choose as new HomeProv
        self.links = {}
        self.advantage = {}
        self.nations   = {}      # Dict of nations, key is nid
        self.pidAgeSeq = []      # list of pid's: first = youngest; last  oldest
        self.turn = 1
        self.qtyPlayers = 2
        self.players = {}         # PK = pid: (Player object)
        self.nextNid = 1

    def load(self):
        for provId in scenario.PROVINCES:
            # diceloc currently unused
            short_name, long_name, diceLoc, pid, armies = scenario.PROVINCES[provId]   # [] denotes index to an array / dictionary etc
            self.province[provId] = Province(provId, short_name, long_name, pid, armies)

        self.maxProv = self.province.__len__()

        print('max provinces='+ str(self.maxProv))
        print(self.province)

        for fr_provId,to_provId,link_type in scenario.LINKS:
          #  print('100',fr_provId,to_provId,link_type)

            if fr_provId not in self.links:
                self.links[fr_provId] = set()
            self.links[fr_provId].add((to_provId,link_type))    # () represent either arguments or tuples
                                                                    # in this case 1st( is arg, 2nd ( contains a tuple

            if to_provId not in self.links:
                self.links[to_provId] = set()
            self.links[to_provId].add((fr_provId,link_type))

        print('links')
        print(self.links)

        for edgeId in scenario.EDGEPROVINCES:
            provId = scenario.EDGEPROVINCES[edgeId]   # [] denotes index to an array / dictionary etc
            self.edgeProvince[edgeId] = provId

        self.maxEdge = self.edgeProvince.__len__()

        print('max Edge provinces='+ str(self.maxEdge))
        print(self.edgeProvince)

        for advId in advantage.ADVANTAGES:
            short_name, long_name = advantage.ADVANTAGES[advId]   # [] denotes index to an array / dictionary etc
            self.advantage[advId] = Advantage(advId, short_name, long_name)

        print('Advantages')
        print(self.advantage)

    # Start up some initial nations
    def startNations(self):

        self.nation = Nation()
        Nation.birth(self.nation, pid=1)
        self.nations[1] = self.nation
        self.players[1] = Player(1, self.nation.nid, 'Alex')

        self.nation = Nation()
        Nation.birth(self.nation, pid=2)
        self.nations[2] = self.nation
        self.players[2] = Player(1, self.nation.nid, 'Mike')

        #self.nation = Nation()
        #Nation.birth(self.nation, nid=3), pid=3
        #self.nations[3] = self.nation

        print('province')
        print(self.province)

        print('nations')
        print(self.nations)

        print('players')
        print(self.players)

    # add homeProvId and all linked provs to the NoGo list
    def addToNoGoProv(self, homeProvId, noGoProvince):
        print('addToNoGoProv ' + str(homeProvId))
        noGoProvince[homeProvId] = homeProvId

        for link in self.links[homeProvId]:   # or could use game.model.links ?
            provId, linkType = link
            #print('linkloop provId=' + str(provId))
            noGoProvince[provId] = provId

        print('NoGoProv ')
        print(noGoProvince)

    def addPidAgeSeq(self, pid):
        #print('NASb ')
        #print(game.model.pidAgeSeq)

        game.model.pidAgeSeq = [pid] + game.model.pidAgeSeq

        print('NAS')
        print(game.model.pidAgeSeq)

    def doGameTurn(self):
        c = input('Press Return for next game turn')

        self.turn += 1
        gameturn = GameTurn()
        print('gameturn init')
        #print(gameturn)
        gameturn.phaseMaint()

        print('gameturn phaseMaint')
        #print(gameturn)

    def __str__(self):
        return repr(self.province) + '\n' + str(self.links)
        # __str_ string of(object)
        # repr  return string representation of object

class RiseAndFall:
    def __init__(self):
        self.running=False
        self.model = None
        self.mousedownposition = None

    def setup_scenario(self):
        self.board = pygame.image.load("board_1200_900.jpg")
        self.boardrect = self.board.get_rect()
        self.size = width, height = 1200, 900
        self.screen = pygame.display.set_mode(self.size)
        self.model = Model()
        self.model.load()
        self.model.startNations()
        self.pygame_map = PygameMap(self.screen)
        self.pygame_map.load(self.model)

        print('setup_scenario end')

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running=False

        #    if event.type == pygame.MOUSEBUTTONDOWN:
        #        if event.button == 1:
        #            self.mousedownposition = event.pos
        #        elif event.button == 3:
        #            self.model.delete_orders()


    def update(self):
        pass

    def draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(self.board, self.boardrect)
        self.pygame_map.draw()
        pygame.display.flip()
        print('draw end')

    def run(self):
        try:
            self.running=True
            self.setup_scenario()
            self.draw()
            while self.running:
                self.model.doGameTurn()
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

