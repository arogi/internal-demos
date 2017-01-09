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

 3. Open a web browser and enter the `localhost` into the address bar.


*Shutting Down*  

 1. In the terminal, type: `docker ps -a`  
    to see a list of all local docker containers. Note the name it gives as a label. It often is something like: `jolly_ptolemy`

 2. To stop Docker, type: `docker stop container_name`

 3. To remove the container, type: `docker rm container_name`

 4. To remove the image, type: `docker rmi image_name` (e.g., `docker rmi arogi/internal-demos`)


*Troubleshooting*

 1. If when running `docker run` you get an error that includes `Error starting userland proxy: Bind for 0.0.0.80: unexpected error`, then try running on a different port, e.g. `81:80`. Then in the browser, you will have to open the webpage `http://localhost:81/`
