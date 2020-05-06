import pygame as pg
import os.path
import random
import sys

class BPPGame():
   def __init__(self):
      
      window_width = 600
      window_height = 650
      
      self.tile_width = 150
      self.tile_height = 150

      self.coloumn = 4
      self.rows = 4

      self.img_list = [0,"lisa.jpg","jennie.jpg","jisoo.jpg","rose.jpg",
                       "jenlisa.jpg","chaesoo.jpg","chaelisa.jpg","jensoo.jpg",
                       "bp1.png","bp3.jpg"]

      self.empty_tile = (3,3)
      global emptyc,emptyr
      emptyc,emptyr = 3,3
      
      self.color = (255,51,51)
      white = (215,215,215)
      self.black = (0,0,0)

      self.tiles = {}

      pg.init()
      self.gameWindow = pg.display.set_mode((window_width,window_height))
      pg.display.set_caption("blackpink puzzle")

      self.gameWindow.fill(white)
      pg.display.update()

      if(os.path.isfile('level.txt')):
            lfile=open('level.txt','r')
            
            self.level=int(lfile.read())
            
            lfile.close()
      else:
            self.level=1

      self.intro()

   def message(self,v1,u1,text):
      rect_w = 70
      rect_h = 70
      
      font = pg.font.SysFont('couriernew',25)
      TextSurf = font.render(text,True,self.black)
      TextRect = TextSurf.get_rect()
      TextRect.center = ((v1*rect_w+((rect_w-3)/2)),
                         (u1*rect_h+(rect_h/2)))
   
      self.gameWindow.blit(TextSurf,TextRect)
      pg.display.update()

   def buttons(self,text):
      
      rect_w = 70
      rect_h = 70
      color = self.color

      mouse_pos = pg.mouse.get_pos()
      click = pg.mouse.get_pressed()

      if (self.v*rect_w+rect_w-3 > mouse_pos[0] > self.v*rect_w
          and self.u*rect_h+rect_h-3 > mouse_pos[1] > self.u*rect_h):
         if int(text) <= self.level:
            color = (255,51,102)
            if click[0] == 1:
               self.start(int(text))
         else:
            pass

      pg.draw.rect(self.gameWindow,color,[self.v*rect_w,self.u*rect_h,
                              rect_w-3,rect_h-3])
      self.message(self.v,self.u,text)
      
      pg.display.update()

   def intro(self):

      while True:
         
         self.v = 4
         self.u = 5
         
         for event in pg.event.get():
            
            if event.type == pg.QUIT:
               pg.quit()
               sys.exit()
               
         for rec in range(1,11):
               
            self.buttons(str(rec))
            
              
            self.v += 1
         
            if self.v == 8:
               self.v = 4
               self.u += 1
               


   def labels(self,v1,u1,text,color,size=20):
      font = pg.font.SysFont('comicsansms',size)
      TextSurf = font.render(text,True,color)
      TextRect = TextSurf.get_rect()
      
      TextRect.center = (v1,u1)
   
      self.gameWindow.blit(TextSurf,TextRect)
      pg.display.update()
      
   def check(self):

      global game_over
   
      j,k = 0,0
      tag_list = []
      
      for i in range(1,17):
         
      
         tag = "tag"+str(i)
         
      
         if self.tiles[(j,k)][1] == tag:
            tag_list.append(tag)
            j += 1
            if j > 3:
               k += 1
               j = 0

         else:
            break

      if i == 16:
         print("GAME FINISHED")
         game_over = True

   def shift (self,c, r) :
       global emptyc, emptyr
       rect_color = (255,255,255)
       self.gameWindow.blit(
           self.tiles[(c, r)][0],
           (emptyc*self.tile_width, emptyr*self.tile_height))

       
    
       self.gameWindow.blit(
           self.tiles[self.empty_tile][0],
           (c*self.tile_width, r*self.tile_height))

       
       
       temp = self.tiles[(c,r)]
       
    
       self.tiles[(c,r)] = self.tiles[(emptyc,emptyr)]
       self.tiles[(emptyc,emptyr)] = temp
       
       emptyc, emptyr = c, r

       
       pg.draw.rect(self.gameWindow,rect_color,[c*self.tile_width,r*self.tile_height,
                                      self.tile_width-1,self.tile_height-1])
    
       self.empty_tile = (emptyc, emptyr)
    
       
       pg.display.flip()

   def shuffle(self) :
      global emptyc, emptyr
      
      last_r = 0 
      for i in range(100):
         
         pg.time.delay(50)
         while True:
            
            r = random.randint(1, 4)
            if (last_r + r == 5):
               
               continue
            if r == 1 and (emptyc > 0):
               self.shift(emptyc - 1, emptyr) 
            elif r == 4 and (emptyc < self.coloumn - 1):
               self.shift(emptyc + 1, emptyr) 
            elif r == 2 and (emptyr > 0):
               self.shift(emptyc, emptyr - 1) 
            elif r == 3 and (emptyr < self.rows - 1):
               self.shift(emptyc, emptyr + 1) 
            else:
                
               continue
            last_r=r
            break 

   def start(self,l):
      f=1
      global level,game_over
      game_over = False
      level = l
      img = self.img_list[level]
      self.image = pg.image.load("./Image/"+img)

      self.gameWindow.fill((190,190,190))
      for r in range (self.coloumn):
      
         for c in range (self.rows):

            tag = "tag"+str(f)
         
            tile = self.image.subsurface(c*self.tile_width,r*self.tile_height,
                              self.tile_width-1,self.tile_height-1)
            f += 1
            self.tiles [(c, r)] = (tile,tag)
         
            if(c,r) == self.empty_tile:
               pg.draw.rect(self.gameWindow,(255,255,255),
                            [c*self.tile_width,r*self.tile_height,
                             self.tile_width-1,self.tile_height-1])
               break
            
            self.gameWindow.blit(tile,(c*self.tile_width,r*self.tile_height))
            pg.display.update()
            
          
      
      text = "Level "+str(level)
      self.labels(75,625,text,(0,0,0))
      self.labels(300,625,"Click to start Game",(0,0,0))
         
      pg.display.update()

      self.gameloop()

   def gameloop(self):
   
      started = False
      show_sol = False

      global level
      
   
      while True:

         if game_over:
            self.labels(300,300,"Good job well played",(255,51,51),50)
            
      
         for event in pg.event.get():
         
            
            if event.type == pg.QUIT:
               pg.quit()
               sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
               
            
               if not started:
                  self.shuffle()
                  self.gameWindow.fill((190,190,190),(150,610,300,40))
                  self.labels(300,625,"Right click to see Solution",(0,0,255))
                  started = True

               if game_over:
                  level += 1
                  
                  if self.level < level:
                     self.level +=1
                     file = open("level.txt","w")
                     file.write(str(self.level))
                     file.close()
                  self.start(level)

               if event.dict['button'] == 1:
                  mouse_pos = pg.mouse.get_pos()
               
                  c = mouse_pos[0] // self.tile_width
                  r = mouse_pos[1] // self.tile_height
               
                  
               
                  if c == emptyc and r == emptyr:
                     continue
                  elif c == emptyc and (r == emptyr-1 or r == emptyr+1):
                     self.shift(c,r)
                     self.check()
                  elif r == emptyr and (c == emptyc-1 or c == emptyc+1):
                     self.shift(c,r)
                     self.check()
                  

               elif event.dict['button'] == 3:
                  saved_image = self.gameWindow.copy()
                  
                  self.gameWindow.blit(self.image, (0, 0))
                  pg.display.flip()
                  show_sol= True

            elif show_sol and (event.type == pg.MOUSEBUTTONUP):
               
               self.gameWindow.blit (saved_image, (0, 0))
               pg.display.flip()
               show_sol = False

if __name__ == "__main__":
   BPPGame()



