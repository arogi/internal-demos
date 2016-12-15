<b>Using Docker with Circuit-Web</b>  
<hr />

*Prerequisites*  

 1. Install Docker. Their webpage has [instructions](https://docs.docker.com/engine/installation/).

 2. In Windows and OS X, launch the Docker app. Linux uses the standard Terminal.

 3. Make a local copy of internal-demos. Type:  
    `git clone https://github.com/arogi/internal-demos.git`


*Getting Started*

 1. From within the internal-demos folder, build the Docker image. Type: `./build.sh`  
    *Note: this process may take over 15 minutes*  

 2. Type: `docker run -d -p 80:80 arogi/internal-demos`  

 3. Open a web browser and enter the `localhost` into the address bar:  


*Running TSP on a Road Network — (OS X and Windows only, will add Linux support soon)*  

 1. Type: `docker pull arogi/arogi-valhalla` to grab the latest Arogi-Valhalla Docker image.
    *Note: This downloads statewide road networks for CA, NV, OR, and AZ. Thus it may take a while, depending on your network speed.*

 2. Type: `docker run -it -d -p 8002:8002 arogi/arogi-valhalla`  

 3. Type `docker ps -a` and check if circuit-web container is still running. If not, do "Getting Started" section above.  

 4. Open a web browser and enter the following into the address bar:  
     On OS X and Windows, enter `192.168.99.100/network.html`. On Linux, enter `localhost/network.html` 


*Shutting Down*  

 1. In the terminal, type: `docker ps -a`  
    to see a list of all local docker containers. Note the name it gives as a label. It often is something like: `jolly_ptolemy`

 2. To stop Docker, type: `docker stop container_name`

 3. To remove the container, type: `docker rm container_name`

 4. To remove the image, type: `docker rmi image_name` (e.g., `docker rmi arogi/circuit-web`)
