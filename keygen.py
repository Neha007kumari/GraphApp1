
class VertexKey:
  
  seed = [ord('a')]*4

  def increment():
   n = 0
   while VertexKey.seed[n] == ord('z'):
         VertexKey.seed[n] = ord('a')
         n += 1
   VertexKey.seed[n] += 1

  def keygen():
   VertexKey.increment()
   return "".join(list(map(chr,VertexKey.seed)))
   

  
if __name__ == "__main__":
   for i in range(29):
       print(VertexKey.keygen())
   

      
