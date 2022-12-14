# El plan
Este repositorio contiene los ejercicios desarrolados de una prueba para un puesto de backend development donde 1) se mejora un algoritmo para procesar órdenes financieras ficticias y 2) Se hace una REST API basada en el algoritmo anterior.

# Setup
Este ejercicio fue desarrollado en una maquina linux asi que es posible que no funciones algunas partes si se ejecuta en un computador con sistema operativo windows. Esto es debido a que los paths no se hicieron agnosticos de sistema operativo.
El archivo requirements.txt contiene los paquetes que hay que instalar para poder ejecutar correctamente los archivos de este repositorio. Esto se logra con el commando: `pip install -r requirements.txt`.

Para la primera task solo se uso el paquete de matplotlib para mostrar graficamente la diferencia de rendimiento entre el algoritmo original y el nuevo.

El server de FastAPI (uvicorn) se ejecuta con el comando `uvicorn main:app --reload` estando en la carpeta "task_2". Normalmente se ejecuta en el puerto 8000 pero este valor se puede cambiar. Para probar la api se puede navegar a `localhost:8000/docs`.
 
# Ejercicio 1
En el primer ejercicio el algoritmo procesa órdenes financieras. La clase principal y única se llama OrdersManagers. Esta clase tiene métodos para crear el id de las órdenes de manera programática (en el constructor se usa), loguear la información y guardar las órdenes en las bases de datos. El método principal es 'process orders' donde se usan las funciones logging y de guardado en base de datos (save_on_db) para procesar la información financiera creada en la base de datos en el constructor usando la función __generate_fake_orders.

El quid del asunto es el método save_on_db. Este es el proceso que nos interesa en este caso, pues es el proceso que toma bastante tiempo (500 segundos), en realizarse.
Esta función es falsa, no guarda realmente nada  una base de datos, solamente invoca un número random del 0 a 1 que representa, imagino yo, el tiempo que se demorara procesar una transacción para guardarla en una base de datos.
El problema que veo es que no hay realmente una necesidad de esperar a que cada orden se procese esperando al resultado de la función anterior. Las variables que se guardan no están relacionadas de una manera en que cada tarea dependa del resultado de la tarea anterior.

Bueno entonces ya hemos determinado que el algoritmo puede mejorarse al hacer que se procesen un número aún no determinado de órdenes al mismo tiempo. Pero tradicionalmente existen dos tipos de concurrencia en Python: threading y multiprocessing (paralelismo) .
Para evitar discusiones teóricas que nos impida llegar a crear código, definamos escuetamente estos dos posibles caminos de acción.

Threading se usa cuando las tareas que queremos que realice nuestro programa están limitadas por los inputs y outputs (i/o bound), es decir, lo que hace que nuestro programa se demore son procesos de escribir, recolectar, descargar o enviar información. Esto es contrario a que un proceso esté limitado por la cpu, es decir, cuando la velocidad del programa sea limitada por el procesamiento de tareas intensivas en el cpu o gpu. Un ejemplo de estas últimas pueden ser cuestiones de procesamientos matemáticos, por ejemplo el renderizado de las gráficas de un videojuego.

Generalmente para cuestiones de limitación I/O se usa threading y para cuestiones de limitación por la cpu se usa multiprocessing o paralelismo. Esto es por que para los problemas limitados I/O no es necesario crear más procesos en la cpu que están trabajando en otras tareas al mismo tiempo, el problema no es la capacidad de la cpu, asi que seria una perdida de recursos.

En nuestro problema la función para volver más efectiva consiste en guardar elementos en una base de datos. Bueno, realmente consiste en crear un tiempo determinado para que el proceso se pare con la función sleep. Pero de una u otra manera no es un proceso que esté limitado por la capacidad del procesador, así que usaremos threading para optimizarlo.

También además de mejorar el algoritmo un paso importante que tenemos que tener en cuenta es crear funciones para probar la efectividad de los cambios que le hacemos al algoritmo. Creo que matplotlib nos ayudará a ver las diferencias visualmente.
 
## Ejecucion task 1
El algoritmo de threading cambio mucho el rendimiento del algoritmo como se puede ver en el archivo comparacion_algos.py. El número de threads debe tomarse tomando en cuenta que entre mayor número de threads más poder de procesamiento en la CPU es necesario.
 
## Para la task 2
Para el segundo ejercicio se pide planear la arquitectura de un servicio de finanzas que debe manejar una cantidad de 10000000 de transacciones.
Al pensar en escoger una arquitectura para una aplicación hay muchos factores que hay que pensar. El paradigma anterior de arquitectura de software era crear aplicaciones monolíticas donde todas las diferentes ramas y tareas que debía manejar el programa estaban unidas de tal forma que formaban una sola aplicación imposible de separar por utilidad.

Este paradigma de arquitectura tiene ventajas como que es más fácil y rápido para los desarrolladores crearla, pero tiene problemas en que es difícil hacerla escalar pues cambiamos en una pequeña parte del código y afectan a toda la aplicación así que hay que cambiar toda. Este tipo de aplicaciones no escalan muy bien por que si hay una parte de la arquitectura que necesite más recursos, al estar interconectado de maneras no evidente antes y no homologadas, con otras parte de la aplicación, no se pueden hacer escalar individualmente.

Debido a las desventajas del paradigma monolítico de arquitectura de aplicación se empezó a cambiar a una arquitectura de microservicios donde una aplicación se compone por diferentes mini aplicaciones (api), desplegables individualmente, que se comunican entre sí por medio de formas transparentes y agnósticas de lenguaje.

Las ventajas consisten en que es más fácil escalar las aplicaciones y es más sencillo desarrollar cambios a la arquitectura, es más comprensible para personas nuevas al proyecto. Pero un problema consiste en que es más difícil comunicar los datos entre las aplicaciones y que toma más tiempo desarrollarlas que las aplicaciones monolíticas.
 
En el caso de escoger patrones de arquitectura de microservicios hay muchos patrones a los que podríamos escoger. Podríamos por ejemplo hacer una base de datos por cada servicio que creemos. Pero en este caso no lo creo necesario pues el problema no nos habla aún de muchos servicios para realizar. Así que por lo menos con los datos aportados para el ejercicio, ya que solo se habla de un tipo de datos, tener una base de datos unificada será más conveniente.

Un patrón importante para la aplicación creo que será la arquitectura "strangler". Este patrón de desarrollo se usa a menudo cuando se quiere migrar una arquitectura monolítica a una por microservicios, y cuando este proceso se quiere hacer lentamente y con cuidado.
Este patrón consiste en desarrollar los nuevos servicios de la aplicación por medio de una arquitectura de microservicios y tratar de crear abstracciones con la aplicación antigua para crear apis que se acoplen a la arquitectura de microservicios.

Este patrón nos será útil en esta aplicación por lo que el problema nos indica que el cliente tiene una arquitectura antigua que quiere cambiar, y como la aplicación trata con información financiera, que por lo general es sensible, tendría sentido ir cambiando la arquitectura poco a poco en vez de hacerlo de una vez, pues podría ser muy costoso para la empresa los bugs que inevitablemente puedan encontrarse al crear una arquitectura desde 0, nuevamente.
 
Para esta aplicación voy a usar el framework de FastAPI. Hay otros frameworks para el backend de Rest Apis pero esta tiene varias ventajas entre las demás opciones.
en [este link](https://www.techempower.com/benchmarks/#section=data-r19&hw=ph&test=fortune&l=zijzen-1r&f=0-0-0-0-0-1ekg-0-0-4fti4g-0-0) podemos ver que fastapi está en un puesto muy alto de rapidez, superior a flask y django que son otros frameworks muy conocidos y utilizados.

Esto no es la única ventaja. Fast API también es un framework muy intuitivo con una buena documentación  y con poco código boilerplate.Esto es conveniente para la aplicación de finanzas que debemos construir pues no necesitamos un framework que nos haga ya todo, pues esta aplicación puede contener muchas cosas no ordinarias para aplicaciones web comunes, por ejemplo una página web de un blog.

Para el lado de las bases de datos creo conveniente usar postgresql por que es un framework de sql moderno, con una buena documentación, una gran cantidad de usuarios, y mucha flexibilidad para hacer cosas modernas en sql.

Para el deployment de nuestra aplicación podremos usar docker, especialmente docker swarm para poder desarrollar los procesos de la aplicación financiera en una red de computadoras escalables.

Al ser esta una aplicación financiera, tendría sentido usar servidores propios en vez de soluciones para un fácil despliegue de aplicaciones como Azure AWS o GCP pues es la arquitectura seguramente ya está corriendo en servidores privados locales. Al ser un proyecto que puede llegar a necesitar mucho poder de procesamiento y debe tener una gran flexibilidad, en mi opinión no vale la pena usar servicios externos de hosting y deployment en la nube. Se pueden ahorrar en gastos en el tiempo y se puede tener más seguridad y control con una arquitectura de servidores locales.

Para la autorización al uso de la aplicación puede usarse auth02 con jwt. Fast API tiene soporte nativo de authO2 lo que lo hace muy fácil y conveniente trabajar con este tipo de sistemas de autenticación.
 
## Diagrama de la arquitectura
![Alt text](/diagram.png "a title")
 
## Ejecucion
En la carpeta task_2 se encuentra los archivos de la rest api creada con FastAPI. La carpeta db_files es el lugar donde se guardaran los datos resultantes del metodo post
"populate" que inicia una instancia del OrdersManager del algoritmo de la task anterior, crea archivos de transacciones, y los guarda por chunks de 1000 en archivos .json.
El archivo crud.py contiene las funciones que realizan acciones con la base de datos de archivos json. En el archivo main.py se encuentra la aplicacion principal y las rutas con sus metodos respectivos.

En los metodos se encuentra populate, que como su nombre lo indica crea la base de datos en la carpeta db_files. Tambien se encuentran los demas metodos que tienen diferentes formas de conseguir informacion de la base de datos, por pagina, por id o por un rango.

En este momento me doy cuenta de varias formas diferentes en las que podria haber abordado el problema para tal vez haber brindado una mejor solucion.

Pase mucho tiempo creando una forma de almazenar los archivos json envez de usar una base de datos como mongodb que se ocupara de esto. Hacer un sistema de bases de datos no es nada facil. El modelo que cree solo funciona correctamente para obtener informacion de la base de datos pero abria que cambiarlo bastante para guardar informacion en la base de datos.


 

