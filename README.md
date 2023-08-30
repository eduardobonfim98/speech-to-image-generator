# Speech to Text Image Generator
*The development repository had private keys in its commits, necessitating the creation of a new public repository with only one commit to make the project accessible without compromising security.

  :movie_camera: :us: Video presentation of the project: https://youtu.be/SVxiDAktYoc 
  
  :movie_camera: :brazil:   Apresentação do projeto: https://youtu.be/82APdt9iw6g
  
During my internship at the Centre for Artificial Intelligence at the Zurich University of Applied Sciences (Switzerland), I had the opportunity to work on an exciting and diverse project that aimed to demonstrate the practical applications of various machine learning models. The project encompasses the following key components:

<img width="889" alt="1" src="https://user-images.githubusercontent.com/77940524/264304517-f9011a7f-3a0d-41fc-9054-1a9c860e4f5f.png">

1-) A  model designed for translating Swiss German or German to English, which was developed in-house by our research center. This language translation model showcases our team's expertise in natural language processing.

2-) A novel use of ChatGPT as a prompt enhancement tool. Through meticulous training with personalized prompts, I empowered ChatGPT to better understand and enhance user prompts, leading to the generation of better images with the Openjorney model.

3-) Openjorney, an open source text-to-image model that generates AI art images in the distinctive style of Midjourney. This unique model is a fine-tuned version of Stable Diffusion.
Another novel use of the stable diffusion model is to show the the denoising processing, coming from noise and becoming the image.

I have included a question mark button within the interface. By clicking on this button, users can access a comprehensive explanation of how the models function and the step-by-step process of the denoising technique. 

Overall, this project allowed me to gain invaluable experience in cutting-edge machine learning technologies and their practical applications while contributing to the research efforts of the Centre for Artificial Intelligence.

You can access the project at this URL https://160.85.252.37/

Unfortunatelly, the running version is not accessible publicly because we pay for the OpenAI API and the use of our dedicated computational resources to run the models. As a result, we are unable to provide open access to the project at this time, but you are welcomed to go to one of ours events to check it out.

***Currently the translation function is not support on Safari and Google Chrome MOBILE due to the audio type not being supported**

# Project workflow
<img width="889" alt="1" src="https://user-images.githubusercontent.com/77940524/264304476-25305e30-192e-46f9-aa3c-3644ffc02647.png">

After typing the prompt "Mountains on Mars with a blue lake" and clicking on the button "Generate Image" you can see the denoising process happening and the image being generated.

<img width="889" alt="1" src="https://user-images.githubusercontent.com/77940524/264304503-5de5807c-58e7-4ed6-8cae-7c7cc4ba1f86.png">

The generated imaged:

<img width="889" alt="1" src="https://user-images.githubusercontent.com/77940524/264304483-99167438-19cd-444f-bdd1-6d0dd6cdd6c8.png">

Using the ChatGPT to improve the quality and the level of specifications of a prompt sent to the image generation model. To generate a good image you most know a lot of parameters that will increase the level of detail of the image. ChatGPT was prompt engineered to enhance a simple prompt, enhancing the previous prompt we have "Stunningly beautiful view of Mountains on Mars with a blue lake, ultra-highres, alien landscape, surrealist 3D rendering, art by HR Giger and James Gurney, DenviantArt, volumetric lighting, intricate, warm and saturated colors." 

<img width="889" alt="1" src="https://user-images.githubusercontent.com/77940524/264304524-53795e4a-db89-4de6-9784-05a05d4e2d6c.png">

And generating the image again with the new prompt we have those two images: 

<img width="889" alt="1" src="https://user-images.githubusercontent.com/77940524/264304519-2bf1efa6-3a6b-4bfd-a775-f20bdcd6ed29.png">

# Step by Step for deployment

# Create SSL Key
- I used this tutorial: https://blog.miguelgrinberg.com/post/running-your-flask-application-over-https

- Use openssl to create the certificate and the key: openssl req -x509 -newkey rsa:4096 -nodes -out cert.pem -keyout key.pem -days 365

- Make sure that the keys are stored in the correct folder, in my case I stored in src folder of the frontend


## Install locally using conda

````bash
conda create --name denoising-demo python
conda activate denoising-demo
pip install -r requirements.txt
````
# /frontend

I used this tutorial: https://blog.miguelgrinberg.com/post/how-to-deploy-a-react--flask-project

- ```npm install```

- In /frontend run ```npm run build``` this will create the dist folder

- I used Nginx: ```sudo apt-get install nginx```

- Remove the default config: ```sudo rm /etc/nginx/sites-enabled/default```

- Create a new config and store it under ```/etc/nginx/sites-available/denoising-demo.nginx```:

  - sudo touch denoising-demo.nginx

  - sudo nano denoising-demo.nginx 
  
- Run ```sudo ln -s /etc/nginx/sites-enabled/denoising-demo.nginx /etc/nginx/sites-available/denoising-demo.nginx``` to create a symlink between the two files
  
```server {
                listen 443 ssl http2;
                root /home/ubuntu/zhaw-demo-template/frontend/dist;
                index index.html;
                ssl_certificate /home/ubuntu/zhaw-demo-template/frontend/cert.pem;
                ssl_certificate_key /home/ubuntu/zhaw-demo-template/frontend/key.pem;

               
                location /api  {
                        include proxy_params;
                        proxy_pass https://160.85.252.37:8000;
                }
        }
```

- You have to change the IP adress in the following files
  - /frontend/vite.config.js
  - /frontend/package.json
  - /frontend/src/base.ts
  - /frontend/src/views/LoginView.vue

- To start and stop the server you can use
    - sudo systemctl start nginx
    - sudo systemctl stop nginx
  
- Dont forget to change the relative path for the certificates
- Dont forget to change the IP adress to the IP adress of the server  
- sudo nginx -t to check if the config is correct
- sudo systemctl status nginx
- You can also check the error logs in the /var/log/nginx/
- You can also check the error logs for the gunicorn /var/log/gunicorn/

# /backend

- export <RABBIT_MQ_PW_PASSWORD>
- pip install gunicorn
- pip install connexion flask_cors
- For the backend to work you have to change your IP address accordingly in the files:
    - /backend/swagger_server/swagger/swagger.yaml

- ``gunicorn --certfile swagger_server/cert.pem --keyfile swagger_server/key.pem -b 0.0.0.0:8000 wsgi:app``

- You can access the swagger https://0.0.0.0:8000/api/ui/

# Running the services /backend/swagger_server/services

- GPT3
- export <RABBIT_MQ_PW_PASSWORD>
  ``python rpc_server.py --model gpt-3``

- StableDiffusion
- export <RABBIT_MQ_PW_PASSWORD>
  ``python rpc_server.py --model stable_diffusion``

- Audio
- export <RABBIT_MQ_PW_PASSWORD>
  ```python rpc_server.py --model audio```

# RabbitMQ
- ``docker images`` to see the images 
- Use the rabbitmq:3.11-management to have access to the browser management interface
- If you don't have the image use ``docker pull`` to get the image
  - ``docker run -d --name my_rabbitmq -p 5672:5672 -p 15672:15672 rabbitmq:3.11-management``
- Use ``docker ps`` to see the running containers and get the container ID
- ``docker exec -it [ID] bash`` to run the bash inside the container
- To use the rabbitmq command line use ``rabbitmqctl`` or you can go to the http://160.85.252.37:15672/ and use the browser interface
- The standard user is guest and the password is guest
- You have to create a user with the tag administrator, I created ``admin`` with the password ``<RABBIT_MQ_PW_PASSWORD>``
- You have to create a Virtual Hosts, i created ``zhaw-demo-template``
- The user admin has to have access to the virtual host

- With the command line you can do the following
  - rabbitmqctl add_user admin
  - rabbitmqctl list_users
  - rabbitmqctl list_user_permissions admin
  - set_user_tags "admin" administrator
  - rabbitmqctl add_vhost zhaw-demo-template
  - rabbitmqctl list_vhosts
  - rabbitmqctl set_permissions -p "zhaw-demo-template" "admin" "." "." ".*"

- Virtual host documentation https://www.rabbitmq.com/vhosts.html

- Authentication, Authorisation, Access Control documentation https://www.rabbitmq.com/access-control.html

# MongoDB
- docker run --name mongodb -d -p 27017:27017 mongodb/mongodb-community-server:6.0-ubi8
- Login into Container (docker ps to get the id -> docker exec -it 70e822bb095f bash) and define username password
$ mongosh
$ db.createUser({ user: "admin", pwd: "<RABBIT_MQ_PW_PASSWORD>", roles: [ { role: "readWrite", db: "mydb" } ] })

- open port 27017 on APU (sage)
- change config.yaml to new IP address

# Possible problems
- 1 -) 403 error, I solved it by changing the permissions of the project folder
- sudo chmod o+x /home/eduardosiq/
- sudo chmod o+x /home/eduardosiq/Documents/
- sudo chmod o+x /home/eduardosiq/Documents/deployment/

- 2 -) Redirect to the default apache page
- I solved changing to the port 8843 in the nginx config file

```                                                                                                                                                                                                             
server {
                listen 8443 ssl http2;
                root /home/eduardosiq/Documents/deployment/zhaw-demo-template/frontend/dist/;
                index index.html;
                ssl_certificate /home/eduardosiq/Documents/deployment/zhaw-demo-template/frontend/cert.pem;
                ssl_certificate_key /home/eduardosiq/Documents/deployment/zhaw-demo-template/frontend/key.pem;

                location /api  {
                        include proxy_params;
                        proxy_pass https://localhost:8000;
                }
        }
```
