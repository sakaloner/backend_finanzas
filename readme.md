# El plan
Bueno este repositiorio contiene una prueba de backend development donde 1) tengo que mejorar un algoritmo para que se procesen mejor unas ordenes financieras ficticias y 2) tengo que hacer una rest api alrededor de este algoritmo para una entidad financiera que procesa ordenes.

# Ejercicio 1
En el primer ejercicio el algoritmo procesa ordernes financieras. La clase principal y unica se llama OrdersManagers. Esta clase tiene metodos para crear el id de las ordenes de manera programatica (en el constructor se usa), loggear la informacion y guardar las ordenes en las bases de datos. El metodo principal es 'process_orders' donde se usan las funciones logging y de guardado en base de datos (save_on_db) para procesar la informacion financiera creada en la base de datos en el contructor usando la funcion __generate_fake_orders.
El quid del asunto es el metodo save_on_db. Este es el proceso que nos interesa en este caso, pues es el proceso que toma bastante tiempo (500 segundos), en realizarse.
Esta funcion es falso, no guarda realmente nada  una base de datos, solamente invoca un numero random del 0 a 1 que representa, imagino yo, el tiempoo que se demoraria procesar una transaccion para guardarla en una base de datos.
El problema que veo es que no hay realmente una necesidad de esperar a que cada orden se procese esperando al resultado de la funcion anterior. Las variables que se guarden no estan relacionadas de una manera en que cada tarea dependa del resultado de la tarea anterior.
Bueno entonces ya hemos determinado que el algoritmo puede mejorarse al hacer que se procesen un numero aun no determinado de ordenes al mismo tiempo. Pero tradicionalmente existen dos tipos de concurrencia en python: threading y multiporcessing (paralelismo) .
Para evitar discuciones teoricas que nos impida llegar a crear codigo, definamos escuetamente estos dos posibles caminos de accion.
Threading se usa cuando las tareas que queremos que nuestro realize nuestro programa estan limitadas por los inputs y outputs (i/o bound), es decir, lo que hacee que nuestro programa se demore son procesos de escribir, recolectar, descargar o enviar informacion. Esto es contrario a que un proceso este limitado por la cpu, es decir, cuando la velocidad del programa sea limitada por el procesamiento de tareas intensivas en el cpu o gpu. Un ejemplo de estas ultimas pueden ser cuestiones de procesamientos matematicos, por ejemplo el renderizado de las graficas de un videojuego.
Generalmente para cuestiones de limitacion I/O se usa threading y para cuestiones de limitacion por la cpu se usa multiprocessing o paralelismo. Esto es por que para los problemas limitados I/O no es necesario crear mas procesos en la cpu que esten trabajando en otras tareas al mismo tiempo, el problema no es la capacidad de la cpu, asi que seria una perdida de recursos.
En nuestro problema la funcion para volve mas efectiva consiste en guardar elementos en una base de datos. Bueno, realmente consiste en crear un tiempo determinado para que el proceso se pare con la funcion sleep. Pero de una u otra manera no es un proceso que este limitado por la capacidad del procesador, asi que usaremos threading para optimizarlo.
Tambien ademas de mejorar el algoritmo un paso imprtante que tenemos que tener en cuenta es crear funciones para probar la efectividad de los cambios que le hacemos al algoritmo. Creo que mathplotlib nos ayudara a ver las diferencias visualmente.

## El acto
Hay que pensar en el numero de procesos que haremos. En el ejercicio son 1000 cosas. Necesitamos escojer con algun criterio el numero de threads de 1 en 1000. Tal vez la visualizacion del rendimiento nos ayudara a tener algun fundamento para esto. Pero tambien mas research sobre las desventajas del threading sera necesario. (does it consume ram)

## Para la task 2

