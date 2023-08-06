# vectorplot

**vectorplot** é um pacote simples e fácil para plotar vetores no espaço bidimensional e tridimensional.

## Dependências
**Python 3.6** ou posterior

Pacote **numpy**
Pacote **matplotlib.pyplot**


## Começando o uso
Você vai precisar instalar o pacote **vectorplot**, para isso basta executar:
```
pip install vectorplot
```

## Funções

* `plot2D([<lista de vetores>],[<lista de cores para cada vetor],[<limites da plotage 2D>])` - Plota vetores no espaço bidimensional
```
Ex: 
pip install vectorplot
import numpy as np
from vectorplot import vp

u_laranja='#FF9A13'
v_azul='#1190FF'
r_vermelho='#FF0000'

u=[1,2]
v=[2,1]
u=np.array(u)
v=np.array(v)
r=u+v

vp.plot2D([u,v,r], [u_laranja,v_azul,r_vermelho], [-3,3,-3,3])
```

* `plot2D([<Lista de coordenadas dos vetores>],[<lista de cores para cada vetor],[<limites da plotage 2D>])` - Plota vetores no espaço bidimensional
```
Ex: 
pip install vectorplot

u_laranja='#FF9A13'
v_azul='#1190FF'

u=[[1,8],[3,5]]
v=[[4,2],[6,7]]

plot2d([u,v], [[u_laranja],[v_azul]], [-10,10,-10,10])
```

* `coord_to_vector([<Lista de coordenadas dos vetores>])` - Converte lista de coordenadas em um vetor
```
Ex: 
pip install vectorplot
import numpy as np
from vectorplot import vp

u=[[1,8],[3,5]]
u=coord_to_vector(u)
print(u)

```

* `plot3D([<lista de vetores>],[<lista de cores para cada vetor],[<limites da plotage 3D>])` - Plota vetores no espaço tridimensional
```
Ex: 
pip install vectorplot
import numpy as np
from vectorplot import vp

u_laranja='#FF9A13'
v_azul='#1190FF'
r_vermelho='#FF0000'

u=[-1,1,2]
v=[2,3,2]
u=np.array(u)
v=np.array(v)
r=u+v

vp.plot3D([u,v,r],[u_laranja,v_azul,r_vermelho],[-4,4,-4,4,-4,4])
```