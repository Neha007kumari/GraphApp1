#include <python3.5m/Python.h>

typedef struct vertex {
  int deg;
  int *nbr;
} VERTEX;

static PyObject* py_longcycle(PyObject *self, PyObject *args);

int findcycles(int cylist[], int n, VERTEX b[]);
int cycledfs(int cylist[], int G, int tv, int u, int dep, int cl[], VERTEX b[]);

static PyObject* py_longcycle(PyObject *self, PyObject *args)
{
  int i,j,k,n;
  PyObject *li, *p, *q;
  PyObject *list;
  PyObject *item;
  VERTEX *b;
  int *cl;

  if (!PyArg_ParseTuple(args, "iO", &n, &li))
    return NULL;
  b = (VERTEX *) malloc(n*sizeof(VERTEX));
  cl = (int *) malloc(n*sizeof(int));
  for(i=0;i<n;i++){
    p = PyList_GetItem(li,i);
    q = PyList_GetItem(p,0);
    k = PyLong_AsLong(q);
    b[i].deg = k;
    b[i].nbr = (int *) malloc(k * sizeof(int));
    for(j=0;j<k;j++){
      q = PyList_GetItem(p,j+1);
      b[i].nbr[j] = PyLong_AsLong(q);
    }
  }
  k = findcycles(cl,n,b);
  if(k == 0)
    return PyList_New(0);
  list = PyList_New(k);
  for(i=0;i<k;i++){
    item = PyLong_FromLong(cl[i]);
    PyList_SetItem(list,i,item);
  }
  for(i=0;i<n;i++)
    free(b[i].nbr);
  free(b);
  free(cl);
  return list;
}
int findcycles(int cylist[], int n, VERTEX *b)
{
  int g,i,j;
  int cl[n];

  for(g=n;g>=2;--g){
    for(i=0;i<=n-g;i++){
      for(j=0;j<n;j++)
        cl[j]=0;
      cl[i]=1;
      cylist[0] = i;
      if(cycledfs(cylist,g,i,i,1,cl,b))
        return g;
    }
  }
  return 0;
}
int cycledfs(int cylist[], int g, int tv, int u, int dep, int cl[], VERTEX b[])
{
  int i,v;
  if(dep==g){
    for(i=0;i<b[u].deg;i++){
      if(tv==b[u].nbr[i]){
        return 1;
      }
    }
    return 0;
  }
  for(i=0;i<b[u].deg;i++){
    v=b[u].nbr[i];
    if(cl[v])
      continue;
    if(v <= tv)
      continue;
    cl[v] = 1;
    cylist[dep] = v;
    if(cycledfs(cylist,g,tv,v,dep+1,cl,b))
      return 1;
    cl[v] = 0;
  }
  return 0;
}

static PyMethodDef cyclesMethods[]={
  {"longcycle", py_longcycle, METH_VARARGS, "Longest Cycle"}
};

static struct PyModuleDef cycles = {
  PyModuleDef_HEAD_INIT,
  "cycles",
  "Longest Cycle",
  -1,
  cyclesMethods
};

PyMODINIT_FUNC
PyInit_cycles(void)
{
  fprintf(stderr,"cycles\n");
  return PyModule_Create(&cycles);
}
