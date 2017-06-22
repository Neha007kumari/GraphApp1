from tkinter import *
from keygen import *
import LongestCycle   # C module to calculate longest cycle
from tkinter import filedialog


class App(Frame):

    def __init__(self, master):
        Frame.__init__(self, master)
        master.attributes("-topmost",True)
        self.pack()
        self.createWidgets()
        self.rad = 5
        self.halfedge = False
        self.tar1 = None
        self.can.focus_set() 
        self.vlist = {}
        self.elist = {}
        self.cylenflag = False

    def createWidgets(self):
        self.xframe = Frame(self,bd=5)
        self.xframe.pack({"side":"top"})

        self.cframe = Frame(self,bd=5,bg="#ffb3b3")
        self.cframe.pack({"side":"top"})
       
        self.lab1 = Label(self.xframe,text="No of Vertices : 0 \n No of Edges : 0\n No of Crossings: 0",justify=LEFT,width=20,height=5,bg="#ffb3b3")
        self.lab2 = Label(self.xframe,text = "Max Degree: 0 \n Min Degree: 0",justify=LEFT,width=20,height=5,bg="#ffb3b3")
        self.lab1.pack({"side":"left"})
        self.lab2.pack({"side":"left"})
  
        self.bframe = Frame(self,bd=5,bg="#ffb3b3")
        self.bframe.pack({"side":"bottom"})
    
        self.quitbutton = Button(self.bframe,text="Quit",command=self.quit)
        self.quitbutton.pack({"side": "right"})

        self.clearbutton = Button(self.bframe,text="Clear",command=self.clear)
        self.clearbutton.pack({"side": "right"})
        
        self.savegraph = Button(self.bframe,text="Save",command=self.savegraph)
        self.savegraph.pack({"side":"right"})

        self.readgraph = Button(self.bframe,text="Read",command=self.readgraph)
        self.readgraph.pack({"side":"right"})

        self.longcycle = Button(self.bframe,text="Longest Cycle",command=self.longestcycle)
        self.longcycle.pack({"side":"right"})

        self.debug = Button(self.bframe,text="Debug",command=self.debug)
        self.debug.pack({"side":"right"})
      

        self.var = IntVar()
        self.var.set(1) # initializing the choice
        self.options = [
             ("Add Vert",1),
             ("Add Edge",2),
             ("Del Vert",3),
             ("Del Edge",4),
             ("Drag",5)
        ]
       
        for txt,val in self.options:
            Radiobutton(self.cframe,text=txt,padx =5,pady = 5,command=self.message,value=val,variable=self.var,justify=LEFT).pack(side="left",anchor="center")

        self.can = Canvas(self,width=800,height=600)
        self.can["bg"] = "#FFDAB9"                         # set background color
        self.can["highlightbackground"] = "#000000"      # black border
        self.can.bind("<Button-1>", self.graph_mod)
        self.can.bind("<B1-Motion>",self.drag)
        self.can.bind("<ButtonRelease-1>",self.drop)
        self.can.pack({"side":"top"})
    
    def message(self):
        if self.vlist:
           list = self.degree()
           cross = str(self.edgecrossing())
           if self.cylenflag:
                lb1 = "No of Vertices : "+format(len(self.vlist))+"\n No of Edges :"+format(len(self.elist))+"\n No of Crossings:"+format(cross)
                lb2 ="Max Degree: "+format(list[-1])+"\n Min Degree: "+format(list[0])+"\n Cycle Length: "+format(self.cylen)
           else:
                lb1 = "No of Vertices : "+format(len(self.vlist))+"\n No of Edges: "+format(len(self.elist))+"\n No of Crossings:"+format(cross)
                lb2 ="Max Degree: "+format(list[-1])+"\n Min Degree: "+format(list[0])       
        else:
           lb1 = "No of Vertices :0 \n No of Edges :0 \n No of Crossings:0"
           lb2 = "Max Degree:0 \n Min Degree:0"
        self.lab1.config(text=lb1);
        self.lab2.config(text=lb2);

    def debug(self):
        print("Vertex List:")
        for k,v in self.vlist.items():
            print("{0:s} {1:s}".format(k,str(v)))
        print("Edge List:")
        for k,v in self.elist.items():
            print("{0:s} {1:s}".format(k,str(v)))
        print(self.adjacency_list())

    def vdistance(self,x1,y1,v):
        [x2,y2] = self.can.coords(v[0])[:2]
        return ((x1-x2)**2 + (y1-y2)**2)

    def find_closest_vertex(self,x,y):
        if len(self.vlist) == 0:
           return None
        mind = 1e9
        who  = None
        for it in self.vlist.values():
            d = self.vdistance(x,y,it)
            if d < mind:
               mind,who = d,it
        return who

    def edistance(self,x1,y1,e):
       li = self.can.coords(e[0])
       x2 = (li[0]+li[2])/2
       y2 = (li[1]+li[3])/2
       return (x1-x2)**2 + (y1-y2)**2
  
    def find_closest_edge(self,x,y):     # Finds the closest edge at the clicked point on canvas
        if len(self.elist) == 0:
           return None
        who = None
        mind = 1e9
        for it in self.elist.values():
            d = self.edistance(x,y,it)
            if d < mind:
               mind, who = d, it
        return who
    
    def delete_edge_by_key(self,key):
        self.can.delete(self.elist[key][0])
        u, v = self.elist[key][2]
        self.vlist[u][2].remove(v)
        self.vlist[v][2].remove(u)
        self.vlist[u][3].remove(key)
        self.vlist[v][3].remove(key)
        del(self.elist[key])
        
    def addvertex(self,x,y):
        key = VertexKey.keygen()
        r = self.rad
        tmp = self.can.create_oval(x-self.rad,y-self.rad,x+self.rad,y+self.rad,fill="red",tag="VERTEX")
        self.vlist[key] = [tmp,key,[],[]]
 
    def start_edge(self,x,y):
        self.tar1 = self.find_closest_vertex(x,y)
        if self.tar1:
           self.can.itemconfig(self.tar1[0],fill="green")
           self.halfedge = True

    def finish_edge(self,x,y):
        self.can.itemconfig(self.tar1[0],fill="red")
        self.tar2 = self.find_closest_vertex(x,y)
        if self.tar2 and (self.tar1 != self.tar2):
           k1 = self.tar1[1]
           k2 = self.tar2[1]
           if k1 not in self.tar2[2] and k2 not in self.tar1[2]:
              c1 = self.can.coords(self.tar1[0])
              c2 = self.can.coords(self.tar2[0])
              r = self.rad
              tmp = self.can.create_line(c1[0]+r,c1[1]+r,c2[0]+r,c2[1]+r,width=3,tag="EDGE")
              self.can.tag_lower(tmp)
              key = VertexKey.keygen()
              self.elist[key] = [tmp,key,(k1,k2)]
              self.tar1[2].append(k2)
              self.tar2[2].append(k1)
              self.tar1[3].append(key)
              self.tar2[3].append(key)
        self.halfedge = False

    def delvertex(self,x,y):
        tar = self.find_closest_vertex(x,y)
        if tar:
           self.can.delete(tar[0])
           while len(tar[3]) > 0:
               self.delete_edge_by_key(tar[3][0])
           del(self.vlist[tar[1]])

    def deledge(self,x,y):
        etar = self.find_closest_edge(x,y)
        if etar:
           self.can.delete(etar[0])
           self.delete_edge_by_key(etar[1])
    
    def drag(self,event):
        x = self.can.canvasx(event.x)
        y = self.can.canvasy(event.y)
        if self.var.get() == 5:
           if self.tar1:
              vh = self.tar1[1]
              r = self.rad
              self.can.coords(self.tar1[0],(x-r,y-r,x+r,y+r))
              for eh in self.vlist[vh][3]:
                  e1 = self.elist[eh]
                  co = self.can.coords(e1[0])
                  if e1[2][0] == vh:
                     co = (x,y,co[2],co[3])
                  else:
                     co = (co[0],co[1],x,y)
                  self.can.coords(e1[0],co)

    def drop(self,event):
        if self.var.get() == 5 and self.tar1:
           self.can.itemconfig(self.tar1[0],fill="red")
           self.tar1 = None
 
    def adjacency_list(self):
        tmp = list(self.vlist.keys())
        numberof = {tmp[i]:i for i in range(len(tmp))}
        return [[numberof[v] for v in self.vlist[u][2]] for u in tmp]
        

    def graph_mod(self,event):
        x = self.can.canvasx(event.x)
        y = self.can.canvasy(event.y)
        if self.var.get() == 1:
           self.addvertex(x,y)
        elif self.var.get() == 2:
           if not self.halfedge:
              self.start_edge(x,y)
           else:
              self.finish_edge(x,y)
        elif self.var.get() == 3:
           self.delvertex(x,y)
        elif self.var.get() == 4:
           self.deledge(x,y)
        elif self.var.get() == 5:
           if self.tar1:
              self.can.itemconfig(self.tar1[0],fill="red")
           self.tar1 = self.find_closest_vertex(x,y)
           if self.tar1:
              self.can.itemconfig(self.tar1[0],fill="green")
           else:
              self.debug()
              print("Error")
        self.message()

    def clear(self):                         # start over
        self.can.delete(ALL)
        self.vlist = {}
        self.elist = {}        
        self.message()
        self.cylenflag = False
   

    def destroy(self):
        self.quit()
   
    def savegraph(self):
        with open('tmpfile.graph','w') as f:
             for i,x in enumerate(self.adjacency_list(),start=1):
                 vert = self.can.coords(i)
                 tmp = str(vert[0])+","+str(vert[1])+" "
                 f.write(tmp)
                 for v in list(x):
                     coord = self.can.coords(v+1)
                     f.write(str(coord[0])+","+str(coord[1])+" ")
                 f.write("\n")
        f.close()

    def readgraph(self):
        self.clear()
        isTrue = True
        filename = filedialog.askopenfilename(filetypes = (("Graph Files Only","*.graph"),("All Files","*.*")))
        with open(filename,'r') as f:
             for line in f.readlines():
                 coords = line.split()
                 print(coords)
                 for x in coords:
                     v = list(map(float,x.split(",")))
                     print(v)
                     if isTrue:
                       v1 = v
                       self.addvertex(v1[0],v1[1])
                       isTrue = False
                     else:
                       self.addvertex(v[0],v[1])
                       self.start_edge(v1[0],v1[1])
                       self.finish_edge(v[0],v[1])
                 isTrue = True

    def disjoint(self,e1,e2):
        if e1[0] in e2: return False
        if e1[1] in e2: return False
        return True

    def leftturn(self,p,q,r):
        dx1 = q[0] - p[0]
        dy1 = q[1] - p[1]
        dx2 = r[0] - p[0]
        dy2 = r[1] - p[1]
        return dx1*dy2 - dx2*dy1 > 0

    def crossing(self,vli):
        f1 = self.leftturn(vli[0],vli[1],vli[2])
        f2 = self.leftturn(vli[0],vli[1],vli[3])
        if f1 == f2: return False
        f1 = self.leftturn(vli[2],vli[3],vli[0])
        f1 = self.leftturn(vli[2],vli[3],vli[1])
        if f1 == f2: return False
        return True
        
    def edgecrossing(self):
        li = list(self.can.find_withtag("VERTEX"))
        self.cl = {}
        for i,v in enumerate(li,start=1):
            self.cl[i] = self.can.coords(v)
        tally = 0
        self.val = []
        for z in list(self.elist.values()):
            x = self.vlist[z[2][0]][0]
            y = self.vlist[z[2][1]][0]
            self.val.append((x,y))
        for i in range(0,len(self.val)):
            e1 = self.val[i]
            for j in range(i+1,len(self.val)):
                e2 = self.val[j]
                if self.disjoint(e1,e2):
                    cl = [self.can.coords(e1[0]),self.can.coords(e1[1]),self.can.coords(e2[0]),self.can.coords(e2[1])]
                    if self.crossing(cl):
                        tally += 1
        return tally

    def degree(self):
        unique = set()
        for y in list(self.vlist.values()):
            v = len(y[2])
            unique.add(v)
        s = sorted(list(unique))
        return s
        
    def recoloredge(self,u,v):
        for e in self.elist.values():
            if u in e[2] and v in e[2]:
               self.can.itemconfig(e[0],fill="green")


    def longestcycle(self):
         klist = list(self.vlist.keys())
         adjlist = self.adjacency_list()
         n = len(adjlist)
         degree = [len(edgeli[2]) for edgeli in self.vlist.values()]
         alist = [[a]+b for a,b in zip(degree,adjlist)]
         self.cycle = LongestCycle.findCycle(n,alist)     # C module to find longest cycle
         print("degree = ", degree, "\n alist = ", alist, "\n cycle = ", self.cycle)
         self.cylen = len(self.cycle)
         if self.cylen > 2:
            for i in range(self.cylen):
                self.recoloredge(klist[self.cycle[i]],klist[self.cycle[(i+1)%self.cylen]])
         if self.cylen:
            self.cylenflag = True
            self.message()


if __name__ == "__main__":
    root = Tk()
    app = App(root)
    root.title("GraphApp")
    app["bg"] = "#1a0000"
    app.mainloop()

